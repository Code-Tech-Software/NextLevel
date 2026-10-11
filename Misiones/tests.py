from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from . import gamificacion as juego
from .models import (
    Alumno, ArticuloTienda, Clase, CompraAlumno, Mision, Mundo, Nivel, OpcionRespuesta, Pregunta, ProgresoMision,
    calcular_nivel, xp_para_nivel,
)

# Las pruebas no dependen del manifiesto generado por collectstatic
ALMACEN_PRUEBAS = {**settings.STORAGES, 'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}}


@override_settings(STORAGES=ALMACEN_PRUEBAS)
class BaseJuego(TestCase):
    def setUp(self):
        self.clase = Clase.objects.create(nombre='Robótica', grado='4', grupo='A', anio=2026)
        self.mundo = Mundo.objects.create(clase=self.clase, nombre='Mundo 1', orden=1)
        self.nivel = Nivel.objects.create(clase=self.clase, mundo=self.mundo, nombre='Nivel 1', orden=1, recompensa_cofre=20)
        self.m1 = Mision.objects.create(clase=self.clase, nivel=self.nivel, nombre='Uno', descripcion='x', tipo='arduino',
                                        orden=1, xp_recompensa=50, monedas_recompensa=10)
        self.m2 = Mision.objects.create(clase=self.clase, nivel=self.nivel, nombre='Dos', descripcion='x', tipo='cuestionario',
                                        orden=2, xp_recompensa=50, monedas_recompensa=20)
        pregunta = Pregunta.objects.create(mision=self.m2, texto='¿2+2?', puntos=10)
        self.correcta = OpcionRespuesta.objects.create(pregunta=pregunta, texto='4', es_correcta=True)
        self.incorrecta = OpcionRespuesta.objects.create(pregunta=pregunta, texto='5')
        self.pregunta = pregunta
        self.alumno = Alumno.objects.create(nombre='Ana', apellido='López', pin='1234')
        self.alumno.clases.add(self.clase)

    def entrar(self):
        self.client.post(f'/clase/{self.clase.id}/alumno/{self.alumno.id}/ingresar/', {'pin': '1234'})


class NivelesTests(TestCase):
    def test_curva_de_niveles(self):
        self.assertEqual(xp_para_nivel(1), 0)
        self.assertEqual(xp_para_nivel(2), 100)
        self.assertEqual(xp_para_nivel(3), 250)
        self.assertEqual(calcular_nivel(0), 1)
        self.assertEqual(calcular_nivel(249), 2)
        self.assertEqual(calcular_nivel(250), 3)


class RutaTests(BaseJuego):
    def test_regla_de_oro_bloquea_lo_siguiente(self):
        ruta = juego.construir_ruta(self.alumno, self.clase)
        items = ruta['mundos'][0]['niveles'][0]['misiones']
        self.assertTrue(items[0]['desbloqueada'])
        self.assertTrue(items[0]['actual'])
        self.assertFalse(items[1]['desbloqueada'])

        juego.calificar(ProgresoMision(alumno=self.alumno, mision=self.m1), 100)
        items = juego.construir_ruta(self.alumno, self.clase)['mundos'][0]['niveles'][0]['misiones']
        self.assertTrue(items[1]['desbloqueada'])

    def test_no_se_puede_entregar_una_mision_bloqueada(self):
        self.entrar()
        self.client.post(f'/clase/{self.clase.id}/mision/{self.m2.id}/completar/',
                         {f'pregunta_{self.pregunta.id}': self.correcta.id})
        self.assertFalse(ProgresoMision.objects.filter(alumno=self.alumno, mision=self.m2).exists())


class CalificacionTests(BaseJuego):
    def test_primera_aprobacion_da_recompensa_y_recalificar_solo_ajusta(self):
        progreso = ProgresoMision.objects.create(alumno=self.alumno, mision=self.m1)
        juego.calificar(progreso, 50)
        self.alumno.refresh_from_db()
        xp, monedas = self.alumno.xp_total, self.alumno.monedas
        self.assertGreaterEqual(xp, 50)

        juego.calificar(progreso, 100)
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.xp_total, xp)
        self.assertEqual(self.alumno.monedas, monedas + 5)

    def test_cuestionario_no_se_puede_repetir_para_ganar_mas(self):
        juego.calificar(ProgresoMision(alumno=self.alumno, mision=self.m1), 100)
        self.entrar()
        url = f'/clase/{self.clase.id}/mision/{self.m2.id}/completar/'
        self.client.post(url, {f'pregunta_{self.pregunta.id}': self.correcta.id})
        self.alumno.refresh_from_db()
        xp = self.alumno.xp_total
        self.client.post(url, {f'pregunta_{self.pregunta.id}': self.correcta.id})
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.xp_total, xp)
        self.assertEqual(ProgresoMision.objects.get(alumno=self.alumno, mision=self.m2).puntuacion, 100)

    def test_opcion_de_otra_pregunta_no_cuenta(self):
        otra = Pregunta.objects.create(mision=self.m1, texto='otra')
        ajena = OpcionRespuesta.objects.create(pregunta=otra, texto='x', es_correcta=True)
        juego.calificar(ProgresoMision(alumno=self.alumno, mision=self.m1), 100)
        self.entrar()
        self.client.post(f'/clase/{self.clase.id}/mision/{self.m2.id}/completar/', {f'pregunta_{self.pregunta.id}': ajena.id})
        self.assertEqual(ProgresoMision.objects.get(alumno=self.alumno, mision=self.m2).puntuacion, 0)

    def test_cofre_solo_una_vez_y_con_nivel_completo(self):
        self.assertIsNone(juego.abrir_cofre(self.alumno, self.nivel))
        juego.calificar(ProgresoMision(alumno=self.alumno, mision=self.m1), 100)
        juego.calificar(ProgresoMision(alumno=self.alumno, mision=self.m2), 100)
        self.assertIsNotNone(juego.abrir_cofre(self.alumno, self.nivel))
        self.assertIsNone(juego.abrir_cofre(self.alumno, self.nivel))


class TiendaTests(BaseJuego):
    def test_stock_limite_y_reembolso(self):
        self.alumno.monedas = 100
        self.alumno.save()
        articulo = ArticuloTienda.objects.create(nombre='Llavero', descripcion='x', costo_monedas=30, stock=1,
                                                 limite_por_alumno=2)
        ok, _ = juego.comprar(self.alumno, articulo)
        self.assertTrue(ok)
        articulo.refresh_from_db()
        self.assertEqual(articulo.stock, 0)
        ok, mensaje = juego.comprar(self.alumno, articulo)
        self.assertFalse(ok)
        self.assertIn('agotó', mensaje)

        compra = CompraAlumno.objects.get(alumno=self.alumno, articulo=articulo)
        self.assertTrue(juego.cancelar_compra(compra))
        articulo.refresh_from_db()
        self.alumno.refresh_from_db()
        self.assertEqual(articulo.stock, 1)
        self.assertEqual(self.alumno.monedas, 100)

    def test_nivel_requerido(self):
        self.alumno.monedas = 500
        self.alumno.save()
        articulo = ArticuloTienda.objects.create(nombre='Comodín', descripcion='x', costo_monedas=10, nivel_requerido=5)
        ok, _ = juego.comprar(self.alumno, articulo)
        self.assertFalse(ok)


class SeguridadTests(BaseJuego):
    def test_api_de_monedas_requiere_profesor(self):
        respuesta = self.client.post('/api/actualizar-monedas/', {'alumno_id': self.alumno.id, 'cantidad': 99, 'accion': 'sumar'})
        self.assertEqual(respuesta.status_code, 302)
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.monedas, 0)

    def test_paginas_del_profesor_cargan(self):
        self.client.force_login(User.objects.create_superuser('profe', 'p@x.com', 'x'))
        for url in ['/profesor/dashboard/', f'/profesor/clases/{self.clase.id}/', '/profesor/revisiones/',
                    f'/clase/{self.clase.id}/matriz/', '/profesor/alumnos/', '/profesor/tienda/', '/profesor/pedidos/',
                    '/economia-alumnos/', '/profesor/diarias/', '/profesor/logros/', f'/profesor/misiones/{self.m2.id}/editar/']:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_alumno_de_otra_clase_no_entra(self):
        otra = Clase.objects.create(nombre='Otra', grado='5', grupo='B', anio=2026)
        self.entrar()
        respuesta = self.client.get(f'/clase/{otra.id}/dashboard/')
        self.assertRedirects(respuesta, f'/clase/{otra.id}/')


class FormulariosEnModalTests(BaseJuego):
    def setUp(self):
        super().setUp()
        self.client.force_login(User.objects.create_superuser('profe', 'p@x.com', 'x'))
        self.modal = {'HTTP_X_MODAL': '1', 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def test_en_modal_solo_se_envia_el_formulario(self):
        for url in ['/forja/clase/nueva/', f'/profesor/mundos/nuevo/?clase={self.clase.id}', '/forja/nivel/nuevo/',
                    '/forja/mision/nueva/', f'/profesor/misiones/{self.m2.id}/editar/', f'/profesor/misiones/{self.m2.id}/calificar/',
                    '/forja/alumno/nuevo/', '/profesor/alumnos/masivo/', '/forja/tienda/nuevo/', '/profesor/diarias/nueva/',
                    '/profesor/logros/nuevo/']:
            respuesta = self.client.get(url, **self.modal)
            self.assertEqual(respuesta.status_code, 200, url)
            self.assertContains(respuesta, 'class="form-panel', msg_prefix=url)
            self.assertNotContains(respuesta, 'class="sidebar"', msg_prefix=url)
            # Sin la cabecera se ve la página completa
            self.assertContains(self.client.get(url), 'class="sidebar"', msg_prefix=url)

    def test_guardar_en_modal_responde_json_y_errores_vuelven_al_formulario(self):
        datos = {'nombre': 'Nueva', 'grado': '6', 'grupo': 'A', 'anio': 2026, 'icono': 'X', 'color': 'uva'}
        respuesta = self.client.post('/forja/clase/nueva/', datos, **self.modal)
        self.assertEqual(respuesta.json()['ok'], True)
        self.assertTrue(Clase.objects.filter(nombre='Nueva').exists())

        respuesta = self.client.post('/forja/clase/nueva/', {'nombre': ''}, **self.modal)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'con-error')
        self.assertNotContains(respuesta, 'class="sidebar"')

    def test_mision_con_errores_conserva_las_preguntas(self):
        preguntas = '[{"texto": "Pregunta escrita", "puntos": 10, "opciones": [{"texto": "a", "es_correcta": true}, {"texto": "b"}]}]'
        respuesta = self.client.post('/forja/mision/nueva/', {'tipo': 'cuestionario', 'preguntas_json': preguntas}, **self.modal)
        self.assertContains(respuesta, 'Pregunta escrita')

    def test_alta_masiva_navega_a_credenciales(self):
        respuesta = self.client.post('/profesor/alumnos/masivo/', {'clase': self.clase.id, 'nombres': 'Luis Ruiz'}, **self.modal)
        datos = respuesta.json()
        self.assertTrue(datos['navegar'])
        self.assertIn('/profesor/alumnos/credenciales/', datos['redirect'])


class ModoClaseTests(BaseJuego):
    def setUp(self):
        super().setUp()
        from .models import Comportamiento, Equipo
        self.positivo = Comportamiento.objects.create(nombre='Participación', icono='🙋', monedas=5, xp=10)
        self.negativo = Comportamiento.objects.create(nombre='Distracción', icono='📵', monedas=-3, xp=0)
        self.equipo = Equipo.objects.create(clase=self.clase, nombre='Leones', emoji='🦁')
        self.equipo.miembros.add(self.alumno)

    def test_comportamiento_positivo_da_monedas_xp_y_puntos_al_equipo(self):
        juego.registrar_conducta(self.alumno, self.clase, self.positivo)
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.monedas, 5)
        self.assertEqual(self.alumno.xp_total, 10)
        self.assertEqual(juego.ranking_equipos(self.clase)[0].total, 10)

    def test_negativo_nunca_deja_saldo_negativo_y_deshacer_revierte(self):
        self.alumno.monedas = 2
        self.alumno.save()
        registro = juego.registrar_conducta(self.alumno, self.clase, self.negativo)
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.monedas, 0)
        self.assertEqual(registro.monedas, -2)
        juego.deshacer_conducta(registro)
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.monedas, 2)

    def test_deshacer_positivo_quita_puntos_del_equipo(self):
        registro = juego.registrar_conducta(self.alumno, self.clase, self.positivo)
        juego.deshacer_conducta(registro)
        self.alumno.refresh_from_db()
        self.assertEqual((self.alumno.monedas, self.alumno.xp_total), (0, 0))
        self.assertEqual(juego.ranking_equipos(self.clase)[0].total, 0)

    def test_repartir_equipos_equilibrado_y_un_equipo_por_clase(self):
        from .models import Equipo
        Equipo.objects.create(clase=self.clase, nombre='Lobos', emoji='🐺')
        for i in range(5):
            otro = Alumno.objects.create(nombre=f'A{i}', apellido='X', pin='1111')
            otro.clases.add(self.clase)
        juego.repartir_equipos(self.clase)
        tamanos = sorted(e.miembros.count() for e in self.clase.equipos.all())
        self.assertEqual(tamanos, [3, 3])
        lobos = self.clase.equipos.get(nombre='Lobos')
        juego.asignar_equipo(self.alumno, self.clase, lobos)
        self.assertEqual(self.alumno.equipos.filter(clase=self.clase).count(), 1)

    def test_meta_del_grupo_se_cumple_y_premia_una_sola_vez(self):
        from .models import MetaGrupo
        meta = MetaGrupo.objects.create(clase=self.clase, titulo='Película', tipo='conducta', objetivo=2,
                                        monedas_recompensa=7)
        juego.registrar_conducta(self.alumno, self.clase, self.positivo)
        juego.revisar_metas(self.clase)
        meta.refresh_from_db()
        self.assertIsNone(meta.completada_en)
        juego.registrar_conducta(self.alumno, self.clase, self.positivo)
        juego.revisar_metas(self.clase)
        juego.revisar_metas(self.clase)
        meta.refresh_from_db()
        self.alumno.refresh_from_db()
        self.assertIsNotNone(meta.completada_en)
        self.assertEqual(self.alumno.monedas, 5 + 5 + 7)

    def test_api_y_paginas_del_modo_clase(self):
        anonimo = self.client.post('/api/modo-clase/conducta/', {'clase': self.clase.id, 'comportamiento': self.positivo.id,
                                                                 'alumnos': [self.alumno.id]})
        self.assertEqual(anonimo.status_code, 302)

        self.client.force_login(User.objects.create_superuser('profe2', 'p@x.com', 'x'))
        respuesta = self.client.post('/api/modo-clase/conducta/', {
            'clase': self.clase.id, 'comportamiento': self.positivo.id, 'alumnos': [self.alumno.id]})
        datos = respuesta.json()
        self.assertTrue(datos['ok'])
        self.assertEqual(datos['alumnos'][str(self.alumno.id)]['monedas'], 5)
        deshacer = self.client.post('/api/modo-clase/deshacer/', {'clase': self.clase.id, 'registros': datos['registros']})
        self.assertEqual(deshacer.json()['deshechos'], 1)

        for url in [f'/profesor/modo-clase/{self.clase.id}/', f'/profesor/equipos/clase/{self.clase.id}/',
                    '/profesor/metas/', '/profesor/comportamientos/', f'/profesor/clases/{self.clase.id}/proyector/']:
            self.assertEqual(self.client.get(url).status_code, 200, url)
        for url in ['/profesor/equipos/nuevo/', '/profesor/metas/nueva/', '/profesor/comportamientos/nuevo/']:
            self.assertContains(self.client.get(url, HTTP_X_MODAL='1'), 'form-panel', msg_prefix=url)

    def test_alumno_ve_su_equipo_y_la_meta(self):
        from .models import MetaGrupo
        MetaGrupo.objects.create(clase=self.clase, titulo='Meta visible', tipo='manual', objetivo=5)
        self.entrar()
        tablero = self.client.get(f'/clase/{self.clase.id}/dashboard/')
        self.assertContains(tablero, 'Meta visible')
        self.assertContains(tablero, 'Leones')
        self.assertContains(self.client.get(f'/clase/{self.clase.id}/ranking/?periodo=equipos'), 'tu equipo')

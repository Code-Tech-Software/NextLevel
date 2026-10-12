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


class FormulariosGuiadosTests(BaseJuego):
    def setUp(self):
        super().setUp()
        self.client.force_login(User.objects.create_superuser('profe3', 'p@x.com', 'x'))

    def datos_mision(self, **extra):
        datos = {'nivel': self.nivel.id, 'nombre': 'Nueva', 'descripcion': 'x', 'tipo': 'arduino',
                 'xp_recompensa': 50, 'monedas_recompensa': 15, 'activa': 'on'}
        datos.update(extra)
        return datos

    def orden_nivel(self):
        return list(self.nivel.misiones.order_by('orden').values_list('nombre', flat=True))

    def test_posicion_dentro_del_nivel(self):
        self.client.post('/forja/mision/nueva/', self.datos_mision(nombre='Al inicio', posicion='inicio'))
        self.assertEqual(self.orden_nivel(), ['Al inicio', 'Uno', 'Dos'])
        self.client.post('/forja/mision/nueva/', self.datos_mision(nombre='En medio', posicion=f'despues:{self.m1.id}'))
        self.assertEqual(self.orden_nivel(), ['Al inicio', 'Uno', 'En medio', 'Dos'])
        self.client.post('/forja/mision/nueva/', self.datos_mision(nombre='Final', posicion='final'))
        self.assertEqual(self.orden_nivel()[-1], 'Final')
        # Editar sin mover conserva el lugar
        self.client.post(f'/profesor/misiones/{self.m1.id}/editar/', self.datos_mision(nombre='Uno', posicion='mantener'))
        self.assertEqual(self.orden_nivel()[1], 'Uno')

    def test_link_y_video_necesitan_enlace(self):
        for tipo in ('link', 'video'):
            respuesta = self.client.post('/forja/mision/nueva/', self.datos_mision(nombre=f'Sin enlace {tipo}', tipo=tipo))
            self.assertContains(respuesta, 'con-error')
            self.assertFalse(Mision.objects.filter(nombre=f'Sin enlace {tipo}').exists())

    def test_formulario_de_mision_trae_estructura(self):
        respuesta = self.client.get(f'/forja/mision/nueva/?nivel={self.nivel.id}', HTTP_X_MODAL='1')
        self.assertContains(respuesta, 'estructura-data')
        self.assertContains(respuesta, f'data-nivel-inicial="{self.nivel.id}"')

    def test_logro_nuevo_se_entrega_a_quienes_ya_cumplen(self):
        from .models import Logro, LogroAlumno
        juego.calificar(ProgresoMision(alumno=self.alumno, mision=self.m1), 100)
        conteo = self.client.get('/api/logros/cumplen/', {'condicion': 'misiones', 'valor': 1}).json()
        self.assertEqual(conteo['total'], 1)
        self.assertEqual(self.client.get('/api/logros/cumplen/', {'condicion': 'misiones', 'valor': 5}).json()['total'], 0)

        self.client.post('/profesor/logros/nuevo/', {
            'nombre': 'Pionero', 'descripcion': 'Completa tu primera misión', 'icono': '🚀', 'condicion': 'misiones',
            'valor': 1, 'rareza': 'raro', 'recompensa_monedas': 5, 'recompensa_xp': 0, 'activo': 'on'})
        logro = Logro.objects.get(nombre='Pionero')
        self.assertTrue(LogroAlumno.objects.filter(alumno=self.alumno, logro=logro).exists())

    def test_logro_manual_no_se_entrega_solo(self):
        from .models import Logro, LogroAlumno
        self.client.post('/profesor/logros/nuevo/', {
            'nombre': 'Especial', 'descripcion': 'x', 'icono': '🌈', 'condicion': 'manual', 'rareza': 'legendario',
            'recompensa_monedas': 0, 'recompensa_xp': 0, 'activo': 'on'})
        logro = Logro.objects.get(nombre='Especial')
        self.assertEqual(logro.valor, 1)
        self.assertFalse(LogroAlumno.objects.filter(logro=logro).exists())
        self.assertContains(self.client.get(f'/profesor/logros/{logro.id}/editar/', HTTP_X_MODAL='1'), 'data-form="logro"')


class FormularioDiariaTests(BaseJuego):
    def setUp(self):
        super().setUp()
        self.client.force_login(User.objects.create_superuser('profe4', 'p@x.com', 'x'))

    def test_formulario_guiado_en_modal(self):
        respuesta = self.client.get('/profesor/diarias/nueva/', HTTP_X_MODAL='1')
        self.assertContains(respuesta, 'data-form="diaria"')
        self.assertContains(respuesta, 'Todas las clases')

    def test_objetivos_sin_meta_guardan_uno_y_los_demas_su_meta(self):
        from .models import MisionDiaria
        base = {'descripcion': 'x', 'icono': '⭐', 'recompensa_monedas': 5, 'recompensa_xp': 5, 'activa': 'on'}
        self.client.post('/profesor/diarias/nueva/', {**base, 'titulo': 'Tienda', 'objetivo': 'tienda', 'meta': 9})
        self.client.post('/profesor/diarias/nueva/', {**base, 'titulo': 'Dos misiones', 'objetivo': 'misiones', 'meta': 2})
        self.client.post('/profesor/diarias/nueva/', {**base, 'titulo': 'Sin meta', 'objetivo': 'cuestionarios', 'meta': ''})
        self.assertEqual(MisionDiaria.objects.get(titulo='Tienda').meta, 1)
        self.assertEqual(MisionDiaria.objects.get(titulo='Dos misiones').meta, 2)
        self.assertEqual(MisionDiaria.objects.get(titulo='Sin meta').meta, 1)


@override_settings(STORAGES={**ALMACEN_PRUEBAS, 'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'}})
class FormularioArticuloTests(BaseJuego):
    def setUp(self):
        super().setUp()
        self.client.force_login(User.objects.create_superuser('profe5', 'p@x.com', 'x'))

    def datos(self, **extra):
        datos = {'nombre': 'Premio', 'tipo': 'fisico', 'descripcion': 'x', 'costo_monedas': 50, 'stock': 10,
                 'nivel_requerido': 1, 'requiere_validacion': 'on', 'activo': 'on'}
        datos.update(extra)
        return datos

    def imagen(self):
        from io import BytesIO

        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image
        buffer = BytesIO()
        Image.new('RGB', (4, 4), 'teal').save(buffer, 'PNG')
        return SimpleUploadedFile('avatar.png', buffer.getvalue(), content_type='image/png')

    def test_formulario_guiado_en_modal(self):
        respuesta = self.client.get('/forja/tienda/nuevo/', HTTP_X_MODAL='1')
        self.assertContains(respuesta, 'data-form="articulo"')
        self.assertContains(respuesta, 'monedas-alumnos')

    def test_avatar_necesita_imagen_y_nunca_pasa_por_pedidos(self):
        respuesta = self.client.post('/forja/tienda/nuevo/', self.datos(nombre='Avatar sin foto', tipo='avatar', stock=''))
        self.assertContains(respuesta, 'Los avatares necesitan una imagen')
        self.assertFalse(ArticuloTienda.objects.filter(nombre='Avatar sin foto').exists())

        self.client.post('/forja/tienda/nuevo/', self.datos(nombre='Avatar robot', tipo='avatar', stock='',
                                                             imagen=self.imagen()))
        avatar = ArticuloTienda.objects.get(nombre='Avatar robot')
        self.assertFalse(avatar.requiere_validacion)
        self.assertIsNone(avatar.stock)

    def test_precio_minimo_y_stock_ilimitado(self):
        self.client.post('/forja/tienda/nuevo/', self.datos(nombre='Gratis', costo_monedas=0))
        self.assertFalse(ArticuloTienda.objects.filter(nombre='Gratis').exists())
        self.client.post('/forja/tienda/nuevo/', self.datos(nombre='Privilegio', tipo='permiso', stock=''))
        self.assertIsNone(ArticuloTienda.objects.get(nombre='Privilegio').stock)


@override_settings(STORAGES=ALMACEN_PRUEBAS)
class EtiquetasTiendaTests(BaseJuego):
    def test_cada_tarjeta_dice_que_tipo_de_premio_es_y_como_se_recibe(self):
        ArticuloTienda.objects.create(nombre='Llavero', descripcion='x', costo_monedas=5, tipo='fisico',
                                      requiere_validacion=False)
        ArticuloTienda.objects.create(nombre='Comodín', descripcion='x', costo_monedas=5, tipo='permiso')
        ArticuloTienda.objects.create(nombre='Fondo', descripcion='x', costo_monedas=5, tipo='otro',
                                      requiere_validacion=False)
        self.entrar()
        respuesta = self.client.get(f'/clase/{self.clase.id}/tienda/')
        # Un físico siempre lo entrega el profe, aunque no requiera validación
        self.assertContains(respuesta, '🎁 Físico</span>')
        self.assertContains(respuesta, '🤝 Te lo entrega el profe')
        self.assertContains(respuesta, '🤝 El profe lo autoriza')
        self.assertContains(respuesta, '💻 Digital</span>')
        self.assertContains(respuesta, '⚡ Lo recibes al instante')


@override_settings(STORAGES=ALMACEN_PRUEBAS)
class FormulariosGuiadosAdminTests(BaseJuego):
    def setUp(self):
        super().setUp()
        self.client.force_login(User.objects.create_superuser('profe6', 'p@x.com', 'x'))
        self.modal = {'HTTP_X_MODAL': '1'}

    def test_cada_formulario_guiado_carga_en_la_ventana(self):
        from .models import Comportamiento, Equipo, MetaGrupo
        equipo = Equipo.objects.create(clase=self.clase, nombre='Leones', emoji='🦁')
        meta = MetaGrupo.objects.create(clase=self.clase, titulo='Meta', tipo='manual', objetivo=5)
        boton = Comportamiento.objects.create(nombre='Celular', icono='📱', monedas=-3)
        paginas = {
            '/forja/clase/nueva/': 'clase', f'/profesor/clases/{self.clase.id}/editar/': 'clase',
            f'/profesor/mundos/nuevo/?clase={self.clase.id}': 'mundo', f'/profesor/mundos/{self.mundo.id}/editar/': 'mundo',
            f'/forja/nivel/nuevo/?mundo={self.mundo.id}': 'nivel', f'/profesor/niveles/{self.nivel.id}/editar/': 'nivel',
            '/forja/alumno/nuevo/': 'alumno', f'/profesor/alumnos/{self.alumno.id}/editar/': 'alumno',
            '/profesor/alumnos/masivo/': 'masiva', '/profesor/equipos/nuevo/': 'equipo',
            f'/profesor/equipos/{equipo.id}/editar/': 'equipo', '/profesor/metas/nueva/': 'meta',
            f'/profesor/metas/{meta.id}/editar/': 'meta', '/profesor/comportamientos/nuevo/': 'conducta',
            f'/profesor/comportamientos/{boton.id}/editar/': 'conducta',
        }
        for url, nombre in paginas.items():
            self.assertContains(self.client.get(url, **self.modal), f'data-form="{nombre}"', msg_prefix=url)
        # Un botón que resta se edita con la cantidad en positivo y «resta» marcado
        edicion = self.client.get(f'/profesor/comportamientos/{boton.id}/editar/', **self.modal)
        self.assertContains(edicion, 'value="negativo" checked')
        self.assertContains(edicion, 'name="monedas" value="3"')

    def test_nivel_y_mundo_se_acomodan_en_la_posicion_elegida(self):
        self.client.post('/forja/nivel/nuevo/', {'mundo': self.mundo.id, 'nombre': 'Intro', 'recompensa_cofre': 20,
                                                 'posicion': 'inicio'})
        self.assertEqual(list(Nivel.objects.filter(mundo=self.mundo).values_list('nombre', flat=True)), ['Intro', 'Nivel 1'])
        self.assertEqual(list(Nivel.objects.filter(mundo=self.mundo).values_list('orden', flat=True)), [1, 2])

        self.client.post('/profesor/mundos/nuevo/', {'clase': self.clase.id, 'nombre': 'Océano', 'tema': 'oceano',
                                                     'posicion': f'despues:{self.mundo.id}'})
        self.client.post('/profesor/mundos/nuevo/', {'clase': self.clase.id, 'nombre': 'Inicio', 'tema': 'hielo',
                                                     'posicion': 'inicio'})
        self.assertEqual(list(Mundo.objects.filter(clase=self.clase).values_list('nombre', flat=True)),
                         ['Inicio', 'Mundo 1', 'Océano'])

    def test_boton_que_resta_guarda_monedas_negativas_y_sin_xp(self):
        from .models import Comportamiento
        self.client.post('/profesor/comportamientos/nuevo/', {'nombre': 'Celular', 'icono': '📱', 'polaridad': 'negativo',
                                                               'monedas': 3, 'xp': 10, 'activo': 'on'})
        boton = Comportamiento.objects.get(nombre='Celular')
        self.assertEqual((boton.monedas, boton.xp), (-3, 0))
        respuesta = self.client.post('/profesor/comportamientos/nuevo/', {'nombre': 'Nada', 'icono': '⭐',
                                                                          'polaridad': 'positivo', 'monedas': 0, 'xp': 0})
        self.assertContains(respuesta, 'Escribe cuántas monedas da o quita')

    def test_alta_masiva_entiende_apellidos_con_coma(self):
        from .forms import separar_nombre
        self.assertEqual(separar_nombre('  Ana   López Pérez '), ('Ana', 'López Pérez'))
        self.assertEqual(separar_nombre('García Torres, María José'), ('María José', 'García Torres'))
        self.assertEqual(separar_nombre('Luis\tRuiz'), ('Luis', 'Ruiz'))
        self.client.post('/profesor/alumnos/masivo/', {'clase': self.clase.id, 'nombres': 'García Torres, María José\n\nPedro'})
        self.assertTrue(Alumno.objects.filter(nombre='María José', apellido='García Torres', clases=self.clase).exists())
        self.assertTrue(Alumno.objects.filter(nombre='Pedro', apellido='').exists())

    def test_alumno_necesita_una_clase_y_equipo_se_numera_solo(self):
        from .models import Equipo
        respuesta = self.client.post('/forja/alumno/nuevo/', {'nombre': 'Sin', 'apellido': 'Clase', 'pin': '4821', 'activo': 'on'})
        self.assertContains(respuesta, 'Elige al menos una clase')
        Equipo.objects.create(clase=self.clase, nombre='Leones', emoji='🦁', orden=1)
        self.client.post('/profesor/equipos/nuevo/', {'clase': self.clase.id, 'nombre': 'Lobos', 'emoji': '🐺', 'color': 'uva'})
        self.assertEqual(Equipo.objects.get(nombre='Lobos').orden, 2)


@override_settings(STORAGES=ALMACEN_PRUEBAS)
class MinijuegosTests(BaseJuego):
    def setUp(self):
        super().setUp()
        from .models import Juego
        self.meteoros = Juego.objects.create(nombre='Lluvia', plantilla='meteoros', monedas_arcade=5, configuracion={
            'palabras': ['monitor', 'teclado', 'mouse', 'bocina', 'cpu'], 'duracion': 60, 'velocidad': 'normal', 'meta': 10})
        self.teclado = Juego.objects.create(nombre='Teclas', plantilla='teclado', monedas_arcade=0,
                                            configuracion={'conjunto': 'central', 'rondas': 20})
        # La misión del juego va después de las dos misiones del nivel
        self.m3 = Mision.objects.create(clase=self.clase, nivel=self.nivel, nombre='Juego', descripcion='x', tipo='juego',
                                        juego=self.meteoros, orden=3, xp_recompensa=40, monedas_recompensa=20)

    def jugar(self, juego_obj, datos, mision=None, segundos=60):
        import json
        from datetime import timedelta
        from django.utils import timezone
        from .models import PartidaJuego
        inicio = self.client.post(f'/clase/{self.clase.id}/juegos/{juego_obj.id}/iniciar/',
                                  {'mision': mision.id} if mision else {})
        if inicio.status_code != 200:
            return inicio
        partida = inicio.json()['partida']
        PartidaJuego.objects.filter(pk=partida).update(inicio=timezone.now() - timedelta(seconds=segundos))
        return self.client.post(f'/clase/{self.clase.id}/juegos/partida/{partida}/terminar/',
                                json.dumps(datos), content_type='application/json')

    def test_calificacion_limita_lo_imposible(self):
        from . import minijuegos
        inflado = minijuegos.calificar_partida(self.meteoros, {'destruidos': 999, 'caracteres': 99999, 'vidas': 3}, 60)
        self.assertLessEqual(inflado['aciertos'], int(60 / (2.1 * 0.5)) + 3)
        self.assertEqual(inflado['calificacion'], 100)
        self.assertIsNone(minijuegos.calificar_partida(self.teclado, {'completadas': 20, 'aciertos': 20}, 1))
        normal = minijuegos.calificar_partida(self.teclado, {'completadas': 20, 'aciertos': 15, 'errores': 6, 'rapidas': 4}, 40)
        self.assertEqual((normal['calificacion'], normal['estrellas']), (75, 2))
        self.assertEqual(normal['puntaje'], 15 * 100 + 5 * 40 + 4 * 50)

    def test_la_mision_de_juego_se_supera_jugando_y_se_puede_mejorar(self):
        self.entrar()
        # Bloqueada hasta completar las anteriores
        self.assertEqual(self.jugar(self.meteoros, {}, mision=self.m3).status_code, 403)
        for m in (self.m1, self.m2):
            juego.calificar(ProgresoMision(alumno=self.alumno, mision=m), 100, avisar=False)
        monedas = Alumno.objects.get(pk=self.alumno.pk).monedas

        fallida = self.jugar(self.meteoros, {'destruidos': 3, 'caracteres': 18}, mision=self.m3).json()
        self.assertEqual(fallida['estrellas'], 0)
        self.assertFalse(fallida['mision']['aprobada'])

        superada = self.jugar(self.meteoros, {'destruidos': 6, 'caracteres': 36, 'vidas': 2}, mision=self.m3).json()
        self.assertTrue(superada['mision']['primera'])
        self.assertEqual((superada['estrellas'], superada['xp'], superada['monedas']), (1, 40, 12))
        progreso = ProgresoMision.objects.get(alumno=self.alumno, mision=self.m3)
        self.assertEqual((progreso.estado, progreso.puntuacion), ('aprobado', 60))

        peor = self.jugar(self.meteoros, {'destruidos': 5, 'caracteres': 30}, mision=self.m3).json()
        self.assertFalse(peor['mision']['mejoro'])
        mejor = self.jugar(self.meteoros, {'destruidos': 10, 'caracteres': 60, 'vidas': 3}, mision=self.m3).json()
        self.assertTrue(mejor['mision']['mejoro'])
        self.assertEqual((mejor['estrellas'], mejor['monedas'], mejor['xp']), (3, 8, 0))
        self.assertTrue(mejor['record'])
        # 12 por superarla + 8 al mejorar, más los bonos de subir de nivel que pudiera haber
        self.assertGreaterEqual(Alumno.objects.get(pk=self.alumno.pk).monedas, monedas + 20)

    def test_arcade_da_monedas_una_vez_al_dia_y_respeta_el_candado(self):
        self.entrar()
        self.assertContains(self.client.get(f'/clase/{self.clase.id}/dashboard/'), f'/clase/{self.clase.id}/arcade/')
        sin_premio = self.jugar(self.teclado, {'completadas': 20, 'aciertos': 19, 'errores': 1, 'rapidas': 10}, segundos=30).json()
        self.assertEqual((sin_premio['estrellas'], sin_premio['monedas']), (3, 0))  # Este juego no da monedas
        self.teclado.monedas_arcade = 5
        self.teclado.save()
        cero = self.jugar(self.teclado, {'completadas': 20, 'aciertos': 5}, segundos=30).json()
        self.assertEqual(cero['monedas'], 0)  # Sin estrellas no hay premio
        premio = self.jugar(self.teclado, {'completadas': 20, 'aciertos': 15}, segundos=30).json()
        self.assertEqual((premio['monedas'], premio.get('premio_diario')), (5, True))
        otra = self.jugar(self.teclado, {'completadas': 20, 'aciertos': 20}, segundos=30).json()
        self.assertEqual(otra['monedas'], 0)

        # «Al superar su misión»: con candado hasta aprobarla en el mapa
        self.meteoros.desbloqueo = 'mision'
        self.meteoros.save()
        self.assertEqual(self.jugar(self.meteoros, {}).status_code, 403)
        self.assertContains(self.client.get(f'/clase/{self.clase.id}/arcade/'), 'Supera su misión en el mapa')
        juego.calificar(ProgresoMision(alumno=self.alumno, mision=self.m3), 80, avisar=False)
        self.assertEqual(self.jugar(self.meteoros, {'destruidos': 8, 'caracteres': 40}).status_code, 200)
        self.assertContains(self.client.get(f'/clase/{self.clase.id}/arcade/{self.meteoros.id}/'), 'Récords')

    def test_partidas_cuentan_para_misiones_del_dia_y_logros(self):
        from .models import Logro, LogroAlumno, MisionDiaria, ProgresoDiario
        MisionDiaria.objects.update(activa=False)  # Solo esta, para que salga en el sorteo de hoy
        MisionDiaria.objects.create(titulo='Arcade', objetivo='juegos', meta=1)
        veloz = Logro.objects.create(nombre='Dedos veloces', condicion='ppm', valor=20)
        self.entrar()
        self.jugar(self.meteoros, {'destruidos': 12, 'caracteres': 150}, segundos=60)
        self.assertTrue(ProgresoDiario.objects.filter(alumno=self.alumno, mision__objetivo='juegos', progreso=1).exists())
        self.assertTrue(LogroAlumno.objects.filter(alumno=self.alumno, logro=veloz).exists())  # 150/5 = 30 ppm

    def test_profe_crea_el_juego_y_lo_pone_en_el_mapa(self):
        from .models import Juego
        self.client.force_login(User.objects.create_superuser('profe7', 'p@x.com', 'x'))
        self.assertContains(self.client.get('/profesor/juegos/nuevo/', HTTP_X_MODAL='1'), 'data-form="juego"')
        base = {'duracion': 60, 'velocidad': 'normal', 'vidas': 3, 'conjunto': 'central', 'rondas': 20, 'modo': 'guiado',
                'desbloqueo': 'libre', 'monedas_arcade': 5, 'en_arcade': 'on', 'activo': 'on'}
        respuesta = self.client.post('/profesor/juegos/nuevo/', {**base, 'plantilla': 'meteoros', 'nombre': 'Pocas',
                                                                'icono': '☄️', 'palabras': 'uno, dos'})
        self.assertContains(respuesta, 'al menos 5 palabras')
        self.client.post('/profesor/juegos/nuevo/', {
            **base, 'plantilla': 'teclado', 'nombre': 'Vocales', 'icono': '⌨️', 'conjunto': 'personalizado',
            'teclas': 'a e i o u', 'rondas': 15, 'modo': 'reto', 'desbloqueo': 'mision', 'agregar_mapa': 'on',
            'nivel_mapa': self.nivel.id, 'xp_mapa': 30, 'monedas_mapa': 10})
        vocales = Juego.objects.get(nombre='Vocales')
        self.assertEqual(vocales.configuracion['teclas'], 'AEIOU')
        mision = Mision.objects.get(juego=vocales)
        self.assertEqual((mision.tipo, mision.nivel, mision.xp_recompensa, mision.orden), ('juego', self.nivel, 30, 4))
        self.assertContains(self.client.get('/profesor/juegos/'), 'Vocales')
        self.assertContains(self.client.get(f'/forja/mision/nueva/?juego={vocales.id}', HTTP_X_MODAL='1'), 'value="juego" checked')
        # Una misión de tipo minijuego necesita su juego
        respuesta = self.client.post('/forja/mision/nueva/', {'nivel': self.nivel.id, 'nombre': 'Sin juego', 'descripcion': 'x',
                                                              'tipo': 'juego', 'xp_recompensa': 10, 'monedas_recompensa': 5})
        self.assertContains(respuesta, 'Elige el minijuego')


@override_settings(STORAGES=ALMACEN_PRUEBAS)
class DetectiveYRobotTests(BaseJuego):
    def test_detective_califica_y_limita(self):
        from . import minijuegos
        from .models import Juego
        detective = Juego.objects.create(nombre='Detective', plantilla='clasifica', configuracion={
            'rondas': 10, 'tiempo': 8, 'categorias': [
                {'nombre': 'Entrada', 'emoji': '⌨️', 'tarjetas': ['Teclado', 'Mouse', 'Micrófono', 'Escáner']},
                {'nombre': 'Salida', 'emoji': '🔊', 'tarjetas': ['Monitor', 'Bocinas', 'Impresora']}]})
        cfg = minijuegos.configuracion(detective)
        self.assertEqual(cfg['rondas'], 7)  # No puede pedir más tarjetas de las que hay
        self.assertIsNone(minijuegos.calificar_partida(detective, {'completadas': 7, 'aciertos': 7}, 1))
        r = minijuegos.calificar_partida(detective, {'completadas': 99, 'aciertos': 99, 'rapidas': 99}, 30)
        self.assertEqual((r['calificacion'], r['estrellas'], r['puntaje']), (100, 3, 7 * 150))
        r = minijuegos.calificar_partida(detective, {'completadas': 7, 'aciertos': 4, 'rapidas': 1}, 30)
        self.assertEqual((r['calificacion'], r['estrellas'], r['errores'], r['precision']), (57, 1, 3, 57))
        # Datos rotos: se usa el tema «¿Seguro o peligroso?»
        roto = Juego(nombre='Roto', plantilla='clasifica', configuracion={'categorias': [{'nombre': 'Solo uno'}]})
        self.assertEqual(len(minijuegos.configuracion(roto)['categorias']), 2)

    def test_robot_califica_y_limita(self):
        from . import minijuegos
        from .models import Juego
        robot = Juego.objects.create(nombre='Robot', plantilla='robot', configuracion={
            'dificultad': 'media', 'niveles': 3, 'modo': 'giros', 'bucles': True})
        cfg = minijuegos.configuracion(robot)
        self.assertEqual((cfg['tablero']['tam'], cfg['intentos'], cfg['modo']), (6, 3, 'giros'))
        self.assertIsNone(minijuegos.calificar_partida(robot, {'resueltos': 3}, 2))
        r = minijuegos.calificar_partida(robot, {'resueltos': 2, 'perfectos': 5, 'errores': 50}, 60)
        self.assertEqual((r['calificacion'], r['estrellas'], r['puntaje'], r['errores']), (67, 1, 2 * 150 + 2 * 75, 9))
        self.assertEqual(minijuegos.descripcion_meta(robot), 'Resuelve 3 laberintos programando al robot')

    def test_profe_crea_detective_y_robot(self):
        from .models import Juego
        self.client.force_login(User.objects.create_superuser('profe8', 'p@x.com', 'x'))
        respuesta = self.client.get('/profesor/juegos/nuevo/?plantilla=clasifica', HTTP_X_MODAL='1')
        self.assertContains(respuesta, 'data-temas-clasifica')
        self.assertContains(respuesta, 'Pedir permiso antes de descargar un juego')  # Tema listo precargado
        base = {'icono': '🎮', 'duracion': 60, 'velocidad': 'normal', 'vidas': 3, 'conjunto': 'central', 'rondas': 20,
                'modo': 'guiado', 'desbloqueo': 'libre', 'monedas_arcade': 5, 'en_arcade': 'on', 'activo': 'on'}
        incompleto = self.client.post('/profesor/juegos/nuevo/', {**base, 'plantilla': 'clasifica', 'nombre': 'Uno',
                                                                  'cat1_nombre': 'Solo', 'cat1_tarjetas': 'a\nb'})
        self.assertContains(incompleto, 'al menos 2 grupos')
        self.client.post('/profesor/juegos/nuevo/', {
            **base, 'plantilla': 'clasifica', 'nombre': 'Hardware', 'tema_clasifica': 'personalizado',
            'cat1_emoji': '🔧', 'cat1_nombre': 'Hardware', 'cat1_tarjetas': 'Teclado\nMonitor\n\nMouse',
            'cat2_emoji': '💿', 'cat2_nombre': 'Software', 'cat2_tarjetas': 'Word\nScratch', 'rondas_tarjetas': 15,
            'tiempo_tarjeta': 0})
        detective = Juego.objects.get(nombre='Hardware')
        self.assertEqual([c['tarjetas'] for c in detective.configuracion['categorias']], [['Teclado', 'Monitor', 'Mouse'], ['Word', 'Scratch']])
        self.assertEqual(detective.configuracion['tiempo'], 0)
        self.client.post('/profesor/juegos/nuevo/', {**base, 'plantilla': 'robot', 'nombre': 'Rover', 'dificultad': 'dificil',
                                                     'niveles': 8, 'modo_robot': 'giros', 'bucles': 'on'})
        self.assertEqual(Juego.objects.get(nombre='Rover').configuracion,
                         {'dificultad': 'dificil', 'niveles': 8, 'modo': 'giros', 'bucles': True})
        # Al editar, los grupos vuelven a sus campos
        edicion = self.client.get(f'/profesor/juegos/{detective.id}/editar/', HTTP_X_MODAL='1')
        self.assertContains(edicion, 'Teclado\nMonitor\nMouse')


@override_settings(STORAGES=ALMACEN_PRUEBAS)
class CuatroMinijuegosTests(BaseJuego):
    def test_configuracion_y_calificacion_por_rondas(self):
        from . import minijuegos
        from .models import Juego
        atajos = Juego(nombre='A', plantilla='atajos', configuracion={'atajos': ['copiar', 'cerrar_pestaña'], 'rondas': 10})
        self.assertEqual(minijuegos.configuracion(atajos)['atajos'], list(minijuegos.GRUPOS_ATAJOS['texto'][2]))  # 1 válido no alcanza
        mensaje = Juego(nombre='M', plantilla='mensaje', configuracion={'cifrado': 'cesar', 'palabras': ['Ratón', 'pc', 'Contraseña', 'x', 'electroencefalograma'], 'rondas': 10})
        cfg = minijuegos.configuracion(mensaje)
        self.assertEqual(cfg['palabras'], ['RATON', 'PC', 'CONTRASEÑA'])
        self.assertEqual(cfg['rondas'], 3)
        for plantilla, minimo in (('atajos', 0.4), ('mensaje', 2), ('rutas', 1.5), ('formato', 2)):
            juego_obj = Juego(nombre=plantilla, plantilla=plantilla, configuracion={'rondas': 5})
            self.assertIsNone(minijuegos.calificar_partida(juego_obj, {'completadas': 5, 'aciertos': 5}, 5 * minimo - 0.1), plantilla)
            r = minijuegos.calificar_partida(juego_obj, {'completadas': 9, 'aciertos': 9, 'perfectos': 9, 'errores': 2}, 60)
            self.assertEqual((r['calificacion'], r['estrellas'], r['puntaje'], r['precision']), (100, 3, 750, 71), plantilla)
            self.assertTrue(minijuegos.descripcion_meta(juego_obj))

    def test_jugar_atajos_en_el_arcade(self):
        import json
        from datetime import timedelta
        from django.utils import timezone
        from .models import Juego, PartidaJuego
        atajos = Juego.objects.create(nombre='Ninja', plantilla='atajos', monedas_arcade=3,
                                      configuracion={'atajos': ['copiar', 'pegar', 'guardar'], 'rondas': 10, 'modo': 'ninja'})
        self.entrar()
        pagina = self.client.get(f'/clase/{self.clase.id}/arcade/{atajos.id}/')
        self.assertContains(pagina, 'Atajos ninja')
        self.assertContains(pagina, 'situaciones')  # La configuración trae las situaciones del catálogo
        partida = self.client.post(f'/clase/{self.clase.id}/juegos/{atajos.id}/iniciar/').json()['partida']
        PartidaJuego.objects.filter(pk=partida).update(inicio=timezone.now() - timedelta(seconds=40))
        r = self.client.post(f'/clase/{self.clase.id}/juegos/partida/{partida}/terminar/',
                             json.dumps({'completadas': 10, 'aciertos': 8, 'perfectos': 6, 'errores': 3}),
                             content_type='application/json').json()
        self.assertEqual((r['estrellas'], r['puntaje'], r['monedas']), (2, 8 * 100 + 6 * 50, 3))

    def test_profe_crea_los_cuatro(self):
        from .models import Juego
        self.client.force_login(User.objects.create_superuser('profe9', 'p@x.com', 'x'))
        formulario = self.client.get('/profesor/juegos/nuevo/', HTTP_X_MODAL='1')
        for texto in ('data-bloque="atajos"', 'data-bloque="mensaje"', 'data-bloque="rutas"', 'data-bloque="formato"', 'Ctrl + C'):
            self.assertContains(formulario, texto)
        base = {'icono': '🎮', 'duracion': 60, 'velocidad': 'normal', 'vidas': 3, 'conjunto': 'central', 'rondas': 20,
                'modo': 'guiado', 'desbloqueo': 'libre', 'monedas_arcade': 5, 'en_arcade': 'on', 'activo': 'on'}
        pocos = self.client.post('/profesor/juegos/nuevo/', {**base, 'plantilla': 'atajos', 'nombre': 'X', 'atajos': ['copiar']})
        self.assertContains(pocos, 'al menos 2 atajos')
        self.client.post('/profesor/juegos/nuevo/', {**base, 'plantilla': 'atajos', 'nombre': 'Ninja', 'atajos': ['negrita', 'cursiva'],
                                                     'rondas_atajos': 15, 'modo_atajos': 'ninja'})
        self.assertEqual(Juego.objects.get(nombre='Ninja').configuracion, {'atajos': ['negrita', 'cursiva'], 'rondas': 15, 'modo': 'ninja'})
        larga = self.client.post('/profesor/juegos/nuevo/', {**base, 'plantilla': 'mensaje', 'nombre': 'M', 'cifrado': 'binario',
                                                             'palabras_mensaje': 'robot\nmotor\nelectroencefalograma'})
        self.assertContains(larga, 'Máximo 12 letras')
        self.client.post('/profesor/juegos/nuevo/', {**base, 'plantilla': 'mensaje', 'nombre': 'Secreto', 'cifrado': 'cesar',
                                                     'palabras_mensaje': 'Ratón, Contraseña\nrobot', 'rondas_mensaje': 8, 'desplazamiento': 5})
        self.assertEqual(Juego.objects.get(nombre='Secreto').configuracion['palabras'], ['RATON', 'CONTRASEÑA', 'ROBOT'])
        self.client.post('/profesor/juegos/nuevo/', {**base, 'plantilla': 'rutas', 'nombre': 'Rutas', 'modo_rutas': 'buscar',
                                                     'dificultad_rutas': 'dificil', 'rondas_rutas': 8})
        self.assertEqual(Juego.objects.get(nombre='Rutas').configuracion, {'modo': 'buscar', 'dificultad': 'dificil', 'rondas': 8})
        mal = self.client.post('/profesor/juegos/nuevo/', {**base, 'plantilla': 'formato', 'nombre': 'F', 'frases': 'una sola frase aquí'})
        self.assertContains(mal, 'al menos 3 frases')
        self.client.post('/profesor/juegos/nuevo/', {**base, 'plantilla': 'formato', 'nombre': 'Formato', 'dificultad_formato': 'dificil'})
        formato = Juego.objects.get(nombre='Formato')
        self.assertEqual(formato.configuracion['frases'], [])
        self.assertContains(self.client.get(f'/profesor/juegos/{formato.id}/editar/', HTTP_X_MODAL='1'), 'value="dificil"')

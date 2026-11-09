/* =========================================================
   NEXT-LEVEL · Bandeja de revisiones
   Calificar sin recargar, deshacer, aprobar una misión completa,
   entregas nuevas en vivo y la «Revisión rápida» (una a la vez).
   ========================================================= */
(function () {
    'use strict';
    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
    const fuente = document.getElementById('rv-entregas');
    if (!fuente) return;

    const ESPERA_DESHACER = 4500;   // ms para arrepentirse antes de que se guarde
    const CADA_NUEVAS = 30000;      // ms entre cada búsqueda de entregas nuevas
    const config = $('[data-rv-config]');
    const motivos = JSON.parse(document.getElementById('rv-motivos').textContent);
    const toast = (texto, icono = 'success') => window.PToast && window.PToast(texto, icono);

    // Cada entrega con su estado en esta página:
    //   null = por revisar · 'decidida' = esperando el «deshacer» · 'enviando' · 'lista' = ya guardada
    const entregas = JSON.parse(fuente.textContent).map(e => ({ ...e, estado: null }));
    const porId = new Map(entregas.map(e => [e.id, e]));
    const enVuelo = new Set();

    const csrf = () => $('[name=csrfmiddlewaretoken]')?.value || '';
    const tarjeta = e => $(`[data-entrega="${e.id}"]`);
    const nota = n => Number(n).toLocaleString('es-MX', { maximumFractionDigits: 1 });
    const plural = (n, uno, varios) => `${n} ${n === 1 ? uno : varios}`;
    const normalizar = t => (t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');

    // ---------- Búsqueda (también filtra la revisión rápida) ----------
    const buscador = $('[data-rv-buscar]');
    function coincide(e) {
        const q = normalizar(buscador?.value.trim());
        if (!q) return true;
        return normalizar(`${e.alumno.nombre} ${e.alumno.apellido} ${e.mision.nombre} ${e.clase.nombre}`).includes(q);
    }
    const porRevisar = () => entregas.filter(e => e.estado === null && coincide(e));

    // Las direcciones en las respuestas escritas se pueden abrir
    function enlazar(nodo, texto) {
        nodo.textContent = '';
        String(texto || '').split(/(https?:\/\/[^\s<>"]+)/g).forEach((parte, i) => {
            if (i % 2) {
                const a = document.createElement('a');
                a.href = parte; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = parte;
                nodo.append(a);
            } else if (parte) {
                nodo.append(parte);
            }
        });
    }
    $$('[data-enlazar]').forEach(n => enlazar(n, n.textContent));

    // =====================================================
    // Decidir → unos segundos para deshacer → guardar
    // =====================================================
    let enEspera = null;   // { entrega, accion, datos, timer }
    const barra = $('[data-rv-deshacer]');

    function decidir(entrega, accion, datos) {
        guardarEnEspera();   // la decisión anterior ya no se puede deshacer: se guarda en este momento
        entrega.estado = 'decidida';
        const texto = accion === 'aprobar'
            ? `${entrega.alumno.nombre}: aprobada con ${nota(datos.calificacion)}`
            : `${entrega.alumno.nombre}: devuelta para corregir`;
        enEspera = { entrega, accion, datos, timer: setTimeout(guardarEnEspera, ESPERA_DESHACER) };
        marcarTarjeta(entrega, accion === 'aprobar' ? `Aprobada con ${nota(datos.calificacion)}` : 'Devuelta para corregir', accion);
        $('[data-rv-deshacer-texto]', barra).textContent = texto;
        barra.hidden = false;
        barra.classList.remove('corriendo');
        void barra.offsetWidth;   // reinicia la barrita del tiempo
        barra.classList.add('corriendo');
        actualizarVista();
    }

    function deshacer() {
        if (!enEspera) return false;
        clearTimeout(enEspera.timer);
        const { entrega } = enEspera;
        enEspera = null;
        barra.hidden = true;
        entrega.estado = null;
        desmarcarTarjeta(entrega);
        rapida.alDeshacer(entrega);
        actualizarVista();
        return true;
    }

    function guardarEnEspera(keepalive = false) {
        if (!enEspera) return Promise.resolve();
        const { entrega, accion, datos, timer } = enEspera;
        clearTimeout(timer);
        enEspera = null;
        barra.hidden = true;
        entrega.estado = 'enviando';
        const body = new FormData();
        body.append('csrfmiddlewaretoken', csrf());
        Object.entries(datos).forEach(([k, v]) => body.append(k, v));
        const peticion = fetch(accion === 'aprobar' ? entrega.aprobar : entrega.rechazar, {
            method: 'POST', body, keepalive, credentials: 'same-origin',
            headers: { 'X-CSRFToken': csrf(), 'X-Requested-With': 'XMLHttpRequest' },
        }).then(r => r.json()).then(j => {
            if (!j.ok && !j.ya_revisada) throw new Error(j.mensaje);
            entrega.estado = 'lista';
            if (!j.ok) toast(j.mensaje, 'info');   // ya la había calificado alguien más (otro dispositivo)
            quitarTarjeta(entrega);
            if (j.revisada) agregarReciente(j.revisada);
            actualizarContadores(j);
        }).catch(() => {
            entrega.estado = null;
            desmarcarTarjeta(entrega);
            toast(`No se guardó la revisión de ${entrega.alumno.nombre}. Revisa tu conexión e inténtalo otra vez.`, 'error');
        }).finally(() => {
            enVuelo.delete(peticion);
            actualizarVista();
        });
        enVuelo.add(peticion);
        return peticion;
    }
    async function guardarTodo() {
        await guardarEnEspera();
        await Promise.allSettled([...enVuelo]);
    }
    // Si el profe se va (cambia de app en el celular o cierra la pestaña), lo decidido se guarda igual
    window.addEventListener('pagehide', () => guardarEnEspera(true));
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') guardarEnEspera(true);
    });
    $('[data-rv-deshacer-btn]').addEventListener('click', deshacer);

    // ---------- Tarjetas de la lista ----------
    function marcarTarjeta(e, texto, accion) {
        const t = tarjeta(e);
        if (!t) return;
        t.classList.remove('aprobada', 'devuelta');
        t.classList.add('decidida', accion === 'aprobar' ? 'aprobada' : 'devuelta');
        const aviso = $('.entrega-decidida', t);
        aviso.replaceChildren();
        const i = document.createElement('i');
        i.className = `bi ${accion === 'aprobar' ? 'bi-check-circle-fill' : 'bi-arrow-counterclockwise'}`;
        aviso.append(i, ` ${texto}`);
    }
    function desmarcarTarjeta(e) {
        tarjeta(e)?.classList.remove('decidida', 'aprobada', 'devuelta', 'saliendo');
    }
    function quitarTarjeta(e) {
        const t = tarjeta(e);
        if (!t) return;
        t.classList.add('saliendo');
        setTimeout(() => { t.remove(); actualizarVista(); }, 280);
    }

    $$('[data-entrega]').forEach(t => {
        const e = porId.get(Number(t.dataset.entrega));
        if (!e) return;
        const comentario = () => $('[name=comentario]', t).value.trim();
        $$('[data-calif]', t).forEach(b => b.addEventListener('click', () => {
            decidir(e, 'aprobar', { calificacion: b.dataset.calif, comentario: comentario() });
        }));
        const otra = $('[name=calificacion]', t);
        const aprobarOtra = () => {
            const n = parseFloat(String(otra.value).replace(',', '.'));
            if (Number.isNaN(n) || n < 0 || n > 10) { toast('Escribe una calificación de 0 a 10', 'warning'); otra.focus(); return; }
            decidir(e, 'aprobar', { calificacion: n, comentario: comentario() });
        };
        $('[data-calif-otra]', t).addEventListener('click', aprobarOtra);
        otra.addEventListener('keydown', ev => { if (ev.key === 'Enter') { ev.preventDefault(); aprobarOtra(); } });
        $('[data-devolver]', t).addEventListener('click', () => pedirMotivo(e));
    });

    async function pedirMotivo(e) {
        const r = await Swal.fire({
            title: `Devolver «${e.mision.nombre}»`,
            html: '<div class="rv-frases rv-frases-swal"></div>',
            input: 'textarea',
            inputLabel: `Explícale a ${e.alumno.nombre} qué debe corregir:`,
            inputPlaceholder: 'Ej. Revisa la conexión del LED, está al revés 🙂',
            didOpen: () => {
                const caja = $('.rv-frases', Swal.getHtmlContainer());
                motivos.forEach(m => {
                    const b = document.createElement('button');
                    b.type = 'button'; b.className = 'rv-frase'; b.textContent = m;
                    b.addEventListener('click', () => { Swal.getInput().value = m; Swal.getInput().focus(); });
                    caja.append(b);
                });
            },
            showCancelButton: true, reverseButtons: true, buttonsStyling: false,
            confirmButtonText: 'Devolver al alumno', cancelButtonText: 'Cancelar',
            customClass: { popup: 'swal-p', confirmButton: 'p-btn peligro-lleno', cancelButton: 'p-btn' },
        });
        if (r.isConfirmed) decidir(e, 'rechazar', { comentario: (r.value || '').trim() });
    }

    // ---------- Aprobar todas las de una misión («Por misión») ----------
    $$('[data-rv-aprobar-grupo]').forEach(btn => btn.addEventListener('click', async () => {
        const mision = Number(btn.dataset.rvAprobarGrupo);
        const lista = entregas.filter(e => e.mision.id === mision && e.estado === null);
        if (!lista.length) return;
        await guardarEnEspera();
        const r = await Swal.fire({
            title: lista.length === 1 ? 'Aprobar la entrega' : `Aprobar las ${lista.length} entregas`,
            text: `De «${btn.dataset.nombre}». Todos reciben la misma calificación, su XP y sus monedas.`,
            input: 'select',
            inputOptions: new Map(['10', '9', '8', '7', '6', '5'].map(n => [n, n])),   // Map: respeta el orden 10 → 5
            inputValue: '10',
            inputLabel: 'Calificación',
            showCancelButton: true, reverseButtons: true, buttonsStyling: false,
            confirmButtonText: lista.length === 1 ? 'Aprobar' : `Aprobar las ${lista.length}`, cancelButtonText: 'Cancelar',
            customClass: { popup: 'swal-p', confirmButton: 'p-btn primario', cancelButton: 'p-btn' },
        });
        if (!r.isConfirmed) return;
        lista.forEach(e => { e.estado = 'enviando'; marcarTarjeta(e, `Aprobando con ${nota(r.value)}…`, 'aprobar'); });
        actualizarVista();
        const body = new FormData();
        body.append('csrfmiddlewaretoken', csrf());
        body.append('calificacion', r.value);
        lista.forEach(e => body.append('ids', e.id));
        try {
            const respuesta = await fetch(config.dataset.varias, {
                method: 'POST', body, credentials: 'same-origin',
                headers: { 'X-CSRFToken': csrf(), 'X-Requested-With': 'XMLHttpRequest' },
            });
            const j = await respuesta.json();
            if (!j.ok) throw new Error(j.mensaje);
            lista.forEach(e => { e.estado = 'lista'; quitarTarjeta(e); });
            actualizarContadores(j);
            toast(j.mensaje);
        } catch (err) {
            lista.forEach(e => { e.estado = null; desmarcarTarjeta(e); });
            toast('No se pudieron aprobar. Revisa tu conexión e inténtalo otra vez.', 'error');
        }
        actualizarVista();
    }));

    // ---------- Contadores, grupos y «Revisadas recientemente» ----------
    function ponerCuenta(contenedor, n, clase) {
        if (!contenedor) return;
        let c = $(`.${clase.split(' ')[0]}`, contenedor);
        if (!n) { c?.remove(); return; }
        if (!c) { c = document.createElement('span'); c.className = clase; contenedor.append(' ', c); }
        c.textContent = n;
    }
    function actualizarContadores(j) {
        if (typeof j.pendientes !== 'number') return;
        ponerCuenta($('.sidebar-nav a[href$="/profesor/revisiones/"]'), j.pendientes, 'cuenta');
        $$('[data-chip-clase]').forEach(chip => ponerCuenta(chip, j.por_clase?.[chip.dataset.chipClase] || 0, 'c'));
    }
    function agregarReciente(r) {
        const lista = $('[data-rv-recientes]');
        $('[data-rv-recientes-vacio]', lista)?.remove();
        const fila = document.createElement('div');
        fila.className = 'feed-item rv-nueva';
        const img = document.createElement('img');
        img.src = r.avatar; img.alt = ''; img.style.cssText = 'width:30px;height:30px;border-radius:50%';
        const cuerpo = document.createElement('div');
        cuerpo.className = 'min-w-0';
        const t = document.createElement('div');
        t.className = 't text-truncate';
        const b = document.createElement('b');
        b.textContent = r.alumno;
        t.append(b, ` · ${r.mision}`);
        const f = document.createElement('div');
        f.className = 'f'; f.textContent = 'justo ahora';
        cuerpo.append(t, f);
        const v = document.createElement('span');
        v.className = 'v';
        const insignia = document.createElement('span');
        insignia.className = r.estado === 'aprobado' ? 'p-badge verde tnum' : 'p-badge rojo';
        insignia.textContent = r.estado === 'aprobado' ? r.calificacion : 'Devuelta';
        v.append(insignia);
        fila.append(img, cuerpo, v);
        lista.prepend(fila);
        $$('.feed-item', lista).slice(8).forEach(x => x.remove());
    }

    function actualizarVista() {
        const quedan = entregas.filter(e => e.estado !== 'lista').length;
        // Encabezado
        const resumen = $('[data-resumen]');
        if (resumen) {
            resumen.replaceChildren();
            if (quedan) {
                const b = document.createElement('b');
                b.textContent = quedan;
                resumen.append(b, ` ${quedan === 1 ? 'entrega esperando' : 'entregas esperando'} tu calificación${resumen.dataset.en || ''}.`);
            } else {
                resumen.textContent = 'Todo al día.';
            }
        }
        $$('[data-rv-abrir]').forEach(b => { if (!b.dataset.rvAbrir) b.disabled = !porRevisar().length; });
        // Grupos por misión
        $$('[data-rv-grupo]').forEach(g => {
            const id = Number(g.dataset.rvGrupo);
            const suyas = entregas.filter(e => e.mision.id === id && e.estado !== 'lista' && tarjeta(e));
            const libres = suyas.filter(e => e.estado === null).length;
            const visibles = suyas.filter(e => !tarjeta(e).classList.contains('d-none')).length;
            g.hidden = !suyas.length || !visibles;
            $('[data-rv-grupo-cuenta]', g).textContent = plural(suyas.length, 'entrega', 'entregas');
            const boton = $('[data-rv-aprobar-grupo]', g);
            boton.disabled = !libres;
            $('span', boton).textContent = libres > 1 ? `Aprobar las ${libres}` : 'Aprobar';
        });
        // Lista vacía
        const vacio = $('[data-rv-vacio]');
        if (vacio) vacio.hidden = Boolean($('[data-entrega]'));
        // Entregas que llegaron y todavía no están en la lista
        const nuevas = entregas.filter(e => e.nueva && e.estado === null && !tarjeta(e));
        const aviso = $('[data-rv-aviso]');
        aviso.hidden = !nuevas.length;
        $('[data-rv-aviso-texto]', aviso).textContent = nuevas.length === 1
            ? `Llegó una entrega nueva de ${nuevas[0].alumno.nombre}.`
            : `Llegaron ${nuevas.length} entregas nuevas.`;
        rapida.pintarAvance();
    }

    buscador?.addEventListener('input', () => {
        $$('[data-entrega]').forEach(t => {
            const e = porId.get(Number(t.dataset.entrega));
            t.classList.toggle('d-none', Boolean(e) && !coincide(e));
        });
        actualizarVista();
    });

    $('[data-rv-actualizar]').addEventListener('click', async ev => {
        ev.currentTarget.disabled = true;
        await guardarTodo();
        location.reload();
    });

    // ---------- Entregas nuevas en vivo ----------
    async function buscarNuevas() {
        if (document.visibilityState !== 'visible') return;
        const params = new URLSearchParams({ conocidas: entregas.filter(e => e.estado !== 'lista').map(e => e.id).join(',') });
        if (config.dataset.clase) params.set('clase', config.dataset.clase);
        if (config.dataset.tipo) params.set('tipo', config.dataset.tipo);
        try {
            const r = await fetch(`${config.dataset.nuevas}?${params}`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
            const j = await r.json();
            const llegaron = j.entregas || [];
            llegaron.forEach(n => {
                const previa = porId.get(n.id);
                if (previa) {
                    Object.assign(previa, n, { estado: null, nueva: true });   // la devolvió y ya la corrigió
                } else {
                    const e = { ...n, estado: null, nueva: true };
                    entregas.push(e);
                    porId.set(e.id, e);
                }
            });
            if (llegaron.length) {
                if (rapida.abierta()) {
                    toast(llegaron.length === 1 ? `Llegó la entrega de ${llegaron[0].alumno.nombre}` : `Llegaron ${llegaron.length} entregas nuevas`, 'info');
                }
                actualizarVista();
            }
        } catch (err) { /* sin conexión: se intenta en la siguiente vuelta */ }
    }
    setInterval(buscarNuevas, CADA_NUEVAS);

    // =====================================================
    // Revisión rápida: una entrega a la vez, en grande
    // =====================================================
    const rapida = (() => {
        const raiz = $('#revision-rapida');
        const deshacerBarra = barra;
        document.body.append(raiz, deshacerBarra);   // fuera del panel, para poder bloquear lo de atrás
        const fondo = [$('.sidebar'), $('.main')].filter(Boolean);
        let actual = null;
        let revisadas = 0;
        let foco = null;
        const abierta = () => !raiz.hidden;
        const modoDevolver = () => !$('[data-rv-modo-devolver]', raiz).hidden;

        function siguienteDe(e, paso = 1) {
            const orden = entregas.filter(coincide);
            const n = orden.length;
            const i = orden.indexOf(e);
            for (let k = 1; k <= n; k++) {
                const c = orden[(((i + paso * k) % n) + n) % n];
                if (c.estado === null) return c;
            }
            return null;
        }

        function abrir(desde) {
            const cola = porRevisar();
            if (!cola.length) { toast('No hay entregas por revisar', 'info'); return; }
            foco = document.activeElement;
            actual = desde && cola.includes(desde) ? desde : cola[0];
            revisadas = 0;
            raiz.hidden = false;
            document.body.classList.add('rv-abierta');
            fondo.forEach(n => { n.inert = true; });
            pintar();
            $('[data-rv-cerrar]', raiz).focus();
        }
        function cerrar() {
            raiz.hidden = true;
            document.body.classList.remove('rv-abierta');
            fondo.forEach(n => { n.inert = false; });
            foco?.focus?.();
            actualizarVista();
        }

        function pintarAvance() {
            if (!abierta()) return;
            const cola = porRevisar();
            const pos = actual ? cola.indexOf(actual) + 1 : cola.length;
            $('[data-rv-pos]', raiz).textContent = Math.max(pos, 1);
            $('[data-rv-cuantas]', raiz).textContent = cola.length;
            $('[data-rv-hechas]', raiz).textContent = revisadas ? `· ${plural(revisadas, 'revisada', 'revisadas')}` : '';
            $('[data-rv-barra]', raiz).style.width = `${revisadas + cola.length ? Math.round(revisadas * 100 / (revisadas + cola.length)) : 100}%`;
            $('.rv-avance-texto', raiz).hidden = !actual;
        }

        function pintar() {
            if (actual && actual.estado !== null) actual = siguienteDe(actual);
            if (!actual) actual = porRevisar()[0] || null;
            const fin = !actual;
            $('[data-rv-cuerpo]', raiz).hidden = fin;
            $('.rv-nav', raiz).hidden = fin;
            $('[data-rv-final]', raiz).hidden = !fin;
            pintarAvance();
            if (fin) {
                $('[data-rv-final-texto]', raiz).textContent = revisadas
                    ? `Revisaste ${plural(revisadas, 'entrega', 'entregas')}. ¡Buen trabajo, profe!`
                    : 'No quedan entregas por revisar.';
                $('[data-rv-final] [data-rv-cerrar]', raiz).focus();
                return;
            }
            const e = actual;
            const alumno = $('[data-rv-alumno]', raiz);
            alumno.href = e.alumno.url;
            $('[data-rv-avatar]', raiz).src = e.alumno.avatar;
            $('[data-rv-nombre]', raiz).textContent = `${e.alumno.nombre} ${e.alumno.apellido}`;
            $('[data-rv-sub]', raiz).textContent = `${e.clase.nombre} · hace ${e.hace}${e.intentos > 1 ? ` · intento ${e.intentos}` : ''}`;
            const tipo = $('[data-rv-tipo]', raiz);
            tipo.textContent = `${e.mision.emoji} ${e.mision.tipo}`;
            tipo.style.cssText = `background:${e.mision.color}1a;color:${e.mision.color};border-color:transparent`;
            $('[data-rv-mision]', raiz).textContent = e.mision.nombre;
            $('[data-rv-ruta]', raiz).textContent = `${e.mision.ruta} · +${e.mision.xp} XP · hasta ${e.mision.monedas} monedas`;
            const pediste = $('[data-rv-pediste]', raiz);
            pediste.hidden = !e.comentario_anterior;
            pediste.textContent = e.comentario_anterior ? `Le pediste corregir: «${e.comentario_anterior}»` : '';

            // Evidencia: la foto en grande (clic = tamaño real), la respuesta escrita o un aviso
            const caja = $('[data-rv-evidencia]', raiz);
            caja.replaceChildren();
            caja.classList.remove('zoom');
            caja.scrollTop = 0;
            if (e.evidencia) {
                const img = document.createElement('img');
                img.src = e.evidencia;
                img.alt = `Evidencia de ${e.alumno.nombre}`;
                img.title = 'Clic para ver en tamaño real';
                img.addEventListener('click', () => caja.classList.toggle('zoom'));
                caja.append(img);
            }
            if (e.texto) {
                const texto = document.createElement('div');
                texto.className = 'rv-texto';
                enlazar(texto, e.texto);
                caja.append(texto);
            }
            if (!e.evidencia && !e.texto) {
                const vacio = document.createElement('div');
                vacio.className = 'rv-sin-evidencia';
                const i = document.createElement('i');
                i.className = 'bi bi-check2-square';
                const p = document.createElement('p');
                p.textContent = `${e.alumno.nombre} marcó la misión como terminada sin adjuntar evidencia.`;
                vacio.append(i, p);
                caja.append(vacio);
            }
            caja.classList.toggle('con-foto', Boolean(e.evidencia));
            caja.classList.toggle('con-texto', Boolean(e.evidencia && e.texto));

            $('[data-rv-comentario]', raiz).value = '';
            $('[data-rv-motivo-texto]', raiz).value = '';
            mostrarDevolver(false);
            // La foto que sigue se va cargando desde ya
            const despues = siguienteDe(e);
            if (despues?.evidencia) new Image().src = despues.evidencia;
        }

        function mostrarDevolver(si) {
            $('[data-rv-modo-aprobar]', raiz).hidden = si;
            $('[data-rv-modo-devolver]', raiz).hidden = !si;
            if (si) $('[data-rv-motivo-texto]', raiz).focus();
        }
        function calificar(n) {
            if (!actual || modoDevolver()) return;
            const e = actual;
            decidir(e, 'aprobar', { calificacion: n, comentario: $('[data-rv-comentario]', raiz).value.trim() });
            revisadas += 1;
            actual = siguienteDe(e);
            pintar();
        }
        function devolver() {
            if (!actual) return;
            const e = actual;
            decidir(e, 'rechazar', { comentario: $('[data-rv-motivo-texto]', raiz).value.trim() });
            revisadas += 1;
            actual = siguienteDe(e);
            pintar();
        }
        function mover(paso) {
            if (!actual) return;
            actual = siguienteDe(actual, paso) || actual;
            pintar();
        }

        $$('[data-rv-abrir]').forEach(b => b.addEventListener('click', () => abrir(porId.get(Number(b.dataset.rvAbrir)))));
        $$('[data-rv-cerrar]', raiz).forEach(b => b.addEventListener('click', cerrar));
        $$('[data-rv-nota]', raiz).forEach(b => b.addEventListener('click', () => calificar(Number(b.dataset.rvNota))));
        $('[data-rv-saltar]', raiz).addEventListener('click', () => mover(1));
        $('[data-rv-anterior]', raiz).addEventListener('click', () => mover(-1));
        $('[data-rv-devolver]', raiz).addEventListener('click', () => mostrarDevolver(true));
        $('[data-rv-cancelar-devolver]', raiz).addEventListener('click', () => mostrarDevolver(false));
        $('[data-rv-confirmar-devolver]', raiz).addEventListener('click', devolver);
        $$('[data-rv-frase]', raiz).forEach(b => b.addEventListener('click', () => {
            $('[data-rv-comentario]', raiz).value = b.textContent;
        }));
        $$('[data-rv-motivo]', raiz).forEach(b => b.addEventListener('click', () => {
            const caja = $('[data-rv-motivo-texto]', raiz);
            caja.value = b.textContent;
            caja.focus();
        }));

        document.addEventListener('keydown', ev => {
            if (!abierta()) {
                if (ev.key.toLowerCase() === 'z' && !ev.target.matches('input, textarea, select') && !ev.ctrlKey && !ev.metaKey && deshacer()) ev.preventDefault();
                return;
            }
            if (ev.key === 'Escape') {
                ev.preventDefault();
                if (modoDevolver()) mostrarDevolver(false); else cerrar();
                return;
            }
            if (ev.target.matches('input, textarea, select')) {
                // Ctrl+Enter en el motivo = devolver
                if (ev.key === 'Enter' && (ev.ctrlKey || ev.metaKey) && ev.target.matches('[data-rv-motivo-texto]')) { ev.preventDefault(); devolver(); }
                else if (ev.key === 'Enter' && ev.target.matches('[data-rv-comentario]')) ev.preventDefault();
                return;
            }
            if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
            const tecla = ev.key.toLowerCase();
            if (/^[0-9]$/.test(tecla)) { ev.preventDefault(); calificar(tecla === '0' ? 10 : Number(tecla)); }
            else if (tecla === 'd') { ev.preventDefault(); mostrarDevolver(true); }
            else if (tecla === 'arrowright') { ev.preventDefault(); mover(1); }
            else if (tecla === 'arrowleft') { ev.preventDefault(); mover(-1); }
            else if (tecla === 'z') { ev.preventDefault(); deshacer(); }
        });

        return {
            abierta,
            pintarAvance,
            alDeshacer(e) {
                if (!abierta()) return;
                revisadas = Math.max(0, revisadas - 1);
                actual = e;
                pintar();
            },
        };
    })();

    actualizarVista();
})();

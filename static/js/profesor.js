/* =========================================================
   NEXT-LEVEL · Interacciones del panel del profesor
   ========================================================= */
(function () {
    'use strict';
    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

    function csrf() {
        const input = $('[name=csrfmiddlewaretoken]');
        return input ? input.value : '';
    }
    async function post(url, datos = {}) {
        const body = new FormData();
        Object.entries(datos).forEach(([k, v]) => body.append(k, v));
        const r = await fetch(url, { method: 'POST', body, headers: { 'X-CSRFToken': csrf(), 'X-Requested-With': 'XMLHttpRequest' } });
        if (!r.ok) throw new Error('Error ' + r.status);
        return r.json();
    }

    // ---------- Toasts ----------
    function toast(titulo, icono = 'success') {
        if (typeof Swal === 'undefined') return;
        Swal.fire({
            toast: true, position: 'bottom-end', showConfirmButton: false, timer: 3200, timerProgressBar: true,
            icon: icono, title: titulo, customClass: { popup: 'swal-p-toast' },
        });
    }
    window.PToast = toast;

    function confirmar({ titulo, texto, boton = 'Confirmar', peligro = false }) {
        if (typeof Swal === 'undefined') return Promise.resolve(window.confirm(texto || titulo));
        return Swal.fire({
            title: titulo, text: texto, showCancelButton: true, reverseButtons: true, buttonsStyling: false,
            confirmButtonText: boton, cancelButtonText: 'Cancelar',
            customClass: { popup: 'swal-p', confirmButton: peligro ? 'p-btn peligro-lleno' : 'p-btn primario', cancelButton: 'p-btn' },
        }).then(r => r.isConfirmed);
    }
    window.PConfirmar = confirmar;

    // ---------- Tema claro / oscuro ----------
    function iniciarTema() {
        const btn = $('#btn-tema');
        if (!btn) return;
        btn.addEventListener('click', () => {
            const oscuro = document.documentElement.dataset.theme !== 'dark';
            document.documentElement.dataset.theme = oscuro ? 'dark' : 'light';
            document.documentElement.dataset.bsTheme = oscuro ? 'dark' : 'light';
            try { localStorage.setItem('nl-tema-profe', oscuro ? 'dark' : 'light'); } catch (e) { /* sin almacenamiento */ }
        });
    }

    // ---------- Menú lateral en móvil ----------
    function iniciarMenu() {
        $('.btn-menu')?.addEventListener('click', () => document.body.classList.toggle('menu-abierto'));
        $('.velo')?.addEventListener('click', () => document.body.classList.remove('menu-abierto'));
    }

    // ---------- Formularios con confirmación ----------
    function iniciarConfirmaciones() {
        document.addEventListener('submit', async e => {
            const form = e.target;
            if (form.dataset.confirmado === '1') return;

            if (form.matches('[data-confirmar]')) {
                e.preventDefault();
                const ok = await confirmar({
                    titulo: form.dataset.titulo || '¿Estás seguro?',
                    texto: form.dataset.confirmar,
                    boton: form.dataset.boton || 'Sí, continuar',
                    peligro: form.hasAttribute('data-peligro'),
                });
                if (ok) { form.dataset.confirmado = '1'; form.submit(); }
            } else if (form.matches('[data-pedir-comentario]')) {
                e.preventDefault();
                const r = await Swal.fire({
                    title: form.dataset.titulo || 'Devolver para corrección',
                    input: 'textarea',
                    inputLabel: form.dataset.pedirComentario,
                    inputPlaceholder: 'Ej. Revisa la conexión del LED, está al revés 🙂',
                    showCancelButton: true, reverseButtons: true, buttonsStyling: false,
                    confirmButtonText: 'Devolver al alumno', cancelButtonText: 'Cancelar',
                    customClass: { popup: 'swal-p', confirmButton: 'p-btn peligro-lleno', cancelButton: 'p-btn' },
                });
                if (r.isConfirmed) {
                    form.querySelector('[name=comentario]').value = r.value || '';
                    form.dataset.confirmado = '1';
                    form.submit();
                }
            }
        });
    }

    // ---------- Calificación rápida ----------
    function iniciarCalificacion() {
        $$('[data-calif]').forEach(btn => btn.addEventListener('click', () => {
            const form = btn.closest('form');
            form.querySelector('[name=calificacion]').value = btn.dataset.calif;
            form.dataset.confirmado = '1';
            form.submit();
        }));
        $$('img[data-ampliar]').forEach(img => img.addEventListener('click', () => {
            Swal.fire({ imageUrl: img.dataset.ampliar, imageAlt: 'Evidencia', showConfirmButton: false, showCloseButton: true,
                width: 'min(900px, 95vw)', customClass: { popup: 'swal-p' } });
        }));
    }

    // ---------- Búsqueda en tablas y listas ----------
    function normalizar(t) { return (t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
    function iniciarBusqueda() {
        $$('[data-buscar]').forEach(input => {
            const objetivo = $(input.dataset.buscar);
            if (!objetivo) return;
            const filas = $$(input.dataset.filas || 'tbody tr', objetivo);
            const contador = input.dataset.contador ? $(input.dataset.contador) : null;
            input.addEventListener('input', () => {
                const q = normalizar(input.value.trim());
                let visibles = 0;
                filas.forEach(fila => {
                    const ok = normalizar(fila.textContent).includes(q);
                    fila.classList.toggle('d-none', !ok);
                    if (ok) visibles += 1;
                });
                if (contador) contador.textContent = visibles;
            });
        });
    }

    // ---------- Interruptores AJAX ----------
    function iniciarInterruptores() {
        $$('[data-alternar-url]').forEach(sw => sw.addEventListener('change', async () => {
            try {
                const r = await post(sw.dataset.alternarUrl);
                sw.checked = r.activo;
                sw.closest('tr')?.classList.toggle('fila-inactiva', !r.activo);
                toast(r.activo ? 'Activado' : 'Desactivado');
            } catch (e) {
                sw.checked = !sw.checked;
                toast('No se pudo guardar el cambio', 'error');
            }
        }));
    }

    // ---------- Stock ----------
    function iniciarStock() {
        $$('[data-stock-url]').forEach(btn => btn.addEventListener('click', async () => {
            try {
                const r = await post(btn.dataset.stockUrl, { accion: btn.dataset.accion, cantidad: 1 });
                const celda = document.getElementById(btn.dataset.objetivo);
                if (celda) celda.textContent = r.stock === null ? '∞' : r.stock;
                const fila = btn.closest('tr');
                fila?.querySelector('.alerta-stock')?.classList.toggle('d-none', !(r.stock !== null && r.stock <= 3));
            } catch (e) { toast('No se pudo actualizar el stock', 'error'); }
        }));
    }

    // ---------- Tooltip de la gráfica ----------
    function iniciarGrafica() {
        const grafica = $('.grafica');
        if (!grafica) return;
        const tip = $('.tooltip-g', grafica);
        const mostrar = grupo => {
            tip.replaceChildren();
            const f = document.createElement('div');
            f.className = 'f';
            f.textContent = grupo.dataset.fecha;
            tip.appendChild(f);
            [['s1', 'Entregas', grupo.dataset.entregas], ['s2', 'Aprobadas', grupo.dataset.aprobadas]].forEach(([clase, nombre, valor]) => {
                const fila = document.createElement('div');
                fila.className = 'r';
                const key = document.createElement('i');
                key.style.background = `var(--series-${clase === 's1' ? 1 : 2})`;
                const b = document.createElement('b');
                b.textContent = valor;
                const s = document.createElement('span');
                s.textContent = nombre;
                fila.append(key, b, s);
                tip.appendChild(fila);
            });
            const caja = grafica.getBoundingClientRect();
            const r = grupo.getBoundingClientRect();
            let x = r.left - caja.left + r.width / 2 - 70;
            x = Math.max(0, Math.min(x, caja.width - 150));
            tip.style.left = x + 'px';
            tip.style.top = Math.max(0, r.top - caja.top - 10) + 'px';
            tip.classList.add('visible');
        };
        $$('.grupo', grafica).forEach(g => {
            g.addEventListener('pointerenter', () => mostrar(g));
            g.addEventListener('focus', () => mostrar(g));
            g.addEventListener('pointerleave', () => tip.classList.remove('visible'));
            g.addEventListener('blur', () => tip.classList.remove('visible'));
        });
        $('#ver-tabla-actividad')?.addEventListener('click', e => {
            const tabla = $('#tabla-actividad');
            tabla.classList.toggle('d-none');
            e.currentTarget.textContent = tabla.classList.contains('d-none') ? 'Ver como tabla' : 'Ocultar tabla';
        });
    }

    // ---------- Copiar ----------
    function iniciarCopiar() {
        $$('[data-copiar]').forEach(btn => btn.addEventListener('click', async () => {
            try { await navigator.clipboard.writeText(btn.dataset.copiar); toast('Copiado al portapapeles'); } catch (e) { /* nada */ }
        }));
    }

    // ---------- Constructor de cuestionarios (formulario de misión) ----------
    function iniciarFormMision(raiz = document) {
        const form = $('form[data-form="mision"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const contenedor = $('[data-preguntas]', form);
        const resumen = $('[data-resumen-quiz]', form);
        const etiquetaLink = $('[data-etiqueta-link]', form);
        const ayudaLink = $('[data-ayuda-link]', form);
        let contador = 0;

        const tipoActual = () => $('input[name=tipo]:checked', form)?.value || '';

        function crearOpcion(tarjeta, datos = {}) {
            const fila = document.createElement('div');
            fila.className = 'opcion-fila';
            if (datos.id) fila.dataset.id = datos.id;
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = 'correcta_' + tarjeta.dataset.clave;
            radio.className = 'check-correcta';
            radio.title = 'Marcar como respuesta correcta';
            radio.checked = !!datos.es_correcta;
            const texto = document.createElement('input');
            texto.type = 'text';
            texto.className = 'nl-input input-opcion';
            texto.placeholder = 'Texto de la opción';
            texto.value = datos.texto || '';
            const quitar = document.createElement('button');
            quitar.type = 'button';
            quitar.className = 'p-btn xs icono fantasma';
            quitar.title = 'Quitar opción';
            quitar.innerHTML = '<i class="bi bi-x-lg"></i>';
            quitar.addEventListener('click', () => { fila.remove(); actualizarResumen(); });
            fila.append(radio, texto, quitar);
            $('.opciones', tarjeta).appendChild(fila);
            return texto;
        }

        function agregarPregunta(datos = {}, opcionesIniciales = null) {
            contador += 1;
            const tarjeta = document.createElement('div');
            tarjeta.className = 'pregunta-card';
            tarjeta.dataset.clave = contador;
            if (datos.id) tarjeta.dataset.id = datos.id;
            tarjeta.innerHTML = `
                <div class="cabeza">
                    <span class="num"></span>
                    <input type="text" class="nl-input input-pregunta" placeholder="Escribe la pregunta">
                    <input type="number" class="nl-input input-puntos" min="1" style="width:84px" title="Puntos">
                    <button type="button" class="p-btn xs icono fantasma subir" title="Subir"><i class="bi bi-arrow-up"></i></button>
                    <button type="button" class="p-btn xs icono fantasma eliminar" title="Eliminar pregunta"><i class="bi bi-trash"></i></button>
                </div>
                <div class="opciones"></div>
                <button type="button" class="p-btn xs fantasma agregar-opcion"><i class="bi bi-plus"></i> Añadir opción</button>`;
            $('.input-pregunta', tarjeta).value = datos.texto || '';
            $('.input-puntos', tarjeta).value = datos.puntos || 10;
            $('.eliminar', tarjeta).addEventListener('click', () => { tarjeta.remove(); actualizarResumen(); });
            $('.subir', tarjeta).addEventListener('click', () => {
                if (tarjeta.previousElementSibling) contenedor.insertBefore(tarjeta, tarjeta.previousElementSibling);
                actualizarResumen();
            });
            $('.agregar-opcion', tarjeta).addEventListener('click', () => crearOpcion(tarjeta).focus());
            contenedor.appendChild(tarjeta);
            (datos.opciones || opcionesIniciales || [{}, {}]).forEach(o => crearOpcion(tarjeta, o));
            actualizarResumen();
            return tarjeta;
        }

        function actualizarResumen() {
            const tarjetas = $$('.pregunta-card', contenedor);
            let puntos = 0;
            tarjetas.forEach((t, i) => {
                $('.num', t).textContent = i + 1;
                puntos += parseInt($('.input-puntos', t).value || 0, 10);
            });
            resumen.textContent = tarjetas.length ? `${tarjetas.length} preguntas · ${puntos} puntos` : '';
        }

        function actualizarSecciones() {
            const tipo = tipoActual();
            $$('.seccion-tipo', form).forEach(s => s.classList.toggle('d-none', !s.dataset.tipos.split(' ').includes(tipo)));
            etiquetaLink.innerHTML = tipo === 'video' ? '<i class="bi bi-youtube"></i> Enlace del video de YouTube' : '<i class="bi bi-link-45deg"></i> Enlace';
            ayudaLink.classList.toggle('d-none', tipo !== 'video');
            if (tipo === 'cuestionario' && !contenedor.children.length) agregarPregunta();
        }

        // Se llama antes de enviar: arma el JSON de preguntas y valida el cuestionario
        form.antesDeEnviar = () => {
            if (tipoActual() !== 'cuestionario') return true;
            const preguntas = [];
            let problema = '';
            $$('.pregunta-card', contenedor).forEach((t, i) => {
                const texto = $('.input-pregunta', t).value.trim();
                if (!texto) return;
                const opciones = $$('.opcion-fila', t).map(f => ({
                    id: f.dataset.id ? parseInt(f.dataset.id, 10) : null,
                    texto: $('.input-opcion', f).value.trim(),
                    es_correcta: $('.check-correcta', f).checked,
                })).filter(o => o.texto);
                if (opciones.length < 2) problema = `La pregunta ${i + 1} necesita al menos 2 opciones.`;
                else if (!opciones.some(o => o.es_correcta)) problema = `Marca la respuesta correcta de la pregunta ${i + 1}.`;
                preguntas.push({
                    id: t.dataset.id ? parseInt(t.dataset.id, 10) : null,
                    texto, puntos: parseInt($('.input-puntos', t).value || 10, 10), opciones,
                });
            });
            if (!preguntas.length) problema = 'Agrega al menos una pregunta al cuestionario.';
            if (problema) { toast(problema, 'warning'); return false; }
            form.querySelector('[name=preguntas_json]').value = JSON.stringify(preguntas);
            return true;
        };

        contenedor.addEventListener('input', e => { if (e.target.matches('.input-puntos')) actualizarResumen(); });
        $('[data-agregar-pregunta]', form).addEventListener('click', () => $('.input-pregunta', agregarPregunta()).focus());
        $('[data-agregar-vf]', form).addEventListener('click', () => {
            $('.input-pregunta', agregarPregunta({}, [{ texto: 'Verdadero' }, { texto: 'Falso' }])).focus();
        });
        $$('input[name=tipo]', form).forEach(r => r.addEventListener('change', actualizarSecciones));

        const datos = $('#preguntas-data', form);
        try { JSON.parse(datos ? datos.textContent : '[]').forEach(p => agregarPregunta(p)); } catch (e) { /* sin preguntas */ }
        actualizarSecciones();
    }

    // En páginas completas (sin modal), la validación del cuestionario corre al enviar
    document.addEventListener('submit', e => {
        const form = e.target;
        if (form.closest('#modal-form') || typeof form.antesDeEnviar !== 'function') return;
        if (!form.antesDeEnviar()) e.preventDefault();
    });

    // "Poner 10 a los vacíos" en Calificar a todos
    document.addEventListener('click', e => {
        const btn = e.target.closest('[data-llenar-vacios]');
        if (!btn) return;
        $$('input[data-calif-aprobada="0"]', btn.closest('form')).forEach(i => { if (!i.value) i.value = 10; });
    });

    // ---------- Ventana emergente para los formularios ----------
    const Modal = (() => {
        let elemento, dialogo, contenido, instancia;
        let sucio = false;
        let guardando = false;

        function preparar() {
            elemento = $('#modal-form');
            if (!elemento || instancia) return !!elemento;
            dialogo = $('.modal-dialog', elemento);
            contenido = $('.modal-content', elemento);
            instancia = bootstrap.Modal.getOrCreateInstance(elemento);
            elemento.addEventListener('hide.bs.modal', async e => {
                if (!sucio || guardando) return;
                e.preventDefault();
                const descartar = await confirmar({
                    titulo: '¿Descartar los cambios?', texto: 'Lo que escribiste en el formulario se perderá.',
                    boton: 'Descartar', peligro: true,
                });
                if (descartar) { sucio = false; instancia.hide(); }
            });
            elemento.addEventListener('hidden.bs.modal', () => { contenido.innerHTML = ''; sucio = false; });
            return true;
        }

        const cabeceras = { 'X-Modal': '1', 'X-Requested-With': 'XMLHttpRequest' };

        function cargando(texto = 'Cargando…') {
            contenido.innerHTML = `<div class="modal-cargando"><div class="spinner-border" role="status"></div><span>${texto}</span></div>`;
        }

        function pintar(html) {
            contenido.innerHTML = html;
            const form = $('form', contenido);
            if (!form) return;
            sucio = false;
            iniciarFormMision(contenido);
            form.addEventListener('input', () => { sucio = true; });
            form.addEventListener('change', () => { sucio = true; });
            form.addEventListener('submit', enviar);
            const error = $('.con-error, .aviso-error', contenido);
            if (error) error.scrollIntoView({ block: 'center' });
            else setTimeout(() => $('.modal-body input:not([type=hidden]):not([type=radio]):not([type=checkbox]), .modal-body select, .modal-body textarea', contenido)?.focus(), 200);
        }

        async function abrir(url, tamano = '') {
            if (!preparar()) { location.href = url; return; }
            if (sucio && !(await confirmar({ titulo: '¿Descartar los cambios?', texto: 'Lo que escribiste en el formulario se perderá.', boton: 'Descartar', peligro: true }))) return;
            sucio = false;
            dialogo.classList.remove('modal-lg', 'modal-xl');
            dialogo.classList.add(tamano === 'xl' ? 'modal-xl' : 'modal-lg');
            cargando();
            instancia.show();
            try {
                const r = await fetch(url, { headers: cabeceras });
                if (!r.ok || r.redirected) throw new Error('sin modal');
                pintar(await r.text());
            } catch (e) {
                location.href = url;
            }
        }

        async function enviar(e) {
            e.preventDefault();
            const form = e.target;
            if (typeof form.antesDeEnviar === 'function' && !form.antesDeEnviar()) return;
            const boton = $('button[type=submit]', form);
            const original = boton?.innerHTML;
            if (boton) { boton.disabled = true; boton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Guardando…'; }
            try {
                const r = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: cabeceras });
                if (r.redirected) { location.href = r.url; return; }
                const tipo = r.headers.get('content-type') || '';
                if (tipo.includes('application/json')) {
                    const datos = await r.json();
                    if (datos.ok) {
                        guardando = true;
                        instancia.hide();
                        if (datos.navegar && datos.redirect) location.href = datos.redirect;
                        else location.reload();
                        return;
                    }
                }
                if (!r.ok) throw new Error('Error ' + r.status);
                pintar(await r.text());
                toast('Revisa los campos marcados', 'warning');
            } catch (err) {
                toast('No se pudo guardar. Inténtalo de nuevo.', 'error');
                if (boton) { boton.disabled = false; boton.innerHTML = original; }
            }
        }

        return { abrir };
    })();
    window.PModal = Modal;

    document.addEventListener('click', e => {
        const enlace = e.target.closest('a[data-modal]');
        if (!enlace || e.ctrlKey || e.metaKey || e.shiftKey || e.button !== 0) return;
        e.preventDefault();
        Modal.abrir(enlace.getAttribute('href'), enlace.dataset.modal);
    });

    function abrirDesdeUrl() {
        const params = new URLSearchParams(location.search);
        const destino = params.get('abrir');
        if (!destino || !/^\/(profesor|forja)\//.test(destino)) return;
        params.delete('abrir');
        history.replaceState(null, '', location.pathname + (params.toString() ? '?' + params : ''));
        Modal.abrir(destino, /mision/.test(destino) ? 'xl' : '');
    }

    document.addEventListener('DOMContentLoaded', () => {
        $$('.modal').forEach(m => document.body.appendChild(m));
        iniciarFormMision();
        abrirDesdeUrl();
        iniciarTema();
        iniciarMenu();
        iniciarConfirmaciones();
        iniciarCalificacion();
        iniciarBusqueda();
        iniciarInterruptores();
        iniciarStock();
        iniciarGrafica();
        iniciarCopiar();

        const datos = $('#mensajes-data');
        if (datos) {
            try {
                JSON.parse(datos.textContent).forEach((m, i) => setTimeout(() => {
                    const icono = m.tag.includes('error') ? 'error' : m.tag.includes('warning') ? 'warning' : m.tag.includes('info') ? 'info' : 'success';
                    toast(m.texto, icono);
                }, i * 400));
            } catch (e) { /* sin mensajes */ }
        }
    });
})();

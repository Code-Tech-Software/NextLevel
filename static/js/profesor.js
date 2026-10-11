/* =========================================================
   NEXT-LEVEL · Interacciones del panel del profesor
   ========================================================= */
(function () {
    'use strict';
    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
    function escapar(texto) {
        const div = document.createElement('div');
        div.textContent = texto ?? '';
        return div.innerHTML;
    }

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

    // ---------- Formulario de misión (guiado, con vista previa) ----------
    const TIPOS_MISION = {
        arduino: {
            emoji: '🤖', nombre: 'Arduino', icono: 'bi-cpu-fill', colores: ['#0ea5e9', '#0369a1'],
            instrucciones: 'Instrucciones del reto', nombrePh: 'Ej. Semáforo con 3 LEDs',
            placeholder: 'Ej. Conecta 3 LEDs (rojo, amarillo y verde) y prográmalos para que funcionen como un semáforo.',
            imagen: 'Diagrama o foto del circuito',
            explica: 'El alumno arma el circuito con tu código base y envía la misión (puede subir una foto). Tú la <b>calificas en Revisiones</b>.',
            flujo: ['Lee las instrucciones y copia el código', 'Arma el circuito y envía la misión', 'Tú la calificas en Revisiones'],
        },
        cuestionario: {
            emoji: '🧠', nombre: 'Cuestionario', icono: 'bi-patch-question-fill', colores: ['#8b5cf6', '#6d28d9'],
            instrucciones: 'Introducción del cuestionario', nombrePh: 'Ej. Quiz de circuitos',
            placeholder: 'Ej. Responde estas preguntas sobre lo que aprendimos de electricidad.',
            imagen: 'Imagen de apoyo', auto: true,
            explica: 'El alumno responde y <b>se califica solo al instante</b>. Las monedas dependen de cuántas acierte: no necesitas revisarlo.',
            flujo: ['Responde las preguntas una por una', 'Recibe su calificación al instante', 'Gana monedas según sus aciertos'],
        },
        link: {
            emoji: '🔗', nombre: 'Link', icono: 'bi-link-45deg', colores: ['#06b6d4', '#0e7490'],
            instrucciones: '¿Qué deben hacer en la página?', nombrePh: 'Ej. Explora Scratch',
            placeholder: 'Ej. Entra a Scratch y crea un personaje que se mueva con las flechas del teclado.',
            imagen: 'Imagen de apoyo',
            explica: 'El alumno abre el enlace, hace la actividad y la envía (puede agregar foto o comentario). Tú la <b>calificas en Revisiones</b>.',
            flujo: ['Abre el enlace en una pestaña nueva', 'Hace la actividad y la envía', 'Tú la calificas en Revisiones'],
        },
        video: {
            emoji: '🎬', nombre: 'Video', icono: 'bi-play-btn-fill', colores: ['#ef4444', '#b91c1c'],
            instrucciones: '¿Qué deben aprender del video?', nombrePh: 'Ej. ¿Qué es un circuito?',
            placeholder: 'Ej. Mira el video completo y pon atención en cómo viaja la electricidad.',
            imagen: 'Imagen de apoyo', auto: true, completo: true,
            explica: 'El video se ve dentro de la misión. Al terminar, el alumno presiona «¡Ya lo vi!» y <b>recibe el premio completo automáticamente</b>.',
            flujo: ['Ve el video dentro de la misión', 'Presiona «¡Ya lo vi!»', 'Recibe toda la XP y las monedas'],
        },
        evidencia: {
            emoji: '📸', nombre: 'Evidencia con foto', icono: 'bi-camera-fill', colores: ['#f59e0b', '#b45309'],
            instrucciones: '¿Qué deben construir y fotografiar?', nombrePh: 'Ej. Arma tu semáforo',
            placeholder: 'Ej. Construye tu semáforo y toma una foto donde se vean los 3 LEDs encendidos.',
            imagen: 'Foto de ejemplo',
            explica: 'El alumno <b>debe subir una foto</b> de su trabajo para poder enviarla. Tú la ves en grande y la <b>calificas en Revisiones</b>.',
            flujo: ['Hace la actividad', 'Sube una foto de su trabajo', 'Tú la revisas y la calificas'],
        },
        texto: {
            emoji: '✍️', nombre: 'Respuesta escrita', icono: 'bi-pencil-fill', colores: ['#ec4899', '#be185d'],
            instrucciones: 'Pregunta que deben responder', nombrePh: 'Ej. Explica tu semáforo',
            placeholder: 'Ej. Con tus palabras, explica para qué sirve una resistencia en un circuito.',
            imagen: 'Imagen de apoyo',
            explica: 'El alumno <b>escribe su respuesta</b> dentro de la misión. Tú la lees y la <b>calificas en Revisiones</b>.',
            flujo: ['Lee la pregunta', 'Escribe su respuesta y la envía', 'Tú la lees y la calificas'],
        },
        presencial: {
            emoji: '🙋', nombre: 'Actividad en clase', icono: 'bi-people-fill', colores: ['#10b981', '#047857'],
            instrucciones: 'Describe la actividad', nombrePh: 'Ej. Exposición en equipo',
            placeholder: 'Ej. En equipos, presenten su proyecto al grupo en 3 minutos.',
            imagen: 'Imagen de apoyo',
            explica: 'Se hace en el salón: el alumno <b>no envía nada</b>. Cuando la terminen, califícala con <b>«Calificar a todos»</b>.',
            flujo: ['Ve la misión en su mapa', 'La realiza en clase', 'Tú la calificas con «Calificar a todos»'],
        },
    };

    function idYoutube(url) {
        const m = (url || '').match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/))([\w-]{6,20})/);
        return m ? m[1] : '';
    }

    function iniciarFormMision(raiz = document) {
        const form = $('form[data-form="mision"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const contenedor = $('[data-preguntas]', form);
        const resumen = $('[data-resumen-quiz]', form);
        const tipoActual = () => $('input[name=tipo]:checked', form)?.value || '';
        let contador = 0;

        // ----- Constructor de cuestionarios -----
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

        contenedor.addEventListener('input', e => { if (e.target.matches('.input-puntos')) actualizarResumen(); });
        $('[data-agregar-pregunta]', form).addEventListener('click', () => $('.input-pregunta', agregarPregunta()).focus());
        $('[data-agregar-vf]', form).addEventListener('click', () => {
            $('.input-pregunta', agregarPregunta({}, [{ texto: 'Verdadero' }, { texto: 'Falso' }])).focus();
        });
        const datosPreguntas = $('#preguntas-data', form);
        try { JSON.parse(datosPreguntas ? datosPreguntas.textContent : '[]').forEach(p => agregarPregunta(p)); } catch (e) { /* sin preguntas */ }

        // ----- Paso 2: clase → mundo → nivel → posición -----
        let estructura = [];
        try { estructura = JSON.parse($('#estructura-data', form)?.textContent || '[]'); } catch (e) { estructura = []; }
        const selClase = $('[data-sel-clase]', form);
        const selMundo = $('[data-sel-mundo]', form);
        const selNivel = $('[data-sel-nivel]', form);
        const selPosicion = $('[data-sel-posicion]', form);
        const misionId = form.dataset.mision;
        const nivelOriginal = misionId ? form.dataset.nivelInicial : '';
        const sinNiveles = $('[data-sin-niveles]', form);

        const claseActual = () => estructura.find(c => String(c.id) === selClase.value);
        const mundoActual = () => claseActual()?.mundos.find(m => String(m.id) === selMundo.value);
        const nivelActual = () => mundoActual()?.niveles.find(n => String(n.id) === selNivel.value);

        function llenar(select, items, valor, textoVacio) {
            select.replaceChildren();
            if (!items.length) {
                select.appendChild(new Option(textoVacio, '', true, true));
                select.disabled = true;
                return;
            }
            select.disabled = false;
            items.forEach(item => select.appendChild(new Option(`${item.emoji ? item.emoji + ' ' : ''}${item.nombre}`, item.id)));
            if (valor && items.some(i => String(i.id) === String(valor))) select.value = valor;
        }

        function avisoSinNiveles(texto, mundoId) {
            sinNiveles.classList.toggle('d-none', !texto);
            if (!texto) return;
            $('[data-sin-niveles-texto]', form).textContent = texto;
            const enlace = $('[data-crear-nivel]', form);
            enlace.classList.toggle('d-none', !mundoId);
            if (mundoId) enlace.setAttribute('href', `/forja/nivel/nuevo/?mundo=${mundoId}`);
        }

        function llenarPosiciones(inicial) {
            const nivel = nivelActual();
            selPosicion.replaceChildren();
            const bloque = $('[data-bloque-posicion]', form);
            bloque.classList.toggle('d-none', !nivel);
            if (!nivel) return;
            const otras = nivel.misiones.filter(m => String(m.id) !== String(misionId));
            const mismoNivel = misionId && String(nivel.id) === String(nivelOriginal);
            if (mismoNivel) selPosicion.appendChild(new Option('Mantener su lugar actual', 'mantener'));
            const ultima = otras[otras.length - 1];
            selPosicion.appendChild(new Option(ultima ? `Al final (después de «${ultima.nombre}»)` : 'Primera misión del nivel', 'final'));
            if (otras.length) {
                selPosicion.appendChild(new Option('Al inicio del nivel', 'inicio'));
                otras.slice(0, -1).forEach(m => selPosicion.appendChild(new Option(`Después de «${m.nombre}»`, `despues:${m.id}`)));
            }
            const opciones = Array.from(selPosicion.options).map(o => o.value);
            selPosicion.value = opciones.includes(inicial) ? inicial : (mismoNivel ? 'mantener' : 'final');
            $('[data-ayuda-posicion]', form).textContent = otras.length
                ? `Este nivel tiene ${otras.length} misión${otras.length === 1 ? '' : 'es'}. Los alumnos las desbloquean en orden.`
                : 'Será la primera misión de este nivel.';
        }

        function alCambiarMundo(nivelInicial, posicionInicial) {
            const mundo = mundoActual();
            llenar(selNivel, mundo ? mundo.niveles : [], nivelInicial, 'Sin niveles');
            if (mundo && !mundo.niveles.length) avisoSinNiveles('Este mundo aún no tiene niveles.', mundo.id || null);
            else if (!mundo) avisoSinNiveles(claseActual() ? 'Esta clase aún no tiene mundos. Créalos en Clases y mundos.' : '', null);
            else avisoSinNiveles('', null);
            llenarPosiciones(posicionInicial);
            actualizarPrevia();
        }

        function alCambiarClase(mundoInicial, nivelInicial, posicionInicial) {
            const clase = claseActual();
            llenar(selMundo, clase ? clase.mundos : [], mundoInicial, 'Sin mundos');
            alCambiarMundo(nivelInicial, posicionInicial);
        }

        selClase.addEventListener('change', () => alCambiarClase());
        selMundo.addEventListener('change', () => alCambiarMundo());
        selNivel.addEventListener('change', () => { llenarPosiciones(); actualizarPrevia(); });

        // ----- Paso 3: contenido según el tipo -----
        const inputNombre = campo('nombre');
        const inputDescripcion = campo('descripcion');
        const inputLink = campo('link');
        const videoPrevia = $('[data-video-previa]', form);
        const ayudaLink = $('[data-ayuda-link]', form);

        function revisarLink() {
            const tipo = tipoActual();
            const url = inputLink.value.trim();
            videoPrevia.classList.add('d-none');
            ayudaLink.className = 'ayuda';
            if (tipo === 'video') {
                const id = idYoutube(url);
                if (id) {
                    if (videoPrevia.dataset.id !== id) {
                        videoPrevia.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${id}?rel=0" title="Vista previa del video" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen loading="lazy"></iframe>`;
                        videoPrevia.dataset.id = id;
                    }
                    videoPrevia.classList.remove('d-none');
                    ayudaLink.classList.add('ok');
                    ayudaLink.textContent = '✓ Video de YouTube detectado: así se verá dentro de la misión.';
                } else if (url) {
                    ayudaLink.classList.add('alerta');
                    ayudaLink.textContent = 'No parece un enlace de YouTube; se mostrará como un enlace normal.';
                } else {
                    ayudaLink.textContent = 'Copia el enlace desde YouTube (botón Compartir) y pégalo aquí.';
                }
            } else if (tipo === 'link') {
                ayudaLink.textContent = url && !/^https?:\/\//.test(url)
                    ? 'El enlace debe empezar con http:// o https://'
                    : 'Se abrirá en una pestaña nueva para que el alumno no pierda el mapa.';
                if (url && !/^https?:\/\//.test(url)) ayudaLink.classList.add('alerta');
            }
        }

        function aplicarTipo() {
            const tipo = tipoActual();
            const info = TIPOS_MISION[tipo];
            $$('.seccion-tipo', form).forEach(s => s.classList.toggle('d-none', !s.dataset.tipos.split(' ').includes(tipo)));
            const explicacion = $('[data-explicacion-tipo]', form);
            explicacion.classList.toggle('d-none', !info);
            if (info) {
                explicacion.innerHTML = `<span class="e">${info.emoji}</span><div>${info.explica}</div>`;
                $('[data-label-instrucciones]', form).textContent = info.instrucciones;
                inputDescripcion.placeholder = info.placeholder;
                inputNombre.placeholder = info.nombrePh;
                $('[data-label-imagen]', form).innerHTML = `${info.imagen} <span class="text-muted-p fw-normal">(opcional)</span>`;
                $('[data-etiqueta-link]', form).innerHTML = tipo === 'video'
                    ? '<i class="bi bi-youtube"></i> Enlace del video de YouTube <span class="text-danger">*</span>'
                    : '<i class="bi bi-link-45deg"></i> Enlace de la página <span class="text-danger">*</span>';
            }
            if (tipo === 'cuestionario' && !contenedor.children.length) agregarPregunta();
            revisarLink();
            actualizarPrevia();
        }

        let temporizadorLink = null;
        inputLink.addEventListener('input', () => { clearTimeout(temporizadorLink); temporizadorLink = setTimeout(revisarLink, 350); });
        $$('input[name=tipo]', form).forEach(r => r.addEventListener('change', aplicarTipo));

        const inputImagen = campo('imagen');
        const imagenPrevia = $('[data-imagen-previa]', form);
        form.querySelector('input[name$="-clear"]')?.addEventListener('change', e => {
            imagenPrevia.classList.toggle('d-none', e.target.checked);
        });
        inputImagen?.addEventListener('change', () => {
            const archivo = inputImagen.files[0];
            if (!archivo) return;
            const lector = new FileReader();
            lector.onload = e => { imagenPrevia.src = e.target.result; imagenPrevia.classList.remove('d-none'); };
            lector.readAsDataURL(archivo);
        });

        // ----- Paso 4: recompensa -----
        const inputXp = campo('xp_recompensa');
        const inputMonedas = campo('monedas_recompensa');
        const checkJefe = campo('es_jefe');
        const checkActiva = campo('activa');

        function marcarPreset() {
            $$('[data-preset]', form).forEach(b => b.classList.toggle('activo',
                b.dataset.xp === inputXp.value && b.dataset.monedas === inputMonedas.value));
        }
        $$('[data-preset]', form).forEach(btn => btn.addEventListener('click', () => {
            inputXp.value = btn.dataset.xp;
            inputMonedas.value = btn.dataset.monedas;
            if (btn.dataset.jefe) checkJefe.checked = true;
            form.dispatchEvent(new Event('input', { bubbles: true }));
            marcarPreset();
            actualizarPrevia();
        }));

        function textoRecompensa() {
            const xp = parseInt(inputXp.value || 0, 10);
            const monedas = parseInt(inputMonedas.value || 0, 10);
            const info = TIPOS_MISION[tipoActual()];
            const ejemplo = Math.floor(monedas * 0.8);
            if (info?.completo) return `💡 Al ver el video recibe siempre las <b>${monedas} monedas</b> y <b>${xp} XP</b>.`;
            if (info?.auto) return `💡 Si acierta el 80 % gana <b>${ejemplo} de ${monedas} monedas</b>. La XP (<b>${xp}</b>) siempre es completa.`;
            return `💡 Si la calificas con 8, gana <b>${ejemplo} de ${monedas} monedas</b>. La XP (<b>${xp}</b>) siempre es completa.`;
        }

        // ----- Vista previa -----
        function actualizarPrevia() {
            const tipo = tipoActual();
            const info = TIPOS_MISION[tipo];
            const nodo = $('[data-vp-nodo]', form);
            const icono = $('[data-vp-icono]', form);
            nodo.style.setProperty('--n1', info ? info.colores[0] : '#94a3b8');
            nodo.style.setProperty('--n2', info ? info.colores[1] : '#64748b');
            icono.className = `bi ${info ? info.icono : 'bi-question-lg'}`;
            const jefe = checkJefe?.checked;
            nodo.classList.toggle('jefe', !!jefe);
            $('[data-vp-corona]', form).classList.toggle('d-none', !jefe);
            $('[data-vp-jefe]', form).classList.toggle('d-none', !jefe);
            $('[data-vp-oculta]', form).classList.toggle('d-none', !!checkActiva?.checked);
            $('[data-vp-nombre]', form).textContent = inputNombre.value.trim() || 'Nombre de la misión';
            $('[data-vp-tipo]', form).textContent = info ? `${info.emoji} ${info.nombre}` : 'Elige un tipo';
            const mundo = mundoActual();
            const nivel = nivelActual();
            $('[data-vp-ubicacion]', form).innerHTML = nivel
                ? `<i class="bi bi-geo-alt"></i> ${escapar(mundo.emoji)} ${escapar(mundo.nombre)} › ${escapar(nivel.nombre)}`
                : '<i class="bi bi-geo-alt"></i> Sin ubicación';
            $('[data-vp-xp]', form).textContent = inputXp.value || 0;
            $('[data-vp-monedas]', form).textContent = inputMonedas.value || 0;
            $('[data-vp-flujo]', form).innerHTML = info
                ? `<div class="t">Cómo funciona</div><ol>${info.flujo.map(p => `<li>${escapar(p)}</li>`).join('')}</ol>`
                : '';
            $('[data-hint-recompensa]', form).innerHTML = textoRecompensa();
            const pasos = $$('.paso', form);
            pasos[0]?.classList.toggle('completo', !!tipo);
            pasos[1]?.classList.toggle('completo', !!nivel);
            pasos[2]?.classList.toggle('completo', !!(inputNombre.value.trim() && inputDescripcion.value.trim()));
            pasos[3]?.classList.toggle('completo', !!(inputXp.value && inputMonedas.value));
            pasos[4]?.classList.toggle('completo', true);
        }
        form.addEventListener('input', e => {
            if (e.target === inputXp || e.target === inputMonedas) marcarPreset();
            actualizarPrevia();
        });
        form.addEventListener('change', actualizarPrevia);

        // ----- Validación antes de enviar -----
        form.antesDeEnviar = () => {
            if (!tipoActual()) {
                toast('Elige qué tipo de misión es (paso 1)', 'warning');
                $('.paso', form).scrollIntoView({ behavior: 'smooth', block: 'start' });
                return false;
            }
            if (!selNivel.value) {
                toast('Elige el nivel donde aparecerá la misión (paso 2)', 'warning');
                selNivel.closest('.paso').scrollIntoView({ behavior: 'smooth', block: 'start' });
                return false;
            }
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
            campo('preguntas_json').value = JSON.stringify(preguntas);
            return true;
        };

        // Estado inicial (al final, cuando todos los campos ya existen)
        if (!estructura.length) {
            llenar(selClase, [], '', 'No hay clases');
            avisoSinNiveles('Primero crea una clase con un mundo y un nivel en «Clases y mundos».', null);
        } else {
            let inicio = null;
            estructura.forEach(c => c.mundos.forEach(m => m.niveles.forEach(n => {
                if (String(n.id) === String(form.dataset.nivelInicial)) inicio = { c, m, n };
            })));
            if (!inicio) {
                // Sin nivel elegido: proponer la primera clase que ya tenga niveles
                const c = estructura.find(x => x.mundos.some(m => m.niveles.length));
                const m = c?.mundos.find(x => x.niveles.length);
                if (c) inicio = { c, m, n: m.niveles[0] };
            }
            llenar(selClase, estructura, inicio?.c.id);
            alCambiarClase(inicio?.m.id, inicio?.n.id, form.dataset.posicionInicial);
        }
        aplicarTipo();
        marcarPreset();
    }

    // ---------- Formulario de logro (guiado, con medalla de vista previa) ----------
    const CONDICIONES_LOGRO = {
        misiones: { pregunta: '¿Cuántas misiones debe completar?', unidad: 'misiones', sugerencias: [1, 5, 10, 25], texto: n => n === 1 ? 'Completa tu primera misión' : `Completa ${n} misiones` },
        xp: { pregunta: '¿Cuánta XP total debe juntar?', unidad: 'XP', sugerencias: [100, 500, 1000, 2000], texto: n => `Llega a ${n} XP` },
        nivel: { pregunta: '¿Qué nivel debe alcanzar?', unidad: 'nivel', sugerencias: [3, 5, 10, 20], texto: n => `Llega al nivel ${n}` },
        racha: { pregunta: '¿Cuántos días seguidos debe entrar?', unidad: 'días', sugerencias: [3, 5, 7, 14], texto: n => `Entra ${n} días seguidos` },
        perfectos: { pregunta: '¿En cuántos cuestionarios debe sacar 10?', unidad: 'cuestionarios', sugerencias: [1, 3, 5, 10], texto: n => n === 1 ? 'Saca 10 en un cuestionario' : `Saca 10 en ${n} cuestionarios` },
        jefes: { pregunta: '¿Cuántos jefes debe derrotar?', unidad: 'jefes', sugerencias: [1, 2, 3, 5], texto: n => n === 1 ? 'Derrota a tu primer jefe' : `Derrota ${n} jefes` },
        mundos: { pregunta: '¿Cuántos mundos debe completar?', unidad: 'mundos', sugerencias: [1, 2, 3, 4], texto: n => n === 1 ? 'Completa un mundo entero' : `Completa ${n} mundos` },
        diarias: { pregunta: '¿Cuántas misiones del día debe reclamar?', unidad: 'misiones del día', sugerencias: [5, 10, 20, 50], texto: n => `Completa ${n} misiones del día` },
        monedas: { pregunta: '¿Cuántas monedas debe ganar en total?', unidad: 'monedas', sugerencias: [100, 250, 500, 1000], texto: n => `Gana ${n} monedas en total` },
        compras: { pregunta: '¿Cuántas compras debe hacer en la tienda?', unidad: 'compras', sugerencias: [1, 3, 5, 10], texto: n => n === 1 ? 'Haz tu primera compra en la tienda' : `Haz ${n} compras en la tienda` },
        manual: { texto: () => 'Reconocimiento especial de tu profe' },
    };
    const PREMIOS_RAREZA = { comun: [10, 0], raro: [25, 10], epico: [50, 25], legendario: [100, 50] };
    const NOMBRES_RAREZA = { comun: 'Común', raro: 'Raro', epico: 'Épico', legendario: 'Legendario' };

    function iniciarFormLogro(raiz = document) {
        const form = $('form[data-form="logro"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const inputValor = campo('valor');
        const inputNombre = campo('nombre');
        const inputDescripcion = campo('descripcion');
        const inputIcono = campo('icono');
        const inputMonedas = campo('recompensa_monedas');
        const inputXp = campo('recompensa_xp');
        const condicion = () => $('input[name=condicion]:checked', form)?.value || 'misiones';
        const rareza = () => $('input[name=rareza]:checked', form)?.value || 'comun';
        const totalAlumnos = parseInt(form.dataset.totalAlumnos || 0, 10);
        const esNuevo = !inputNombre.value;
        let ultimaDescripcion = '';
        let premioTocado = !esNuevo;

        const descripcionSugerida = () => {
            const info = CONDICIONES_LOGRO[condicion()];
            return info.texto(Math.max(1, parseInt(inputValor.value || 1, 10)));
        };
        // Mientras la descripción sea la sugerida (o esté vacía), se actualiza sola al cambiar la meta
        let auto = esNuevo || !inputDescripcion.value.trim() || inputDescripcion.value === descripcionSugerida();

        function sugerirDescripcion(forzar) {
            if (!forzar && !auto) return;
            ultimaDescripcion = descripcionSugerida();
            inputDescripcion.value = ultimaDescripcion;
            auto = true;
        }

        let temporizador = null;
        async function contarCumplen() {
            const caja = $('[data-cumplen]', form);
            if (condicion() === 'manual') { caja.innerHTML = ''; return; }
            caja.innerHTML = '<span class="text-muted-p">Calculando…</span>';
            try {
                const params = new URLSearchParams({ condicion: condicion(), valor: inputValor.value || 1 });
                const r = await fetch(`${form.dataset.urlCumplen}?${params}`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
                const { total } = await r.json();
                caja.innerHTML = total
                    ? `👥 <b>${total}</b> de ${totalAlumnos} alumnos ya lo cumplen: <b>lo recibirán al guardar</b>.`
                    : '🎯 Ningún alumno lo cumple todavía: ¡será un buen reto!';
            } catch (e) { caja.innerHTML = ''; }
        }

        function aplicarCondicion() {
            const c = condicion();
            const info = CONDICIONES_LOGRO[c];
            const manual = c === 'manual';
            $('[data-bloque-valor]', form).classList.toggle('d-none', manual);
            $('[data-aviso-manual]', form).classList.toggle('d-none', !manual);
            $('[data-meta-sub]', form).textContent = manual ? 'Este logro no tiene meta automática.' : '¿Cuánto debe lograr el alumno?';
            if (!manual) {
                $('[data-pregunta-valor]', form).textContent = info.pregunta;
                $('[data-unidad-valor]', form).textContent = info.unidad;
                const sugerencias = $('[data-sugerencias]', form);
                sugerencias.replaceChildren();
                info.sugerencias.forEach(n => {
                    const b = document.createElement('button');
                    b.type = 'button';
                    b.textContent = n;
                    b.classList.toggle('activo', String(n) === inputValor.value);
                    b.addEventListener('click', () => { inputValor.value = n; alCambiarValor(); });
                    sugerencias.appendChild(b);
                });
            }
            sugerirDescripcion(false);
            contarCumplen();
            actualizarPrevia();
        }

        function alCambiarValor() {
            $$('[data-sugerencias] button', form).forEach(b => b.classList.toggle('activo', b.textContent === inputValor.value));
            sugerirDescripcion(false);
            clearTimeout(temporizador);
            temporizador = setTimeout(contarCumplen, 350);
            actualizarPrevia();
        }

        function marcarIcono() {
            $$('[data-icono]', form).forEach(b => b.classList.toggle('activo', b.dataset.icono === inputIcono.value.trim()));
        }

        function actualizarPrevia() {
            const medalla = $('[data-medalla]', form);
            medalla.className = `medalla-previa ${rareza()}`;
            $('[data-medalla-icono]', form).textContent = inputIcono.value.trim() || '🏅';
            $('[data-medalla-nombre]', form).textContent = inputNombre.value.trim() || 'Nombre del logro';
            $('[data-medalla-desc]', form).textContent = inputDescripcion.value.trim() || descripcionSugerida();
            $('[data-medalla-rareza]', form).textContent = NOMBRES_RAREZA[rareza()];
            const monedas = parseInt(inputMonedas.value || 0, 10);
            const xp = parseInt(inputXp.value || 0, 10);
            const premio = [monedas ? `+${monedas} monedas` : '', xp ? `+${xp} XP` : ''].filter(Boolean).join(' · ');
            $('[data-medalla-premio]', form).textContent = premio ? `🎁 ${premio}` : 'Sin premio extra';
            $('[data-medalla-como]', form).innerHTML = condicion() === 'manual'
                ? '<div class="t">Cómo se gana</div>🎁 Lo entregas tú desde «Otorgar logro» o desde el perfil del alumno.'
                : `<div class="t">Cómo se gana</div>🔓 Se desbloquea solo y el alumno ve una celebración con confeti.`;
            const pasos = $$('.paso', form);
            pasos[0]?.classList.add('completo');
            pasos[1]?.classList.toggle('completo', condicion() === 'manual' || !!inputValor.value);
            pasos[2]?.classList.toggle('completo', !!(inputNombre.value.trim() && inputDescripcion.value.trim()));
            pasos[3]?.classList.add('completo');
        }

        $$('input[name=condicion]', form).forEach(r => r.addEventListener('change', aplicarCondicion));
        inputValor.addEventListener('input', alCambiarValor);
        inputDescripcion.addEventListener('input', () => { auto = inputDescripcion.value === ultimaDescripcion; actualizarPrevia(); });
        $('[data-sugerir-descripcion]', form).addEventListener('click', () => { sugerirDescripcion(true); actualizarPrevia(); });
        $$('[data-icono]', form).forEach(b => b.addEventListener('click', () => {
            inputIcono.value = b.dataset.icono;
            form.dispatchEvent(new Event('input', { bubbles: true }));
            marcarIcono();
            actualizarPrevia();
        }));
        inputIcono.addEventListener('input', () => { marcarIcono(); actualizarPrevia(); });
        inputNombre.addEventListener('input', actualizarPrevia);
        [inputMonedas, inputXp].forEach(i => i.addEventListener('input', () => { premioTocado = true; actualizarPrevia(); }));
        function aplicarPremioSugerido() {
            const [monedas, xp] = PREMIOS_RAREZA[rareza()];
            inputMonedas.value = monedas;
            inputXp.value = xp;
            actualizarPrevia();
        }
        $$('input[name=rareza]', form).forEach(r => r.addEventListener('change', () => {
            if (!premioTocado) aplicarPremioSugerido();
            actualizarPrevia();
        }));
        $('[data-premio-sugerido]', form).addEventListener('click', () => {
            aplicarPremioSugerido();
            form.dispatchEvent(new Event('input', { bubbles: true }));
        });

        if (esNuevo) ultimaDescripcion = inputDescripcion.value = descripcionSugerida();
        else ultimaDescripcion = auto ? inputDescripcion.value : '';
        marcarIcono();
        aplicarCondicion();
    }

    // ---------- Formulario de misión del día (guiado) ----------
    const OBJETIVOS_DIARIA = {
        login: { sinMeta: true, titulo: 'Reportándome', icono: '👋', texto: () => 'Entra a la plataforma hoy',
            explica: 'Se cumple <b>en cuanto el alumno abre su mapa</b>. Es la misión fácil que siempre sale en el sorteo.',
            nota: 'No necesita cantidad: con entrar una vez al día queda completa.' },
        misiones: { pregunta: '¿Cuántas misiones del mapa debe completar hoy?', unidad: 'misiones', sugerencias: [1, 2, 3],
            titulo: 'Aventurero del día', icono: '🗺️', texto: n => n === 1 ? 'Completa 1 misión del mapa' : `Completa ${n} misiones del mapa`,
            explica: 'Cuenta cada misión del mapa que el alumno <b>envía o termina</b> ese día (aunque tú la revises después).' },
        cuestionarios: { pregunta: '¿Cuántos cuestionarios debe responder hoy?', unidad: 'cuestionarios', sugerencias: [1, 2, 3],
            titulo: 'Mente brillante', icono: '🧠', texto: n => n === 1 ? 'Responde un cuestionario' : `Responde ${n} cuestionarios`,
            explica: 'Cuenta cada <b>cuestionario terminado</b>, sin importar la calificación.' },
        perfecto: { pregunta: '¿En cuántos cuestionarios debe sacar 10 hoy?', unidad: 'cuestionarios', sugerencias: [1, 2],
            titulo: '¡Diez perfecto!', icono: '💯', texto: n => n === 1 ? 'Saca 10 en un cuestionario' : `Saca 10 en ${n} cuestionarios`,
            explica: 'Solo cuenta si el alumno <b>acierta todas las preguntas</b>. Es un reto difícil: dale buen premio.' },
        xp: { pregunta: '¿Cuánta XP debe ganar hoy?', unidad: 'XP', sugerencias: [50, 100, 200],
            titulo: 'Cazador de XP', icono: '🔋', texto: n => `Gana ${n} XP hoy`,
            explica: 'Suma <b>toda la XP del día</b>: misiones, cofres, logros y los botones del modo clase.' },
        evidencias: { pregunta: '¿Cuántos trabajos debe enviar hoy?', unidad: 'trabajos', sugerencias: [1, 2, 3],
            titulo: 'Manos a la obra', icono: '🛠️', texto: n => n === 1 ? 'Envía un trabajo para revisión' : `Envía ${n} trabajos para revisión`,
            explica: 'Cuenta las misiones que llegan a tu <b>bandeja de Revisiones</b> (Arduino, link, foto o respuesta escrita).' },
        tienda: { sinMeta: true, titulo: 'De compras', icono: '🛍️', texto: () => 'Visita la tienda',
            explica: 'Se cumple con <b>solo entrar a la tienda</b>; no tiene que comprar nada.',
            nota: 'No necesita cantidad: con entrar una vez a la tienda queda completa.' },
    };

    function iniciarFormDiaria(raiz = document) {
        const form = $('form[data-form="diaria"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const inputMeta = campo('meta');
        const inputTitulo = campo('titulo');
        const inputDescripcion = campo('descripcion');
        const inputIcono = campo('icono');
        const inputMonedas = campo('recompensa_monedas');
        const inputXp = campo('recompensa_xp');
        const objetivo = () => $('input[name=objetivo]:checked', form)?.value || 'misiones';
        const info = () => OBJETIVOS_DIARIA[objetivo()];
        const meta = () => (info().sinMeta ? 1 : Math.max(1, parseInt(inputMeta.value || 1, 10)));
        const esNueva = !inputTitulo.value;

        // Mientras nombre, ícono y descripción sean los sugeridos, se actualizan solos al cambiar el objetivo
        const sugeridos = { titulo: esNueva, icono: esNueva, descripcion: esNueva || !inputDescripcion.value.trim() };
        let ultimo = { titulo: inputTitulo.value, icono: inputIcono.value, descripcion: inputDescripcion.value };

        function proponer(forzar = false) {
            const i = info();
            const valores = { titulo: i.titulo, icono: i.icono, descripcion: i.texto(meta()) };
            Object.entries(valores).forEach(([clave, valor]) => {
                const input = { titulo: inputTitulo, icono: inputIcono, descripcion: inputDescripcion }[clave];
                if (forzar || sugeridos[clave]) {
                    input.value = valor;
                    ultimo[clave] = valor;
                    sugeridos[clave] = true;
                }
            });
        }

        function aplicarObjetivo() {
            const i = info();
            $('[data-bloque-meta]', form).classList.toggle('d-none', !!i.sinMeta);
            const sinMeta = $('[data-sin-meta]', form);
            sinMeta.classList.toggle('d-none', !i.sinMeta);
            sinMeta.innerHTML = i.sinMeta ? `<i class="bi bi-check2-circle"></i> ${i.nota}` : '';
            $('[data-meta-sub]', form).textContent = i.sinMeta ? 'Se cumple con una sola acción.' : '¿Cuántas veces en el día?';
            const explicacion = $('[data-explicacion-objetivo]', form);
            explicacion.classList.remove('d-none');
            explicacion.innerHTML = `<span class="e">${i.icono}</span><div>${i.explica}</div>`;
            if (!i.sinMeta) {
                $('[data-pregunta-meta]', form).textContent = i.pregunta;
                $('[data-unidad-meta]', form).textContent = i.unidad;
                const sugerencias = $('[data-sugerencias-meta]', form);
                sugerencias.replaceChildren();
                i.sugerencias.forEach(n => {
                    const b = document.createElement('button');
                    b.type = 'button';
                    b.textContent = n;
                    b.addEventListener('click', () => { inputMeta.value = n; alCambiarMeta(); });
                    sugerencias.appendChild(b);
                });
            }
            proponer();
            alCambiarMeta();
        }

        function alCambiarMeta() {
            $$('[data-sugerencias-meta] button', form).forEach(b => b.classList.toggle('activo', b.textContent === String(meta())));
            const i = info();
            if (!i.sinMeta) {
                const n = meta();
                $('[data-ayuda-meta]', form).textContent = n >= 3 && objetivo() !== 'xp'
                    ? 'Es una meta alta para un solo día: asegúrate de que haya suficientes misiones disponibles.'
                    : 'Tip: las metas pequeñas motivan a entrar todos los días.';
            }
            if (sugeridos.descripcion) {
                inputDescripcion.value = i.texto(meta());
                ultimo.descripcion = inputDescripcion.value;
            }
            actualizarPrevia();
        }

        function marcarIcono() {
            $$('[data-icono]', form).forEach(b => b.classList.toggle('activo', b.dataset.icono === inputIcono.value.trim()));
        }
        function marcarPreset() {
            $$('[data-preset]', form).forEach(b => b.classList.toggle('activo',
                b.dataset.monedas === inputMonedas.value && b.dataset.xp === inputXp.value));
        }

        function actualizarPrevia() {
            const n = meta();
            $('[data-previa-icono]', form).textContent = inputIcono.value.trim() || info().icono;
            $('[data-previa-titulo]', form).textContent = inputTitulo.value.trim() || info().titulo;
            $('[data-previa-desc]', form).textContent = inputDescripcion.value.trim() || info().texto(n);
            $('[data-previa-contador]', form).textContent = `0/${n}`;
            const monedas = parseInt(inputMonedas.value || 0, 10);
            const xp = parseInt(inputXp.value || 0, 10);
            $('[data-previa-premio]', form).textContent = [monedas ? `🪙 ${monedas}` : '', xp ? `⚡ ${xp} XP` : ''].filter(Boolean).join(' · ') || 'Sin premio';
            $('[data-previa-como]', form).innerHTML = info().sinMeta
                ? 'Se completa sola con una acción.' : `El contador sube solo hasta llegar a <b>${n}</b> durante el día.`;
            marcarIcono();
            marcarPreset();
            const pasos = $$('.paso', form);
            pasos.forEach(p => p.classList.add('completo'));
            pasos[2]?.classList.toggle('completo', !!inputTitulo.value.trim());
        }

        $$('input[name=objetivo]', form).forEach(r => r.addEventListener('change', aplicarObjetivo));
        inputMeta.addEventListener('input', alCambiarMeta);
        inputTitulo.addEventListener('input', () => { sugeridos.titulo = inputTitulo.value === ultimo.titulo; actualizarPrevia(); });
        inputIcono.addEventListener('input', () => { sugeridos.icono = inputIcono.value === ultimo.icono; actualizarPrevia(); });
        inputDescripcion.addEventListener('input', () => { sugeridos.descripcion = inputDescripcion.value === ultimo.descripcion; actualizarPrevia(); });
        [inputMonedas, inputXp].forEach(i => i.addEventListener('input', actualizarPrevia));
        $('[data-sugerir-titulo]', form).addEventListener('click', () => { proponer(true); actualizarPrevia(); });
        $$('[data-icono]', form).forEach(b => b.addEventListener('click', () => {
            inputIcono.value = b.dataset.icono;
            sugeridos.icono = false;
            form.dispatchEvent(new Event('input', { bubbles: true }));
            actualizarPrevia();
        }));
        $$('[data-preset]', form).forEach(b => b.addEventListener('click', () => {
            inputMonedas.value = b.dataset.monedas;
            inputXp.value = b.dataset.xp;
            form.dispatchEvent(new Event('input', { bubbles: true }));
            actualizarPrevia();
        }));

        aplicarObjetivo();
    }

    // ---------- Formulario de artículo de tienda (guiado) ----------
    const TIPOS_ARTICULO = {
        fisico: {
            emoji: '🎁', nombrePh: 'Ej. Stickers de robots', descPh: 'Ej. Un paquete de 5 stickers holográficos.',
            explica: 'Algo que entregas en mano (stickers, llaveros, dulces…). Lleva <b>stock</b>: cuando se acaba aparece «AGOTADO». Cada compra llega a <b>Pedidos</b> para que la entregues.',
            defaults: { stock: 10, entrega: true },
        },
        permiso: {
            emoji: '🎟️', nombrePh: 'Ej. Elige tu lugar por un día', descPh: 'Ej. Siéntate donde quieras durante una clase.',
            explica: 'Un beneficio en el salón (elegir lugar, minutos extra de recreo…). Llega a <b>Pedidos</b> y lo marcas como entregado cuando el alumno lo usa.',
            defaults: { stock: null, entrega: true },
        },
        avatar: {
            emoji: '🤖', nombrePh: 'Ej. Robot astronauta', descPh: 'Ej. Un avatar exclusivo para tu perfil.',
            explica: 'Una imagen para su perfil. <b>Se equipa sola al comprarla</b> y después puede cambiarla desde su perfil. <b>Necesita imagen.</b>',
            defaults: { stock: null, entrega: false, limite: 1 },
        },
        otro: {
            emoji: '💎', nombrePh: 'Ej. DJ de la clase', descPh: 'Ej. Elige la música de fondo mientras trabajamos.',
            explica: 'Algo dentro de la plataforma o un reconocimiento especial. Tú decides si lo entregas o si es automático.',
            defaults: { stock: null, entrega: false },
        },
    };
    const MONEDAS_POR_MISION = 15;

    function iniciarFormArticulo(raiz = document) {
        const form = $('form[data-form="articulo"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const tipo = () => $('input[name=tipo]:checked', form)?.value || 'fisico';
        const inputNombre = campo('nombre');
        const inputDesc = campo('descripcion');
        const inputPrecio = campo('costo_monedas');
        const inputStock = campo('stock');
        const inputLimite = campo('limite_por_alumno');
        const inputNivel = campo('nivel_requerido');
        const checkEntrega = campo('requiere_validacion');
        const checkDestacado = campo('destacado');
        const checkActivo = campo('activo');
        const inputImagen = campo('imagen');
        const imagenPrevia = $('[data-imagen-previa]', form);
        let monedasAlumnos = [];
        let rangos = [];
        try { monedasAlumnos = JSON.parse($('#monedas-alumnos', form).textContent); } catch (e) { /* sin datos */ }
        try { rangos = JSON.parse($('#rangos-data', form).textContent); } catch (e) { /* sin datos */ }
        const tocado = { stock: false, limite: false, entrega: false };
        let modoStock = inputStock.value === '' ? 'ilimitado' : 'limitado';
        let modoLimite = inputLimite.value === '' ? 'libre' : 'limitado';
        let ultimoStock = inputStock.value || '10';
        let ultimoLimite = inputLimite.value || '1';
        let limiteAutomatico = false;

        function pintarSegmentos() {
            $$('[data-modo-stock]', form).forEach(b => b.classList.toggle('activo', b.dataset.modoStock === modoStock));
            $$('[data-modo-limite]', form).forEach(b => b.classList.toggle('activo', b.dataset.modoLimite === modoLimite));
            $('[data-bloque-stock]', form).classList.toggle('d-none', modoStock === 'ilimitado');
            $('[data-bloque-limite]', form).classList.toggle('d-none', modoLimite === 'libre');
        }
        function ponerStock(modo) {
            if (modoStock === 'limitado' && inputStock.value !== '') ultimoStock = inputStock.value;
            modoStock = modo;
            inputStock.value = modo === 'ilimitado' ? '' : ultimoStock;
        }
        function ponerLimite(modo) {
            if (modoLimite === 'limitado' && inputLimite.value !== '') ultimoLimite = inputLimite.value;
            modoLimite = modo;
            inputLimite.value = modo === 'libre' ? '' : ultimoLimite;
        }

        function aplicarTipo(cambio) {
            const info = TIPOS_ARTICULO[tipo()];
            const explicacion = $('[data-explicacion-tipo]', form);
            explicacion.classList.remove('d-none');
            explicacion.innerHTML = `<span class="e">${info.emoji}</span><div>${info.explica}</div>`;
            inputNombre.placeholder = info.nombrePh;
            inputDesc.placeholder = info.descPh;
            const avatar = tipo() === 'avatar';
            $('[data-label-imagen]', form).innerHTML = avatar
                ? 'Imagen del avatar <span class="text-danger">*</span>'
                : 'Foto del premio <span class="text-muted-p fw-normal">(opcional)</span>';
            $('[data-ayuda-imagen]', form).textContent = avatar
                ? 'Usa una imagen cuadrada: se mostrará en círculo en el perfil del alumno.'
                : 'Si no subes foto se mostrará un ícono. Las imágenes con fondo transparente lucen mejor.';
            imagenPrevia.classList.toggle('circular', avatar);
            if (cambio) {
                const d = info.defaults;
                if (!tocado.stock) {
                    if (d.stock === null) ponerStock('ilimitado');
                    else { if (modoStock === 'ilimitado') ultimoStock = String(d.stock); ponerStock('limitado'); }
                }
                if (!tocado.entrega) checkEntrega.checked = d.entrega;
                if (!tocado.limite) {
                    // El límite que pone el avatar se quita solo si cambias a otro tipo
                    if (d.limite) { ultimoLimite = String(d.limite); ponerLimite('limitado'); }
                    else if (limiteAutomatico) ponerLimite('libre');
                    limiteAutomatico = !!d.limite;
                }
            }
            if (avatar) checkEntrega.checked = false;
            pintarSegmentos();
            actualizar();
        }

        function rangoDeNivel(nivel) {
            let actual = rangos[0];
            rangos.forEach(r => { if (nivel >= r.nivel) actual = r; });
            return actual;
        }

        function actualizar() {
            const info = TIPOS_ARTICULO[tipo()];
            const precio = Math.max(0, parseInt(inputPrecio.value || 0, 10));
            const stock = modoStock === 'ilimitado' ? null : Math.max(0, parseInt(inputStock.value || 0, 10));
            const limite = modoLimite === 'libre' ? null : Math.max(1, parseInt(inputLimite.value || 1, 10));
            const nivel = Math.max(1, parseInt(inputNivel.value || 1, 10));

            // Precio
            $$('[data-precio]', form).forEach(b => b.classList.toggle('activo', b.dataset.precio === String(precio)));
            const misiones = Math.max(1, Math.ceil(precio / MONEDAS_POR_MISION));
            const pueden = monedasAlumnos.filter(m => m >= precio).length;
            $('[data-ayuda-precio]', form).innerHTML = precio
                ? `💡 Equivale a unas <b>${misiones} ${misiones === 1 ? 'misión normal' : 'misiones normales'}</b> (${MONEDAS_POR_MISION} monedas cada una).<br>👥 <b>${pueden} de ${monedasAlumnos.length}</b> alumnos ya podrían comprarlo hoy.`
                : 'Escribe un precio.';

            // Disponibilidad
            $('[data-ayuda-stock]', form).textContent = stock === null
                ? 'Nunca se agota. Ideal para privilegios y premios digitales.'
                : stock === 0 ? 'Se mostrará como AGOTADO hasta que agregues piezas.'
                    : stock <= 3 ? 'Con 3 o menos, los alumnos verán «¡Últimas piezas!».' : 'Baja sola con cada compra; si cancelas una compra, la pieza regresa.';
            $('[data-ayuda-limite]', form).textContent = limite === null
                ? 'Un alumno puede comprarlo las veces que quiera (si le alcanzan las monedas).'
                : `Cada alumno podrá comprarlo máximo ${limite} ${limite === 1 ? 'vez' : 'veces'}.`;
            const rango = rangoDeNivel(nivel);
            $$('[data-nivel]', form).forEach(b => b.classList.toggle('activo', b.dataset.nivel === String(nivel)));
            $('[data-ayuda-nivel]', form).innerHTML = nivel <= 1
                ? 'Todos los alumnos pueden comprarlo.'
                : `Solo alumnos de nivel ${nivel} en adelante (${rango ? `${rango.emoji} ${rango.nombre}` : ''}). Los demás lo verán con candado 🔒.`;

            // Entrega
            const avatar = tipo() === 'avatar';
            $('[data-bloque-entrega]', form).classList.toggle('d-none', avatar);
            $('[data-ayuda-entrega]', form).textContent = checkEntrega.checked
                ? 'Aparecerá en Pedidos y tú lo marcas como entregado. El alumno lo verá como «Por recibir».'
                : 'El alumno lo recibe al instante al comprarlo; no pasa por Pedidos.';

            // Vista previa
            const producto = $('[data-producto]', form);
            producto.dataset.tipo = tipo();
            producto.classList.toggle('destacado', checkDestacado.checked);
            const conImagen = imagenPrevia.getAttribute('src') && !imagenPrevia.classList.contains('d-none');
            const imgPrevia = $('[data-previa-imagen]', form);
            imgPrevia.classList.toggle('d-none', !conImagen);
            if (conImagen) imgPrevia.src = imagenPrevia.src;
            $('[data-previa-emoji]', form).classList.toggle('d-none', !!conImagen);
            $('[data-previa-emoji]', form).textContent = info.emoji;
            $('[data-previa-precio]', form).textContent = precio;
            const tipoChip = { fisico: ['fisico', '🎁 Físico'], permiso: ['privilegio', '🎟️ Privilegio en clase'],
                avatar: ['digital', '💻 Digital · Avatar'], otro: ['digital', '💻 Digital'] }[tipo()];
            const entregaChip = avatar ? '✨ Se equipa al instante'
                : tipo() === 'fisico' ? '🤝 Te lo entrega el profe'
                    : checkEntrega.checked ? (tipo() === 'permiso' ? '🤝 El profe lo autoriza' : '🤝 El profe lo activa')
                        : '⚡ Lo recibes al instante';
            $('[data-previa-tipo]', form).innerHTML =
                `<span class="chip-tipo ${tipoChip[0]}">${tipoChip[1]}</span><span class="chip-entrega">${entregaChip}</span>`;
            $('[data-previa-nombre]', form).textContent = inputNombre.value.trim() || 'Nombre del premio';
            $('[data-previa-desc]', form).textContent = inputDesc.value.trim() || info.descPh.replace('Ej. ', '');
            const etiquetas = [];
            if (checkDestacado.checked) etiquetas.push('<span class="etq oro">🌟 Destacado</span>');
            if (stock !== null && stock > 0 && stock <= 3) etiquetas.push(`<span class="etq rojo">🔥 ¡Últimas ${stock}!</span>`);
            if (nivel > 1) etiquetas.push(`<span class="etq morado">🔒 Nivel ${nivel}</span>`);
            $('[data-previa-etiquetas]', form).innerHTML = etiquetas.join('');
            $('[data-previa-agotado]', form).classList.toggle('d-none', stock !== 0);
            const lineas = [];
            if (stock !== null && stock > 0) lineas.push(`📦 Quedan ${stock} pieza${stock === 1 ? '' : 's'}`);
            if (limite) lineas.push(`🎯 Máximo ${limite} por alumno`);
            $('[data-previa-stock]', form).innerHTML = lineas.join('<br>');
            const boton = $('[data-previa-boton]', form);
            boton.classList.toggle('bloqueado', stock === 0);
            boton.innerHTML = stock === 0 ? '<i class="bi bi-emoji-frown"></i> Agotado' : '<i class="bi bi-bag-check-fill"></i> Comprar';
            $('[data-previa-flujo]', form).innerHTML = avatar
                ? '🤖 Se equipa al instante como su nueva foto de perfil.'
                : checkEntrega.checked
                    ? '📦 Se descuentan las monedas, aparece en tus <b>Pedidos</b> y el alumno lo ve en su mochila como «Por recibir».'
                    : '⚡ Se descuentan las monedas y el alumno lo ve como «Recibido» en su mochila.';
            $('[data-previa-oculto]', form).classList.toggle('d-none', checkActivo.checked);

            const pasos = $$('.paso', form);
            pasos.forEach(p => p.classList.add('completo'));
            pasos[1]?.classList.toggle('completo', !!(inputNombre.value.trim() && inputDesc.value.trim() && (!avatar || conImagen)));
            pasos[2]?.classList.toggle('completo', precio > 0);
        }

        $$('input[name=tipo]', form).forEach(r => r.addEventListener('change', () => aplicarTipo(true)));
        $$('[data-modo-stock]', form).forEach(b => b.addEventListener('click', () => {
            tocado.stock = true;
            ponerStock(b.dataset.modoStock);
            pintarSegmentos();
            if (modoStock === 'limitado') inputStock.focus();
            actualizar();
        }));
        $$('[data-modo-limite]', form).forEach(b => b.addEventListener('click', () => {
            tocado.limite = true;
            ponerLimite(b.dataset.modoLimite);
            pintarSegmentos();
            if (modoLimite === 'limitado') inputLimite.focus();
            actualizar();
        }));
        $$('[data-precio]', form).forEach(b => b.addEventListener('click', () => { inputPrecio.value = b.dataset.precio; actualizar(); }));
        $$('[data-nivel]', form).forEach(b => b.addEventListener('click', () => { inputNivel.value = b.dataset.nivel; actualizar(); }));
        inputStock.addEventListener('input', () => { tocado.stock = true; });
        inputLimite.addEventListener('input', () => { tocado.limite = true; });
        checkEntrega.addEventListener('change', () => { tocado.entrega = true; });
        inputImagen?.addEventListener('change', () => {
            const archivo = inputImagen.files[0];
            if (!archivo) return;
            const lector = new FileReader();
            lector.onload = e => { imagenPrevia.src = e.target.result; imagenPrevia.classList.remove('d-none'); actualizar(); };
            lector.readAsDataURL(archivo);
        });
        form.querySelector('input[name$="-clear"]')?.addEventListener('change', e => {
            imagenPrevia.classList.toggle('d-none', e.target.checked);
        });
        form.addEventListener('input', actualizar);
        form.addEventListener('change', actualizar);

        form.antesDeEnviar = () => {
            if (tipo() === 'avatar' && (!imagenPrevia.getAttribute('src') || imagenPrevia.classList.contains('d-none'))) {
                toast('Los avatares necesitan una imagen (paso 2)', 'warning');
                return false;
            }
            if (modoStock === 'limitado' && inputStock.value === '') inputStock.value = '0';
            if (modoLimite === 'limitado' && inputLimite.value === '') inputLimite.value = '1';
            return true;
        };

        aplicarTipo(false);
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
            try {
                iniciarFormMision(contenido);
                iniciarFormLogro(contenido);
                iniciarFormDiaria(contenido);
                iniciarFormArticulo(contenido);
            } catch (err) {
                console.error('Error al preparar el formulario', err);
            }
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
            let html;
            try {
                const r = await fetch(url, { headers: cabeceras });
                if (!r.ok || r.redirected) throw new Error('sin modal');
                html = await r.text();
            } catch (e) {
                location.href = url;
                return;
            }
            pintar(html);
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
        iniciarFormLogro();
        iniciarFormDiaria();
        iniciarFormArticulo();
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

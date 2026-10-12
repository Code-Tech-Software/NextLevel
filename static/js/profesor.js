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
        juego: {
            emoji: '🎮', nombre: 'Minijuego', icono: 'bi-controller', colores: ['#f97316', '#c2410c'],
            instrucciones: 'Instrucciones del juego', nombrePh: 'Ej. Lluvia de meteoros',
            placeholder: 'Ej. Escribe las partes de la computadora para destruir los meteoros.',
            imagen: 'Imagen de apoyo', auto: true,
            explica: 'El alumno juega dentro de la misión y <b>se califica solo</b> con su resultado. Con la mitad de la meta la supera (⭐) y puede volver a jugar para ganar más estrellas.',
            flujo: ['Presiona «¡Jugar!» dentro de la misión', 'Recibe su calificación al terminar', 'Puede repetir para mejorar sus estrellas'],
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

        // ----- Minijuego: al elegirlo se proponen nombre e instrucciones -----
        const selJuego = campo('juego');
        let juegos = {};
        try { juegos = JSON.parse($('#juegos-mision-data', form).textContent); } catch (e) { /* sin juegos */ }
        selJuego?.addEventListener('change', () => {
            const j = juegos[selJuego.value];
            if (!j) return;
            const nombre = campo('nombre');
            const descripcion = campo('descripcion');
            if (!nombre.value.trim()) nombre.value = j.nombre;
            if (!descripcion.value.trim()) descripcion.value = j.descripcion;
            $('[data-ayuda-juego]', form).innerHTML = `${escapar(j.icono)} <b>Meta:</b> ${escapar(j.meta)}. Con la mitad de la meta supera la misión.`;
            form.dispatchEvent(new Event('input', { bubbles: true }));
        });
        if (selJuego?.value && juegos[selJuego.value]) {
            const j = juegos[selJuego.value];
            $('[data-ayuda-juego]', form).innerHTML = `${escapar(j.icono)} <b>Meta:</b> ${escapar(j.meta)}. Con la mitad de la meta supera la misión.`;
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
        juegos: { pregunta: '¿Cuántas partidas de minijuegos debe jugar?', unidad: 'partidas', sugerencias: [5, 10, 25, 50], texto: n => n === 1 ? 'Juega tu primer minijuego' : `Juega ${n} partidas de minijuegos` },
        ppm: { pregunta: '¿Cuántas palabras por minuto en Mecanografía?', unidad: 'ppm', sugerencias: [15, 20, 30, 40], texto: n => `Escribe ${n} palabras por minuto en Mecanografía` },
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
        juegos: { pregunta: '¿Cuántas partidas debe jugar hoy?', unidad: 'partidas', sugerencias: [1, 2, 3],
            titulo: 'Hora del Arcade', icono: '🎮', texto: n => n === 1 ? 'Juega una partida de minijuegos' : `Juega ${n} partidas de minijuegos`,
            explica: 'Cuenta cada <b>partida terminada</b> de un minijuego, ya sea en una misión del mapa o en el Arcade.' },
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

    // ---------- Formularios guiados: piezas compartidas ----------
    function avisarCambio(form) { form.dispatchEvent(new Event('input', { bubbles: true })); }
    function leerJSON(form, id, defecto) {
        try { return JSON.parse($(`#${id}`, form).textContent); } catch (e) { return defecto; }
    }
    function plural(n, uno, varios) { return `${n} ${n === 1 ? uno : varios}`; }

    // Botones que escriben un valor en un campo: data-poner="campo" data-valor="..."
    function enlazarAtajos(form) {
        form.addEventListener('click', e => {
            const boton = e.target.closest('[data-poner]');
            if (!boton || !form.contains(boton)) return;
            const input = form.querySelector(`[name="${boton.dataset.poner}"]`);
            if (!input) return;
            input.value = boton.dataset.valor;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        });
    }
    function marcarAtajos(form) {
        $$('[data-poner]', form).forEach(b => {
            const input = form.querySelector(`[name="${b.dataset.poner}"]`);
            if (input) b.classList.toggle('activo', normalizar(input.value.trim()) === normalizar(b.dataset.valor));
        });
    }
    function marcarPasos(form, estados) {
        $$('.paso', form).forEach((paso, i) => paso.classList.toggle('completo', estados[i] !== false));
    }
    function pintarIconos(contenedor, campo, iconos) {
        contenedor.innerHTML = iconos.map(i =>
            `<button type="button" class="icono-op" data-poner="${campo}" data-valor="${i}" aria-label="${i}">${i}</button>`).join('');
    }

    // «Lugar»: al inicio, después de cada hermano o al final (la vista renumera 1, 2, 3...)
    function llenarPosicion(select, hermanos, puedeMantener) {
        const previo = select.value || select.dataset.inicial || '';
        select.dataset.inicial = '';
        const opciones = puedeMantener ? [['mantener', 'Dejar donde está']] : [];
        if (hermanos.length) {
            opciones.push(['inicio', 'Al inicio']);
            hermanos.forEach(h => opciones.push([`despues:${h.id}`, `Después de «${h.nombre}»`]));
            opciones.push(['final', 'Al final']);
        } else {
            opciones.push(['final', 'Es el primero']);
        }
        select.innerHTML = opciones.map(([valor, texto]) => `<option value="${valor}">${escapar(texto)}</option>`).join('');
        select.value = opciones.some(([valor]) => valor === previo) ? previo : (puedeMantener ? 'mantener' : 'final');
    }
    function ordenConPosicion(hermanos, posicion, actual, indiceOriginal = 0) {
        const lista = hermanos.slice();
        let indice = lista.length;
        if (posicion === 'inicio') indice = 0;
        else if (posicion === 'mantener') indice = Math.min(indiceOriginal, lista.length);
        else if (posicion.startsWith('despues:')) {
            const k = lista.findIndex(h => `despues:${h.id}` === posicion);
            if (k >= 0) indice = k + 1;
        }
        lista.splice(indice, 0, actual);
        return lista;
    }

    // ---------- Clase ----------
    function iniciarFormClase(raiz = document) {
        const form = $('form[data-form="clase"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const [nombre, grado, grupo, anio, icono, activa] = ['nombre', 'grado', 'grupo', 'anio', 'icono', 'activa'].map(campo);
        const existentes = leerJSON(form, 'clases-existentes', []);

        function actualizar() {
            const color = $('input[name=color]:checked', form);
            const portal = $('[data-portal]', form);
            if (color) {
                portal.style.setProperty('--c1', color.dataset.c1);
                portal.style.setProperty('--c2', color.dataset.c2);
            }
            $('[data-previa-icono]', form).textContent = icono.value.trim() || '🚀';
            $('[data-previa-grado]', form).textContent = `${grado.value.trim()} ${grupo.value.trim().toUpperCase()}`.trim() || 'Grado y grupo';
            $('[data-previa-nombre]', form).textContent = nombre.value.trim() || 'Nombre de la clase';
            $('[data-previa-oculta]', form).classList.toggle('d-none', activa.checked);
            $('[data-ayuda-activa]', form).textContent = activa.checked
                ? 'Tus alumnos la ven en el lobby y pueden entrar.'
                : 'No aparecerá en el lobby. Útil para grupos de años pasados: su progreso se conserva.';
            const repetida = !!nombre.value.trim() && existentes.some(c =>
                normalizar(c.nombre) === normalizar(nombre.value.trim()) && normalizar(c.grado) === normalizar(grado.value.trim())
                && normalizar(c.grupo) === normalizar(grupo.value.trim()) && String(c.anio) === anio.value.trim());
            $('[data-aviso-duplicado]', form).classList.toggle('d-none', !repetida);
            marcarAtajos(form);
            marcarPasos(form, [!!(nombre.value.trim() && grado.value.trim() && grupo.value.trim() && anio.value.trim()),
                !!(icono.value.trim() && color)]);
        }

        enlazarAtajos(form);
        form.addEventListener('input', actualizar);
        form.addEventListener('change', actualizar);
        actualizar();
    }

    // ---------- Mundo ----------
    function iniciarFormMundo(raiz = document) {
        const form = $('form[data-form="mundo"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const selClase = campo('clase');
        const nombre = campo('nombre');
        const desc = campo('descripcion');
        const selPosicion = $('[data-posicion]', form);
        const temas = leerJSON(form, 'temas-data', {});
        const porClase = leerJSON(form, 'mundos-clase-data', {});
        const mundoId = form.dataset.mundo;
        const claseInicial = form.dataset.claseInicial;
        const tema = () => $('input[name=tema]:checked', form)?.value || 'bosque';
        const sugeridos = Object.values(temas).flatMap(t => t.nombres || []);
        const esSugerido = () => !nombre.value.trim() || sugeridos.includes(nombre.value.trim());
        let nombreSugerido = !mundoId && esSugerido();
        let indiceOriginal = 0;

        const hermanos = () => (porClase[selClase.value] || []).filter(m => String(m.id) !== mundoId);

        // Las sugerencias que ya son nombre de otro mundo de la clase no se proponen
        const usado = n => hermanos().some(m => normalizar(m.nombre) === normalizar(n));
        function pintarSugerencias() {
            const nombres = temas[tema()]?.nombres || [];
            $('[data-sugerencias-nombre]', form).innerHTML = nombres.map(n => usado(n)
                ? `<button type="button" disabled title="Ya hay un mundo con este nombre">${escapar(n)}</button>`
                : `<button type="button" data-poner="nombre" data-valor="${escapar(n)}">${escapar(n)}</button>`).join('');
        }
        function alCambiarClase() {
            const lista = porClase[selClase.value] || [];
            indiceOriginal = Math.max(0, lista.findIndex(m => String(m.id) === mundoId));
            llenarPosicion(selPosicion, hermanos(), !!mundoId && selClase.value === claseInicial);
            pintarSugerencias();
            actualizar();
        }
        function alCambiarTema() {
            pintarSugerencias();
            const libre = (temas[tema()]?.nombres || []).find(n => !usado(n));
            if (nombreSugerido && libre) nombre.value = libre;
            actualizar();
        }
        function actualizar() {
            const info = temas[tema()] || {};
            $('[data-previa-mundo]', form).className = `mundo-previa tema-${tema()}`;
            $('[data-previa-isla]', form).textContent = info.emoji || '🌍';
            $('[data-previa-decos]', form).innerHTML = (info.decos || []).slice(0, 4).map(d => `<span>${d}</span>`).join('');
            $('[data-previa-nombre]', form).textContent = nombre.value.trim() || 'Nombre del mundo';
            $('[data-previa-desc]', form).textContent = desc.value.trim();
            const actual = { id: 'actual', nombre: nombre.value.trim() || 'Nuevo mundo', emoji: info.emoji, actual: true };
            const orden = selClase.value ? ordenConPosicion(hermanos(), selPosicion.value || 'final', actual, indiceOriginal) : [actual];
            $('[data-previa-numero]', form).textContent = `Mundo ${orden.indexOf(actual) + 1}`;
            $('[data-previa-orden]', form).innerHTML = orden.map((m, i) =>
                `${i ? '<i class="bi bi-chevron-right"></i>' : ''}<span class="${m.actual ? 'actual' : ''}">${m.emoji || '🌍'} ${escapar(m.nombre)}</span>`).join('');
            marcarAtajos(form);
            marcarPasos(form, [!!selClase.value, true, !!nombre.value.trim()]);
        }

        enlazarAtajos(form);
        selClase.addEventListener('change', alCambiarClase);
        selPosicion.addEventListener('change', actualizar);
        $$('input[name=tema]', form).forEach(r => r.addEventListener('change', alCambiarTema));
        nombre.addEventListener('input', () => { nombreSugerido = esSugerido(); });
        form.addEventListener('input', actualizar);
        alCambiarClase();
    }

    // ---------- Nivel ----------
    function iniciarFormNivel(raiz = document) {
        const form = $('form[data-form="nivel"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const selMundo = campo('mundo');
        const nombre = campo('nombre');
        const cofre = campo('recompensa_cofre');
        const selPosicion = $('[data-posicion]', form);
        const mundos = leerJSON(form, 'mundos-data', {});
        const nivelId = form.dataset.nivel;
        const mundoInicial = form.dataset.mundoInicial;
        // En niveles nuevos el nombre «Nivel N» sigue a la posición mientras no lo cambies
        let nombreSugerido = !nivelId && (!nombre.value.trim() || /^Nivel \d+$/.test(nombre.value.trim()));
        let indiceOriginal = 0;

        const hermanos = () => (mundos[selMundo.value]?.niveles || []).filter(n => String(n.id) !== nivelId);

        function alCambiarMundo() {
            const mundo = mundos[selMundo.value];
            const lista = mundo?.niveles || [];
            indiceOriginal = Math.max(0, lista.findIndex(n => String(n.id) === nivelId));
            llenarPosicion(selPosicion, hermanos(), !!nivelId && selMundo.value === mundoInicial);
            $('[data-ayuda-mundo]', form).textContent = mundo
                ? `${mundo.clase} · ya tiene ${plural(hermanos().length, 'nivel', 'niveles')}` : '';
            actualizar();
        }
        function actualizar() {
            const mundo = mundos[selMundo.value];
            const actual = { id: 'actual', nombre: '', actual: true };
            const lista = ordenConPosicion(hermanos(), selPosicion.value || 'final', actual, indiceOriginal);
            const numero = lista.indexOf(actual) + 1;
            if (nombreSugerido) nombre.value = `Nivel ${numero}`;
            actual.nombre = nombre.value.trim() || 'Nuevo nivel';
            const base = Math.max(1, parseInt(cofre.value, 10) || 1);
            const minimo = Math.max(1, Math.floor(base * 0.6));
            const maximo = Math.floor(base * 1.5) + 1;
            $('[data-ayuda-cofre]', form).innerHTML = `🎁 Cuando un alumno termina todas las misiones del nivel, abre el cofre y gana <b>entre ${minimo} y ${maximo} monedas</b> al azar. ¡La sorpresa es parte de la diversión!`;
            $('[data-previa-camino]', form).className = `camino-previa${mundo ? ` tema-${mundo.tema}` : ''}`;
            $('[data-previa-mundo]', form).textContent = mundo ? `${mundo.emoji} ${mundo.nombre}` : 'Elige un mundo';
            $('[data-previa-paradas]', form).innerHTML = mundo ? lista.map((n, i) => `
                ${i ? '<div class="tramo"></div>' : ''}
                <div class="parada ${n.actual ? 'nueva' : ''}">
                    <span class="nodo">${i + 1}</span>
                    <span class="t">${escapar(n.nombre)}</span>
                    ${n.actual ? `<span class="cofre">🎁 ${minimo}–${maximo}</span>` : ''}
                </div>`).join('') : '<div class="vacio">El camino aparecerá aquí.</div>';
            marcarAtajos(form);
            marcarPasos(form, [!!mundo, !!nombre.value.trim(), cofre.value !== '' && base >= 1]);
        }

        enlazarAtajos(form);
        selMundo.addEventListener('change', alCambiarMundo);
        selPosicion.addEventListener('change', actualizar);
        nombre.addEventListener('input', e => { if (e.isTrusted) nombreSugerido = false; });
        $('[data-sugerir-nombre]', form).addEventListener('click', () => { nombreSugerido = true; actualizar(); avisarCambio(form); });
        form.addEventListener('input', actualizar);
        alCambiarMundo();
    }

    // ---------- Alumno ----------
    const PINES_FACILES = ['1234', '4321', '0123', '2580', '1212', '1122', '9876', '6789', '0987', '1004'];
    const pinFacil = pin => /^(\d)\1{3}$/.test(pin) || PINES_FACILES.includes(pin);
    function pinAlAzar() {
        let pin;
        do { pin = String(Math.floor(Math.random() * 10000)).padStart(4, '0'); } while (pinFacil(pin));
        return pin;
    }

    function iniciarFormAlumno(raiz = document) {
        const form = $('form[data-form="alumno"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const nombre = campo('nombre');
        const apellido = campo('apellido');
        const pin = campo('pin');
        const activo = form.querySelector('input[type=checkbox][name="activo"]');
        const inputAvatar = campo('avatar');
        const imagenPrevia = $('[data-imagen-previa]', form);
        const avatarPrevia = $('[data-previa-avatar]', form);

        function actualizar() {
            const limpio = pin.value.replace(/\D/g, '').slice(0, 4);
            if (limpio !== pin.value) pin.value = limpio;
            const faltan = 4 - limpio.length;
            const ayuda = $('[data-ayuda-pin]', form);
            ayuda.className = `ayuda mt-2${faltan ? '' : pinFacil(limpio) ? ' alerta' : ' ok'}`;
            ayuda.textContent = faltan ? `Faltan ${plural(faltan, 'número', 'números')}.`
                : pinFacil(limpio) ? '⚠️ Es muy fácil de adivinar. Mejor usa uno al azar.' : '✓ Listo. Recuérdaselo o imprime su credencial.';
            $('[data-previa-pin]', form).textContent = limpio.padEnd(4, '•');
            $('[data-previa-nombre]', form).textContent = nombre.value.trim() || 'Nombre';
            $('[data-previa-apellido]', form).textContent = apellido.value.trim() || 'Apellidos';
            const clases = $$('input[name=clases]:checked', form).map(c => c.dataset.nombre);
            $('[data-previa-clases]', form).innerHTML = clases.length
                ? clases.map(c => `<span class="p-badge azul me-1 mb-1">${escapar(c)}</span>`).join('')
                : '<span class="text-muted-p">Ninguna clase todavía: elige al menos una.</span>';
            const conFoto = imagenPrevia.getAttribute('src') && !imagenPrevia.classList.contains('d-none');
            avatarPrevia.src = conFoto ? imagenPrevia.src : avatarPrevia.dataset.robot;
            if (activo) {
                $('[data-previa-inactivo]', form).classList.toggle('d-none', activo.checked);
                $('[data-ayuda-activo]', form).textContent = activo.checked
                    ? 'Aparece en el lobby y en los rankings.'
                    : 'Ya no aparece en el lobby ni en los rankings, pero se guarda todo su progreso.';
            }
            marcarPasos(form, [!!(nombre.value.trim() && apellido.value.trim()), clases.length > 0, !faltan, true, true]);
        }

        $('[data-pin-azar]', form).addEventListener('click', () => { pin.value = pinAlAzar(); avisarCambio(form); });
        inputAvatar?.addEventListener('change', () => {
            const archivo = inputAvatar.files[0];
            if (!archivo) return;
            const lector = new FileReader();
            lector.onload = e => { imagenPrevia.src = e.target.result; imagenPrevia.classList.remove('d-none'); actualizar(); };
            lector.readAsDataURL(archivo);
        });
        form.querySelector('input[name$="-clear"]')?.addEventListener('change', e => {
            imagenPrevia.classList.toggle('d-none', e.target.checked);
            actualizar();
        });
        form.addEventListener('input', actualizar);
        form.addEventListener('change', actualizar);
        actualizar();
    }

    // ---------- Alta masiva ----------
    // Igual que separar_nombre() en forms.py: «Ana López» o «López, Ana Sofía»
    function separarNombre(linea) {
        linea = linea.replace(/\t/g, ' ').split(/\s+/).filter(Boolean).join(' ');
        if (linea.includes(',')) {
            const [apellido, ...resto] = linea.split(',');
            const nombre = resto.join(',').trim();
            if (nombre) return [nombre.slice(0, 100), apellido.trim().slice(0, 100)];
            linea = apellido.trim();
        }
        const partes = linea.split(' ');
        return [partes[0].slice(0, 100), partes.slice(1).join(' ').slice(0, 100)];
    }

    function iniciarFormMasiva(raiz = document) {
        const form = $('form[data-form="masiva"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const texto = form.querySelector('[name="nombres"]');
        const pinAleatorio = form.querySelector('[name="pin_aleatorio"]');
        const porClase = leerJSON(form, 'nombres-clase-data', {});

        function actualizar() {
            const clase = $('input[name=clase]:checked', form);
            const existentes = new Set((porClase[clase?.value] || []).map(n => normalizar(n.trim())));
            const vistos = new Set();
            const avisos = { sinApellido: 0, existe: 0, repetido: 0 };
            const filas = texto.value.split('\n').filter(l => l.trim()).map(separarNombre).filter(([n]) => n);
            const html = filas.map(([nombre, apellido], i) => {
                const clave = normalizar(`${nombre} ${apellido}`.trim());
                let etiqueta = '';
                if (existentes.has(clave)) { etiqueta = '<span class="etq">Ya está en la clase</span>'; avisos.existe++; }
                else if (vistos.has(clave)) { etiqueta = '<span class="etq">Repetido</span>'; avisos.repetido++; }
                vistos.add(clave);
                if (!apellido) avisos.sinApellido++;
                const iniciales = (nombre[0] + (apellido[0] || '')).toUpperCase();
                return `<div class="fila"><span class="num">${i + 1}</span><span class="ini">${escapar(iniciales)}</span>
                    <div class="min-w-0"><div class="n text-truncate">${escapar(nombre)}</div>
                    <div class="a text-truncate ${apellido ? '' : 'falta'}">${apellido ? escapar(apellido) : 'Sin apellido'}</div></div>${etiqueta}</div>`;
            }).join('');
            $('[data-previa-lista]', form).innerHTML = html
                || '<div class="vacia">Pega los nombres a la izquierda y aquí verás cómo se registra cada uno.</div>';
            $('[data-previa-total]', form).textContent = filas.length ? `Se registrarán ${plural(filas.length, 'alumno', 'alumnos')}` : 'Así quedarán';
            $('[data-previa-clase]', form).textContent = clase ? `en ${clase.dataset.nombre}` : 'Elige una clase';
            const lineas = [];
            if (avisos.sinApellido) lineas.push(`✏️ ${plural(avisos.sinApellido, 'alumno', 'alumnos')} sin apellido: escríbelo en el mismo renglón.`);
            if (avisos.existe) lineas.push(`👀 ${avisos.existe} ya ${avisos.existe === 1 ? 'está' : 'están'} en esta clase; si los dejas, se registrarán otra vez.`);
            if (avisos.repetido) lineas.push(`🔁 ${plural(avisos.repetido, 'renglón repetido', 'renglones repetidos')}.`);
            const cajaAvisos = $('[data-previa-avisos]', form);
            cajaAvisos.classList.toggle('d-none', !lineas.length);
            cajaAvisos.innerHTML = lineas.join('<br>');
            $('[data-ayuda-pin]', form).textContent = pinAleatorio.checked
                ? 'Cada alumno tendrá un PIN diferente de 4 números (recomendado).'
                : 'Todos tendrán el PIN 0000. Podrás cambiarlo después desde su perfil.';
            $('[data-boton-registrar]', form).innerHTML = `<i class="bi bi-check2"></i> ${filas.length ? `Registrar ${plural(filas.length, 'alumno', 'alumnos')}` : 'Registrar alumnos'}`;
            marcarPasos(form, [!!clase, filas.length > 0, true]);
        }

        form.addEventListener('input', actualizar);
        form.addEventListener('change', actualizar);
        actualizar();
    }

    // ---------- Equipo ----------
    const EQUIPOS_SUGERIDOS = [
        ['Leones', '🦁', 'ambar'], ['Dragones', '🐉', 'coral'], ['Águilas', '🦅', 'cielo'], ['Lobos', '🐺', 'uva'],
        ['Tiburones', '🦈', 'indigo'], ['Fénix', '🔥', 'rosa'], ['Robots', '🤖', 'esmeralda'], ['Cometas', '☄️', 'cielo'],
        ['Pumas', '🐆', 'ambar'], ['Búhos', '🦉', 'uva'],
    ];

    function iniciarFormEquipo(raiz = document) {
        const form = $('form[data-form="equipo"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const selClase = campo('clase');
        const nombre = campo('nombre');
        const emoji = campo('emoji');
        const porClase = leerJSON(form, 'equipos-clase-data', {});
        const colores = Object.fromEntries(leerJSON(form, 'colores-data', []).map(c => [c.valor, c]));
        let colorElegido = !!nombre.value.trim();
        const otros = () => porClase[selClase.value] || [];

        function pintarSugeridos() {
            const usados = new Set(otros().map(e => normalizar(e.nombre)));
            $('[data-sugeridos]', form).innerHTML = EQUIPOS_SUGERIDOS.map(([n, e, c]) => {
                const usado = usados.has(normalizar(n));
                return `<button type="button" class="preset" data-sugerido="${n}" data-emoji="${e}" data-color="${c}" ${usado ? 'disabled title="Ya existe en esta clase"' : ''}>
                    <span class="e">${e}</span><span class="n">${n}</span>${usado ? '<span class="v">ya existe</span>' : ''}</button>`;
            }).join('');
        }
        function actualizar() {
            const color = $('input[name=color]:checked', form);
            const info = color ? colores[color.value] : null;
            const previa = $('[data-previa-equipo]', form);
            if (info) { previa.style.setProperty('--c1', info.c1); previa.style.setProperty('--c2', info.c2); }
            $('[data-previa-escudo]', form).textContent = emoji.value.trim() || '🛡️';
            $('[data-previa-nombre]', form).textContent = nombre.value.trim() || 'Nombre del equipo';
            const lista = otros();
            $('[data-previa-lugar]', form).textContent = !selClase.value ? ''
                : lista.length ? `Compite contra ${plural(lista.length, 'equipo', 'equipos')}` : '¡El primer equipo de la clase!';
            const tabla = lista.length ? [...lista, { nombre: nombre.value.trim() || 'Nuevo equipo', emoji: emoji.value.trim() || '🛡️', color: color?.value, mio: true }] : [];
            $('[data-previa-tabla]', form).innerHTML = tabla.map(e =>
                `<div class="fila ${e.mio ? 'mio' : ''}"><span class="punto-c" style="--pc:${colores[e.color]?.c1 || '#fff'}"></span><span>${escapar(e.emoji)}</span><span class="n text-truncate">${escapar(e.nombre)}</span></div>`).join('');
            $$('[data-usado]', form).forEach(s => {
                const quienes = lista.filter(e => e.color === s.dataset.usado);
                s.textContent = quienes.length ? `usado por ${quienes.map(e => e.emoji).join(' ')}` : '';
            });
            $('[data-ayuda-clase]', form).textContent = !selClase.value ? ''
                : lista.length ? `Equipos actuales: ${lista.map(e => `${e.emoji} ${e.nombre}`).join(' · ')}` : 'Esta clase aún no tiene equipos.';
            $$('[data-sugerido]', form).forEach(b => b.classList.toggle('activo', normalizar(b.dataset.sugerido) === normalizar(nombre.value.trim())));
            marcarAtajos(form);
            marcarPasos(form, [!!selClase.value, !!(nombre.value.trim() && emoji.value.trim()), !!color]);
        }

        form.addEventListener('click', e => {
            const boton = e.target.closest('[data-sugerido]');
            if (!boton || boton.disabled) return;
            nombre.value = boton.dataset.sugerido;
            emoji.value = boton.dataset.emoji;
            // El color del equipo sugerido solo se pone si aún no elegiste uno
            const radio = form.querySelector(`input[name=color][value="${boton.dataset.color}"]`);
            if (!colorElegido && radio) radio.checked = true;
            avisarCambio(form);
        });
        $$('input[name=color]', form).forEach(r => r.addEventListener('change', e => { if (e.isTrusted) colorElegido = true; }));
        selClase.addEventListener('change', pintarSugeridos);
        enlazarAtajos(form);
        form.addEventListener('input', actualizar);
        form.addEventListener('change', actualizar);
        pintarSugeridos();
        actualizar();
    }

    // ---------- Meta del grupo ----------
    const decimal = x => (Math.round(x * 10) / 10).toLocaleString('es-MX');
    const TIPOS_META = {
        misiones: {
            unidad: 'misiones', pregunta: '¿Cuántas misiones aprobadas entre todos?', sugerencias: [10, 20, 30, 50],
            frase: n => `Si entre todos completamos ${n} misiones`, reto: n => `¡Reto de ${n} misiones!`,
            explica: 'Cuenta cada misión que <b>apruebes</b> a cualquier alumno de la clase. Ideal para que todos avancen en el mapa.',
            como: 'El avance sube solo cada vez que apruebas una misión.',
            porAlumno: x => (x < 1 ? 'menos de una misión por alumno' : `unas ${decimal(x)} misiones por alumno`),
        },
        xp: {
            unidad: 'XP', pregunta: '¿Cuánta XP entre todos?', sugerencias: [500, 1000, 2000, 5000],
            frase: n => `Si entre todos juntamos ${n} XP`, reto: n => `¡Reto de ${n} XP!`,
            explica: 'Suma toda la XP que gane la clase: misiones, misiones del día, logros y botones del Modo clase.',
            como: 'El avance sube solo con toda la XP que gane la clase.',
            porAlumno: x => `unos ${Math.max(1, Math.round(x))} XP por alumno (≈ ${plural(Math.max(1, Math.round(x / 50)), 'misión', 'misiones')})`,
        },
        conducta: {
            unidad: 'veces', pregunta: '¿Cuántos comportamientos positivos?', sugerencias: [20, 50, 100, 200],
            frase: n => `Si sumamos ${n} buenas acciones`, reto: n => `¡${n} buenas acciones!`,
            explica: 'Cuenta cada vez que tocas un botón <b>positivo</b> en el Modo clase (participación, ayudar, orden…). Los negativos no restan.',
            como: 'El avance sube cada vez que usas un botón positivo en el Modo clase.',
            porAlumno: x => (x < 1 ? 'menos de una por alumno' : `unas ${decimal(x)} veces por alumno`),
        },
        manual: {
            unidad: 'puntos', pregunta: '¿Hasta cuántos puntos?', sugerencias: [5, 10, 20, 30],
            frase: n => `Si llegamos a ${n} puntos`, reto: n => `¡Reto de ${n} puntos!`,
            explica: 'Tú decides cuándo avanza con los botones <b>+ / −</b> en Metas o en el Modo clase. Sirve para cualquier reto: traer material, leer libros…',
            como: 'Tú sumas el avance con + / − en Metas o en el Modo clase.',
            porAlumno: null,
        },
    };
    const ICONOS_META = ['🎯', '🏆', '🍿', '⚽', '🎵', '🍕', '🎮', '🎨', '🚀', '⭐', '🔥', '💪', '📚', '🌟'];
    const TITULOS_PREMIO = {
        '🍿 Película el viernes': '¡Viernes de película!', '⚽ Recreo extra': '¡Recreo extra para todos!',
        '🎵 Música en clase': '¡Música en clase!', '🍕 Convivio': '¡Gran convivio!',
        '🎮 Clase de juegos': '¡Clase de juegos!', '🎨 Clase libre': '¡Clase libre!',
    };

    function iniciarFormMeta(raiz = document) {
        const form = $('form[data-form="meta"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const selClase = campo('clase');
        const objetivo = campo('objetivo');
        const recompensa = campo('recompensa');
        const monedas = campo('monedas_recompensa');
        const titulo = campo('titulo');
        const icono = campo('icono');
        const desc = campo('descripcion');
        const fecha = campo('fecha_limite');
        const activa = campo('activa');
        const alumnos = leerJSON(form, 'alumnos-clase-data', {});
        const editando = !!form.dataset.editando;
        const progresoGuardado = parseInt(form.dataset.progreso || 0, 10);
        const tipoInicial = $('input[name=tipo]:checked', form)?.value;
        const claseInicial = selClase.value;
        const hoy = new Date(`${form.dataset.hoy}T00:00:00`);
        const tipo = () => $('input[name=tipo]:checked', form)?.value || 'misiones';
        const info = () => TIPOS_META[tipo()];
        const meta = () => Math.max(1, parseInt(objetivo.value, 10) || 1);
        const sugeridos = { titulo: !editando, icono: !editando, descripcion: !editando || !desc.value.trim() };
        const ultimo = { titulo: titulo.value, icono: icono.value, descripcion: desc.value };

        function propuesta() {
            const premio = recompensa.value.trim();
            const emojiPremio = premio.match(/^\p{Extended_Pictographic}️?/u)?.[0];
            return {
                titulo: TITULOS_PREMIO[premio] || info().reto(meta()),
                icono: emojiPremio || '🎯',
                descripcion: `${info().frase(meta())}, ${premio ? `ganamos: ${premio}` : '¡lo celebramos!'}`,
            };
        }
        function proponer(forzar = false) {
            const valores = propuesta();
            const inputs = { titulo, icono, descripcion: desc };
            Object.keys(valores).forEach(clave => {
                if (forzar || sugeridos[clave]) {
                    inputs[clave].value = valores[clave].slice(0, inputs[clave].maxLength > 0 ? inputs[clave].maxLength : 200);
                    ultimo[clave] = inputs[clave].value;
                    sugeridos[clave] = true;
                }
            });
        }
        function aplicarTipo() {
            const i = info();
            const explicacion = $('[data-explicacion-tipo]', form);
            explicacion.classList.remove('d-none');
            explicacion.innerHTML = `<span class="e">${$('input[name=tipo]:checked', form)?.nextElementSibling.querySelector('.e').textContent || '🎯'}</span><div>${i.explica}</div>`;
            $('[data-pregunta-objetivo]', form).textContent = i.pregunta;
            $('[data-unidad-objetivo]', form).textContent = i.unidad;
            $('[data-sugerencias-objetivo]', form).innerHTML = i.sugerencias.map(n =>
                `<button type="button" data-poner="objetivo" data-valor="${n}">${n}</button>`).join('');
            actualizar();
        }
        // Fecha local (AAAA-MM-DD) dentro de N días; toISOString() la pasaría a UTC
        function enDias(n) {
            const d = new Date(hoy);
            d.setDate(d.getDate() + n);
            return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
        }
        function diasRestantes() {
            if (!fecha.value) return null;
            return Math.round((new Date(`${fecha.value}T00:00:00`) - hoy) / 86400000);
        }
        function actualizar() {
            const i = info();
            const n = meta();
            proponer();
            const totalAlumnos = alumnos[selClase.value] || 0;
            const mismoConteo = editando && tipo() === tipoInicial && selClase.value === claseInicial;
            const progreso = mismoConteo ? progresoGuardado : 0;
            const ayuda = [];
            if (!selClase.value) ayuda.push('Elige la clase para calcular cuánto le toca a cada alumno.');
            else if (!totalAlumnos) ayuda.push('Esta clase aún no tiene alumnos activos.');
            else if (i.porAlumno) ayuda.push(`👥 Con ${plural(totalAlumnos, 'alumno', 'alumnos')} son ${i.porAlumno(n / totalAlumnos)}.`);
            else ayuda.push(`👥 ${plural(totalAlumnos, 'alumno', 'alumnos')} en la clase.`);
            if (mismoConteo) ayuda.push(`📈 Llevan <b>${progreso} de ${n}</b>.`);
            $('[data-ayuda-objetivo]', form).innerHTML = ayuda.join('<br>');

            // Plazo
            const dias = diasRestantes();
            $$('[data-dias]', form).forEach(b => {
                const esperado = b.dataset.dias === '' ? '' : enDias(parseInt(b.dataset.dias, 10));
                b.classList.toggle('activo', fecha.value === esperado);
            });

            // Vista previa
            const lograda = progreso >= n;
            $('[data-previa-meta]', form).classList.toggle('lograda', lograda);
            $('[data-previa-icono]', form).textContent = icono.value.trim() || '🎯';
            $('[data-previa-titulo]', form).textContent = titulo.value.trim() || 'Nombre de la meta';
            $('[data-previa-desc]', form).textContent = desc.value.trim();
            $('[data-previa-barra]', form).style.width = `${Math.min(100, Math.round(progreso * 100 / n))}%`;
            $('[data-previa-avance]', form).textContent = lograda ? '¡Lo lograron entre todos!' : `${progreso} de ${n} · ¡faltan ${n - progreso}!`;
            $('[data-previa-dias]', form).textContent = dias === null || lograda ? '' : dias > 0 ? `⏰ ${plural(dias, 'día', 'días')}` : dias === 0 ? '⏰ ¡Último día!' : '⏰ Ya venció';
            const m = parseInt(monedas.value, 10) || 0;
            const premio = recompensa.value.trim();
            $('[data-previa-premio]', form).textContent = premio || m
                ? `Premio: ${premio}${premio && m ? ' · ' : ''}${m ? `+${m} monedas para todos` : ''}` : '';
            $('[data-previa-oculta]', form).classList.toggle('d-none', activa.checked);
            $('[data-previa-como]', form).textContent = i.como;
            $('[data-previa-celebra]', form).textContent = `Al llegar al objetivo, toda la clase recibe una notificación de celebración${m ? ` y +${m} monedas cada uno` : ''}.`;
            $('[data-ayuda-activa]', form).textContent = activa.checked ? 'Aparece en el mapa de cada alumno.' : 'Guárdala oculta y actívala cuando quieras.';
            marcarAtajos(form);
            marcarPasos(form, [true, !!selClase.value && !!objetivo.value, !!(premio || m), !!titulo.value.trim(), true]);
        }

        enlazarAtajos(form);
        pintarIconos($('[data-iconos-meta]', form), 'icono', ICONOS_META);
        $$('input[name=tipo]', form).forEach(r => r.addEventListener('change', aplicarTipo));
        [['titulo', titulo], ['icono', icono], ['descripcion', desc]].forEach(([clave, input]) =>
            input.addEventListener('input', () => { sugeridos[clave] = input.value === ultimo[clave]; }));
        $('[data-sugerir-titulo]', form).addEventListener('click', () => { proponer(true); actualizar(); avisarCambio(form); });
        $$('[data-dias]', form).forEach(b => b.addEventListener('click', () => {
            fecha.value = b.dataset.dias === '' ? '' : enDias(parseInt(b.dataset.dias, 10));
            avisarCambio(form);
        }));
        form.addEventListener('input', actualizar);
        form.addEventListener('change', actualizar);
        aplicarTipo();
    }

    // ---------- Botón del modo clase ----------
    const IDEAS_CONDUCTA = {
        positivo: [['🙋', 'Participación'], ['🤝', 'Ayudó a un compañero'], ['⭐', 'Excelente trabajo'], ['🧹', 'Dejó todo ordenado'],
            ['⏰', 'Puntualidad'], ['💡', 'Idea creativa'], ['🎧', 'Escuchó con atención'], ['🏅', 'Esfuerzo extra']],
        negativo: [['📱', 'Uso del celular'], ['🗣️', 'Interrumpir'], ['⌛', 'Llegó tarde'], ['📝', 'Sin tarea'],
            ['🧃', 'Comer en clase'], ['🙅', 'Falta de respeto']],
    };
    const ICONOS_CONDUCTA = {
        positivo: ['⭐', '🙋', '🤝', '🧹', '⏰', '💡', '🎧', '🏅', '👏', '🔥', '🧠', '💪', '🎯', '🌟'],
        negativo: ['📱', '🗣️', '⌛', '📝', '🧃', '🙅', '⚠️', '😴', '🔇', '🚫'],
    };

    function iniciarFormConducta(raiz = document) {
        const form = $('form[data-form="conducta"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const nombre = campo('nombre');
        const icono = campo('icono');
        const monedas = campo('monedas');
        const xp = campo('xp');
        const activo = campo('activo');
        const selPosicion = $('[data-posicion]', form);
        const otros = leerJSON(form, 'conductas-data', []);
        const editando = !!form.dataset.editando;
        const polaridad = () => $('input[name=polaridad]:checked', form)?.value || 'positivo';
        const polaridadInicial = polaridad();
        // Mientras nombre e ícono vengan de una idea, cambian solos al pasar de «suma» a «resta»
        let deIdea = false;

        function alCambiarPolaridad(cambio) {
            const p = polaridad();
            $('[data-ideas]', form).innerHTML = IDEAS_CONDUCTA[p].map(([e, n]) =>
                `<button type="button" data-idea="${escapar(n)}" data-emoji="${e}">${e} ${escapar(n)}</button>`).join('');
            pintarIconos($('[data-iconos-conducta]', form), 'icono', ICONOS_CONDUCTA[p]);
            if (cambio && deIdea) {
                [icono.value, nombre.value] = IDEAS_CONDUCTA[p][0];
            }
            // En el Modo clase los positivos y los negativos van en pestañas separadas
            const hermanos = otros.filter(o => o.positivo === (p === 'positivo'));
            llenarPosicion(selPosicion, hermanos, editando && p === polaridadInicial);
            actualizar();
        }
        function actualizar() {
            const negativo = polaridad() === 'negativo';
            const cantidad = Math.abs(parseInt(monedas.value, 10) || 0);
            const puntos = negativo ? 0 : (parseInt(xp.value, 10) || 0);
            const signo = negativo ? '−' : '+';
            $('[data-signo]', form).textContent = signo;
            $('[data-signo]', form).classList.toggle('neg', negativo);
            $('[data-label-monedas]', form).textContent = negativo ? 'Monedas que quita' : 'Monedas que da';
            $('[data-bloque-xp]', form).classList.toggle('d-none', negativo);
            $('[data-sub-valor]', form).textContent = negativo
                ? 'Que sea un recordatorio, no un castigo: 1 a 3 monedas suele bastar.'
                : 'Valores pequeños funcionan mejor: se usan muchas veces al día.';
            const icon = icono.value.trim() || (negativo ? '⚠️' : '⭐');
            const texto = nombre.value.trim() || 'Nombre';
            $('[data-previa-boton]', form).className = `mc-conducta ${negativo ? 'neg' : 'pos'}`;
            $('[data-previa-icono]', form).textContent = icon;
            $('[data-previa-nombre]', form).textContent = texto;
            $('[data-previa-valor]', form).innerHTML = `${signo}${cantidad} <i class="bi bi-coin"></i>${puntos ? ` · +${puntos} XP` : ''}`;
            $('[data-previa-aviso]', form).innerHTML = `<span class="e">${escapar(icon)}</span><div class="min-w-0"><b>Ana López</b> · ${escapar(texto)}
                <b class="${negativo ? 'neg' : 'pos'}">${signo}${cantidad} 🪙${puntos ? ` +${puntos} XP` : ''}</b>
                <div style="font-size:.72rem;opacity:.75">Aviso al tocar el botón, con opción de deshacer</div></div>`;
            $('[data-previa-oculto]', form).classList.toggle('d-none', activo.checked);
            $('[data-ayuda-activo]', form).textContent = activo.checked ? 'Aparece en el Modo clase.' : 'Queda guardado, pero no aparece en el Modo clase.';
            $$('[data-idea]', form).forEach(b => b.classList.toggle('activo', b.dataset.idea === nombre.value.trim()));
            marcarAtajos(form);
            marcarPasos(form, [true, !!nombre.value.trim(), cantidad > 0, true]);
        }

        form.addEventListener('click', e => {
            const boton = e.target.closest('[data-idea]');
            if (!boton) return;
            nombre.value = boton.dataset.idea;
            icono.value = boton.dataset.emoji;
            deIdea = true;
            avisarCambio(form);
        });
        [nombre, icono].forEach(input => input.addEventListener('input', e => { if (e.isTrusted) deIdea = false; }));
        $$('input[name=polaridad]', form).forEach(r => r.addEventListener('change', () => alCambiarPolaridad(true)));
        enlazarAtajos(form);
        form.addEventListener('input', actualizar);
        form.addEventListener('change', actualizar);
        alCambiarPolaridad(false);
    }

    // ---------- Juego (minijuego configurable, con «Probar») ----------
    const NOMBRES_CONJUNTO = {
        central: 'fila guía', superior: 'fila de arriba', inferior: 'fila de abajo', letras: 'todas las letras',
        numeros: 'números', todo: 'letras y números', personalizado: 'mis teclas',
    };

    function iniciarFormJuego(raiz = document) {
        const form = $('form[data-form="juego"]', raiz);
        if (!form || form.dataset.listo) return;
        form.dataset.listo = '1';
        const campo = nombre => form.querySelector(`[name="${nombre}"]`);
        const plantillas = leerJSON(form, 'plantillas-juego-data', {});
        const temas = leerJSON(form, 'temas-juego-data', {});
        const conjuntos = leerJSON(form, 'conjuntos-juego-data', {});
        const velocidades = leerJSON(form, 'velocidades-juego-data', {});
        const temasClasifica = leerJSON(form, 'temas-clasifica-data', {});
        const catalogoAtajos = leerJSON(form, 'atajos-juego-data', {});
        const gruposAtajos = leerJSON(form, 'grupos-atajos-data', {});
        const cifrados = leerJSON(form, 'cifrados-data', {});
        const frasesFormato = leerJSON(form, 'frases-formato-data', []);
        const dificultades = leerJSON(form, 'dificultades-robot-data', {});
        const editando = !!form.dataset.editando;
        const plantilla = () => $('input[name=plantilla]:checked', form)?.value || 'meteoros';
        const palabrasInput = campo('palabras');
        const metaInput = campo('meta');
        const nombre = campo('nombre');
        const icono = campo('icono');
        const enArcade = campo('en_arcade');
        const agregarMapa = campo('agregar_mapa');
        // Meta, nombre e ícono siguen a la configuración mientras no los cambies a mano
        let metaSugerida = !editando || !metaInput.value;
        let nombreSugerido = !editando;
        let iconoSugerido = !editando;

        const palabras = () => palabrasInput.value.split(/[\n,;]+/).map(p => p.trim().replace(/\s+/g, ' ')).filter(Boolean)
            .filter((p, i, lista) => lista.findIndex(x => x.toLowerCase() === p.toLowerCase()) === i);
        const sugerida = () => {
            const intervalo = (velocidades[campo('velocidad').value] || velocidades.normal || { intervalo: 2.1 }).intervalo;
            return Math.max(5, Math.round((parseInt(campo('duracion').value, 10) || 60) / intervalo * 0.7));
        };
        // Detective digital: los grupos que escribió el profe (nombre, emoji y tarjetas)
        const grupos = () => [1, 2, 3].map(n => ({
            nombre: campo(`cat${n}_nombre`).value.trim(), emoji: campo(`cat${n}_emoji`).value.trim() || '📁',
            tarjetas: campo(`cat${n}_tarjetas`).value.split('\n').map(t => t.trim()).filter(Boolean),
        }));
        const gruposValidos = () => grupos().filter(g => g.nombre && g.tarjetas.length);
        function ponerTemaClasifica(clave) {
            const tema = temasClasifica[clave];
            [1, 2, 3].forEach((n, i) => {
                const g = tema.categorias[i];
                campo(`cat${n}_emoji`).value = g ? g.emoji : '';
                campo(`cat${n}_nombre`).value = g ? g.nombre : '';
                campo(`cat${n}_tarjetas`).value = g ? g.tarjetas.join('\n') : '';
            });
            campo('tema_clasifica').value = clave;
            avisarCambio(form);
        }
        const atajosElegidos = () => $$('input[name=atajos]:checked', form).map(c => c.value);
        const palabrasMensaje = () => [...new Set(campo('palabras_mensaje').value.split(/[\n,;]+/)
            .map(p => (window.NLJuegos ? window.NLJuegos.normalizarSecreto(p) : p.trim().toUpperCase())).filter(Boolean))];
        const frasesPropias = () => campo('frases').value.split('\n').map(f => f.trim().replace(/\s+/g, ' ')).filter(f => f.split(' ').length >= 2);
        function config() {
            if (plantilla() === 'atajos') {
                return { atajos: atajosElegidos(), catalogo: catalogoAtajos, rondas: parseInt(campo('rondas_atajos').value, 10) || 10,
                    modo: campo('modo_atajos').value || 'aprende' };
            }
            if (plantilla() === 'mensaje') {
                const palabras = palabrasMensaje().filter(p => p.length >= 2 && p.length <= 12);
                return { cifrado: campo('cifrado').value || 'simbolos', palabras, rondas: Math.min(parseInt(campo('rondas_mensaje').value, 10) || 5, palabras.length || 5),
                    desplazamiento: parseInt(campo('desplazamiento').value, 10) || 3, intentos: 3 };
            }
            if (plantilla() === 'rutas') {
                return { modo: campo('modo_rutas').value || 'ruta', dificultad: campo('dificultad_rutas').value || 'facil',
                    rondas: parseInt(campo('rondas_rutas').value, 10) || 5 };
            }
            if (plantilla() === 'formato') {
                const propias = frasesPropias();
                return { dificultad: campo('dificultad_formato').value || 'facil', rondas: parseInt(campo('rondas_formato').value, 10) || 5,
                    frases: propias.length >= 3 ? propias : frasesFormato, intentos: 3 };
            }
            if (plantilla() === 'clasifica') {
                const tiempo = parseInt(campo('tiempo_tarjeta').value, 10);
                const lista = gruposValidos();
                const total = lista.reduce((n, g) => n + g.tarjetas.length, 0);
                return { categorias: lista, rondas: Math.min(parseInt(campo('rondas_tarjetas').value, 10) || 10, total || 10),
                    tiempo: Number.isNaN(tiempo) ? 8 : tiempo };
            }
            if (plantilla() === 'robot') {
                const dificultad = campo('dificultad').value || 'facil';
                return { dificultad, niveles: parseInt(campo('niveles').value, 10) || 5, modo: campo('modo_robot').value || 'flechas',
                    bucles: campo('bucles').checked, intentos: 3, tablero: dificultades[dificultad] };
            }
            if (plantilla() === 'teclado') {
                const conjunto = campo('conjunto').value || 'central';
                const propias = [...new Set(campo('teclas').value.toUpperCase().replace(/[^A-ZÑ0-9]/g, ''))].join('');
                return {
                    conjunto, rondas: parseInt(campo('rondas').value, 10) || 20, modo: campo('modo').value || 'guiado',
                    teclas: conjunto === 'personalizado' ? (propias.length >= 2 ? propias : conjuntos.central) : conjuntos[conjunto],
                };
            }
            const velocidad = campo('velocidad').value || 'normal';
            return {
                palabras: palabras(), duracion: parseInt(campo('duracion').value, 10) || 60, velocidad,
                vidas: parseInt(campo('vidas').value, 10) || 3, meta: Math.max(1, parseInt(metaInput.value, 10) || sugerida()),
                acentos: campo('acentos_exactos').checked ? 'exactos' : 'opcionales', ...velocidades[velocidad],
            };
        }
        const textoMeta = cfg => ({
            teclado: () => `Encuentra ${cfg.rondas} teclas sin equivocarte`,
            clasifica: () => `Clasifica ${cfg.rondas} tarjetas sin equivocarte`,
            atajos: () => `Resuelve ${cfg.rondas} situaciones con el atajo correcto`,
            mensaje: () => `Descifra ${cfg.rondas} mensajes secretos`,
            rutas: () => `Encuentra ${cfg.rondas} archivos con pocos clics`,
            formato: () => `Copia el formato de ${cfg.rondas} textos`,
            robot: () => `Resuelve ${cfg.niveles} laberintos programando al robot`,
        }[plantilla()] || (() => `Destruye ${cfg.meta} meteoros en ${cfg.duracion} segundos`))();
        const NOMBRES_DIFICULTAD = { facil: 'primeros pasos', media: 'explorador', dificil: 'experto' };
        function nombrePropuesto() {
            if (plantilla() === 'teclado') return `Teclado misterioso: ${NOMBRES_CONJUNTO[campo('conjunto').value] || 'fila guía'}`;
            if (plantilla() === 'robot') return `Robot programador: ${NOMBRES_DIFICULTAD[campo('dificultad').value] || 'primeros pasos'}`;
            if (plantilla() === 'atajos') {
                const elegidos = atajosElegidos();
                const grupos = Object.values(gruposAtajos).filter(g => g.atajos.every(a => elegidos.includes(a)));
                return grupos.length === 1 ? `Atajos ninja: ${grupos[0].nombre.toLowerCase()}` : 'Atajos ninja';
            }
            if (plantilla() === 'mensaje') return `Mensaje secreto: código ${(cifrados[campo('cifrado').value] || ['', 'símbolos'])[1].toLowerCase()}`;
            if (plantilla() === 'rutas') return `Explorador de rutas: ${campo('modo_rutas').value === 'buscar' ? '¿dónde lo guardarías?' : 'sigue la ruta'}`;
            if (plantilla() === 'formato') return `Copia el formato: nivel ${NOMBRES_DIFICULTAD[campo('dificultad_formato').value] || 'primeros pasos'}`;
            if (plantilla() === 'clasifica') {
                const tema = temasClasifica[campo('tema_clasifica').value];
                return tema ? `Detective digital: ${tema.nombre}` : 'Detective digital';
            }
            const lista = palabras().map(p => p.toLowerCase());
            const usados = Object.values(temas).filter(t => t.palabras.filter(p => lista.includes(p)).length >= Math.min(5, t.palabras.length));
            if (usados.length === 1) return `Lluvia de meteoros: ${usados[0].nombre}`;
            return usados.length ? 'Lluvia de meteoros TIC' : 'Lluvia de meteoros';
        }
        function pintarTemas() {
            const lista = palabras().map(p => p.toLowerCase());
            $('[data-temas]', form).innerHTML = Object.entries(temas).map(([clave, t]) =>
                `<button type="button" data-tema="${clave}" class="${t.palabras.every(p => lista.includes(p)) ? 'activo' : ''}">${t.emoji} ${escapar(t.nombre)}</button>`).join('');
        }
        function alternarTema(clave) {
            const tema = temas[clave];
            let lista = palabras();
            const minusculas = lista.map(p => p.toLowerCase());
            if (tema.palabras.every(p => minusculas.includes(p))) lista = lista.filter(p => !tema.palabras.includes(p.toLowerCase()));
            else tema.palabras.forEach(p => { if (!minusculas.includes(p)) lista.push(p); });
            palabrasInput.value = lista.join('\n');
            avisarCambio(form);
        }

        function actualizar() {
            const p = plantilla();
            const info = plantillas[p] || {};
            $$('[data-bloque]', form).forEach(b => b.classList.toggle('d-none', b.dataset.bloque !== p));
            $('[data-explicacion-plantilla]', form).innerHTML = `<span class="e">${info.emoji}</span><div>${escapar(info.como || '')}</div>`;
            if (p === 'atajos') {
                const elegidos = atajosElegidos();
                $('[data-grupos-atajos]', form).innerHTML = Object.entries(gruposAtajos).map(([clave, g]) =>
                    `<button type="button" data-grupo-atajos="${clave}" class="${g.atajos.every(a => elegidos.includes(a)) ? 'activo' : ''}">${g.emoji} ${escapar(g.nombre)}</button>`).join('');
                const cfgA = config();
                $('[data-ayuda-atajos]', form).innerHTML = elegidos.length < 2
                    ? '⚠️ Elige al menos 2 atajos.'
                    : (cfgA.modo === 'ninja' ? '🥷 <b>Ninja:</b> solo ven la situación; la combinación aparece si se equivocan.'
                        : '💡 <b>Aprende:</b> ven la situación y la combinación; practican hasta memorizarla.')
                        + `<br>${elegidos.length} atajos · ⭐ con ${Math.ceil(cfgA.rondas * 0.5)} situaciones resueltas · ⭐⭐⭐ con ${Math.ceil(cfgA.rondas * 0.9)}. En tablets sin teclado aparecen opciones para tocar.`;
            } else if (p === 'mensaje') {
                const cfgM = config();
                const cifrado = cifrados[cfgM.cifrado] || ['🔣', 'Símbolos', ''];
                $('[data-bloque-desplazamiento]', form).classList.toggle('d-none', cfgM.cifrado !== 'cesar');
                $('[data-explicacion-cifrado]', form).innerHTML = `<span class="e">${cifrado[0]}</span><div><b>${escapar(cifrado[1])}:</b> ${escapar(cifrado[2])}</div>`;
                const listaM = palabrasMensaje().map(x => x.toLowerCase());
                $('[data-temas-mensaje]', form).innerHTML = Object.entries(temas).map(([clave, t]) => {
                    const normal = t.palabras.map(x => (window.NLJuegos ? window.NLJuegos.normalizarSecreto(x) : x).toLowerCase());
                    return `<button type="button" data-tema-mensaje="${clave}" class="${normal.every(x => listaM.includes(x)) ? 'activo' : ''}">${t.emoji} ${escapar(t.nombre)}</button>`;
                }).join('');
                const largas = palabrasMensaje().filter(x => x.length > 12);
                const cuenta = $('[data-cuenta-mensaje]', form);
                cuenta.textContent = largas.length ? `⚠️ ${largas[0]} es muy larga` : `${cfgM.palabras.length} palabras`;
                cuenta.classList.toggle('text-danger', cfgM.palabras.length < 3 || largas.length > 0);
                const ejemplo = cfgM.palabras[0];
                $('[data-ejemplo-cifrado]', form).innerHTML = ejemplo && window.NLJuegos
                    ? `<span class="t">Así verán «${escapar(ejemplo)}»:</span><span class="codigos">${[...ejemplo].map(l => `<span><b>${escapar(window.NLJuegos.codigoDe(l, cfgM))}</b><i>${l}</i></span>`).join('')}</span>`
                    : '';
            } else if (p === 'rutas') {
                const cfgX = config();
                $('[data-ayuda-rutas]', form).innerHTML = (cfgX.modo === 'buscar'
                    ? '🔎 <b>Búscalo:</b> solo ven el nombre del archivo (ej. «cancion_feliz.mp3») y deciden en qué carpeta estaría. Aprenden a organizar.'
                    : '🧭 <b>Sigue la ruta:</b> ven el nombre y la ruta (ej. «Documentos › Escuela › Ciencias»). Aprenden a leer rutas.')
                    + `<br>⭐ con ${Math.ceil(cfgX.rondas * 0.5)} archivos encontrados · cada uno cuenta si usan máximo 3 clics de más.`;
            } else if (p === 'formato') {
                const cfgF = config();
                const propias = frasesPropias();
                $('[data-ayuda-formato]', form).innerHTML = ({
                    facil: '🌱 <b>Fácil:</b> un solo formato (negrita, cursiva o subrayado) en todo el texto.',
                    media: '🚀 <b>Media:</b> formato en una o dos palabras; a veces color y centrado.',
                    dificil: '🔥 <b>Difícil:</b> varias palabras con distinto formato, color, tamaño y alineación.',
                }[cfgF.dificultad]) + `<br>${propias.length >= 3 ? `Se usarán tus ${propias.length} frases.` : `Se usarán ${frasesFormato.length} frases de TIC (agrega 3 o más para usar las tuyas).`}`;
            } else if (p === 'clasifica') {
                const tema = campo('tema_clasifica').value;
                $('[data-temas-clasifica]', form).innerHTML = Object.entries(temasClasifica).map(([clave, t]) =>
                    `<button type="button" data-tema-clasifica="${clave}" class="${clave === tema ? 'activo' : ''}">${t.emoji} ${escapar(t.nombre)}</button>`).join('');
                grupos().forEach((g, i) => {
                    const cuenta = $(`[data-cuenta-grupo="${i + 1}"]`, form);
                    cuenta.textContent = g.tarjetas.length ? `${g.tarjetas.length} tarjeta${g.tarjetas.length === 1 ? '' : 's'}` : (i === 2 ? 'Grupo opcional' : 'Sin tarjetas');
                });
                const cfgC = config();
                const total = cfgC.categorias.reduce((n, g) => n + g.tarjetas.length, 0);
                $('[data-ayuda-clasifica]', form).innerHTML = cfgC.categorias.length < 2
                    ? '⚠️ Necesitas al menos 2 grupos, cada uno con sus tarjetas.'
                    : `💡 Hay <b>${total}</b> tarjetas; en cada partida salen <b>${cfgC.rondas}</b> al azar. ⭐ con ${Math.ceil(cfgC.rondas * 0.5)} correctas · ⭐⭐⭐ con ${Math.ceil(cfgC.rondas * 0.9)}.`
                        + (total < parseInt(campo('rondas_tarjetas').value, 10) ? ' Escribe más tarjetas para que no se repitan.' : '');
            } else if (p === 'robot') {
                const cfgR = config();
                const t = cfgR.tablero || { tam: 5 };
                $('[data-ayuda-robot]', form).innerHTML = `🧩 Tableros de <b>${t.tam} × ${t.tam}</b>, nuevos en cada partida y siempre con solución. `
                    + (cfgR.modo === 'giros' ? '🔄 Con «avanzar y girar» piensan como un robot real: hacia dónde mira importa.' : '➡️ Con flechas cada bloque mueve una casilla: ideal para empezar.')
                    + `<br>⭐ con ${Math.ceil(cfgR.niveles * 0.5)} laberintos resueltos · ⭐⭐⭐ con ${Math.ceil(cfgR.niveles * 0.9)}. Bono extra por resolverlo con el código más corto.`;
            } else if (p === 'meteoros') {
                if (metaSugerida) metaInput.value = sugerida();
                const n = palabras().length;
                const cuenta = $('[data-cuenta-palabras]', form);
                cuenta.textContent = n < 5 ? `${n} de 5 mínimo` : `${n} palabras`;
                cuenta.classList.toggle('text-danger', n < 5);
                const meta = parseInt(metaInput.value, 10) || sugerida();
                $('[data-ayuda-meta]', form).innerHTML = `💡 Con <b>${Math.ceil(meta * 0.5)}</b> meteoros superan la misión (⭐), con <b>${Math.ceil(meta * 0.7)}</b> ganan ⭐⭐ y con <b>${Math.ceil(meta * 0.9)}</b> ⭐⭐⭐. Para esta velocidad y duración sugerimos <b>${sugerida()}</b>.`;
                pintarTemas();
            } else {
                $('[data-bloque-teclas]', form).classList.toggle('d-none', campo('conjunto').value !== 'personalizado');
                const cfg = config();
                $('[data-ayuda-teclado]', form).innerHTML = (cfg.modo === 'guiado'
                    ? '💡 <b>Guiado:</b> la tecla brilla en el teclado de la pantalla y el alumno la busca en el suyo.'
                    : '🕵️ <b>Reto:</b> solo ve la letra. Si se equivoca dos veces, aparece una pista.')
                    + `<br>⭐ con ${Math.ceil(cfg.rondas * 0.5)} aciertos a la primera · ⭐⭐⭐ con ${Math.ceil(cfg.rondas * 0.9)}.`;
            }
            if (nombreSugerido) nombre.value = nombrePropuesto();
            if (iconoSugerido && info.emoji) icono.value = info.emoji;

            $('[data-bloque-arcade]', form).classList.toggle('d-none', !enArcade.checked);
            $('[data-bloque-mapa]', form).classList.toggle('d-none', !agregarMapa.checked);
            $('[data-ayuda-desbloqueo]', form).textContent = $('input[name=desbloqueo]:checked', form)?.value === 'mision'
                ? 'Sale con candado 🔒 hasta que el alumno supere su misión del mapa. Si no está en el mapa, queda libre.'
                : 'Lo pueden jugar desde el primer día.';

            const cfg = config();
            $('[data-maquina]', form).style.setProperty('--m1', info.color || '#7c3aed');
            $('[data-previa-icono]', form).textContent = icono.value.trim() || info.emoji || '🎮';
            $('[data-previa-tipo]', form).textContent = `${info.emoji || ''} ${info.nombre || ''}`;
            $('[data-previa-nombre]', form).textContent = nombre.value.trim() || 'Nombre del juego';
            $('[data-previa-meta]', form).textContent = `🎯 ${textoMeta(cfg)}`;
            const corte = q => ({
                teclado: () => `${Math.ceil(cfg.rondas * q)} a la primera`,
                clasifica: () => `${Math.ceil(cfg.rondas * q)} correctas`,
                robot: () => `${Math.ceil(cfg.niveles * q)} laberintos`,
                atajos: () => `${Math.ceil(cfg.rondas * q)} situaciones`,
                mensaje: () => `${Math.ceil(cfg.rondas * q)} mensajes`,
                rutas: () => `${Math.ceil(cfg.rondas * q)} archivos`,
                formato: () => `${Math.ceil(cfg.rondas * q)} textos`,
            }[p] || (() => `${Math.ceil(cfg.meta * q)} meteoros`))();
            $('[data-previa-cortes]', form).innerHTML = `<span>⭐ ${corte(0.5)}</span><span>⭐⭐ ${corte(0.7)}</span><span>⭐⭐⭐ ${corte(0.9)}</span>`;
            const donde = [];
            if (agregarMapa.checked || $('.misiones-juego', form)) donde.push('🗺️ Misión del mapa');
            if (enArcade.checked) donde.push('🕹️ Arcade');
            $('[data-previa-donde]', form).innerHTML = donde.length
                ? `Aparece en: <b>${donde.join(' · ')}</b>` : '⚠️ Todavía no aparece en ningún lado: enciéndelo en el Arcade o agrégalo al mapa.';
            marcarAtajos(form);
            // Pasos: 1 · 2 (meteoros, teclado, detective, robot, atajos, mensaje, rutas, formato) · 3 · 4
            marcarPasos(form, [true, palabras().length >= 5, true, gruposValidos().length >= 2, true, atajosElegidos().length >= 2,
                palabrasMensaje().filter(x => x.length >= 2 && x.length <= 12).length >= 3, true, true, !!nombre.value.trim(), donde.length > 0]);
        }

        form.addEventListener('click', e => {
            const tema = e.target.closest('[data-tema]');
            if (tema) alternarTema(tema.dataset.tema);
            const temaClasifica = e.target.closest('[data-tema-clasifica]');
            if (temaClasifica) ponerTemaClasifica(temaClasifica.dataset.temaClasifica);
            const grupoAtajos = e.target.closest('[data-grupo-atajos]');
            if (grupoAtajos) {
                const claves = gruposAtajos[grupoAtajos.dataset.grupoAtajos].atajos;
                const cajas = claves.map(k => form.querySelector(`input[name=atajos][value="${k}"]`)).filter(Boolean);
                const poner = !cajas.every(c => c.checked);
                cajas.forEach(c => { c.checked = poner; });
                avisarCambio(form);
            }
            const temaMensaje = e.target.closest('[data-tema-mensaje]');
            if (temaMensaje) {
                const t = temas[temaMensaje.dataset.temaMensaje];
                const normal = t.palabras.map(x => window.NLJuegos.normalizarSecreto(x));
                let lista = palabrasMensaje();
                if (normal.every(x => lista.includes(x))) lista = lista.filter(x => !normal.includes(x));
                else normal.forEach(x => { if (!lista.includes(x)) lista.push(x); });
                campo('palabras_mensaje').value = lista.join('\n');
                avisarCambio(form);
            }
            if (e.target.closest('[data-poner="icono"]')) iconoSugerido = false;
            if (e.target.closest('[data-poner="velocidad"], [data-poner="duracion"]') && metaSugerida) setTimeout(actualizar);
        });
        enlazarAtajos(form);
        metaInput.addEventListener('input', e => { if (e.isTrusted) metaSugerida = false; });
        // Si el profe edita los grupos a mano, deja de ser un tema listo
        $$('[data-grupo] input, [data-grupo] textarea', form).forEach(el => el.addEventListener('input', e => {
            if (e.isTrusted) campo('tema_clasifica').value = 'personalizado';
        }));
        nombre.addEventListener('input', e => { if (e.isTrusted) nombreSugerido = false; });
        icono.addEventListener('input', e => { if (e.isTrusted) iconoSugerido = false; });
        $('[data-meta-sugerida]', form).addEventListener('click', () => { metaSugerida = true; actualizar(); avisarCambio(form); });
        $('[data-sugerir-nombre]', form).addEventListener('click', () => { nombreSugerido = true; actualizar(); avisarCambio(form); });
        $('[data-probar]', form).addEventListener('click', () => {
            const p = plantilla();
            const cfg = config();
            if (p === 'meteoros' && cfg.palabras.length < 3) { toast('Escribe al menos 3 palabras para probarlo', 'warning'); return; }
            if (p === 'clasifica' && cfg.categorias.length < 2) { toast('Necesitas al menos 2 grupos con tarjetas', 'warning'); return; }
            if (p === 'atajos' && cfg.atajos.length < 2) { toast('Elige al menos 2 atajos', 'warning'); return; }
            if (p === 'mensaje' && cfg.palabras.length < 3) { toast('Escribe al menos 3 palabras', 'warning'); return; }
            if (!window.NLJuegos) { toast('No se pudo cargar el juego', 'error'); return; }
            window.NLJuegos.abrir({
                demo: true,
                juego: { nombre: nombre.value.trim() || nombrePropuesto(), icono: icono.value.trim() || plantillas[p].emoji,
                    plantilla: p, config: cfg, meta: textoMeta(cfg), info: plantillas[p] },
            });
        });
        form.addEventListener('input', actualizar);
        form.addEventListener('change', actualizar);
        actualizar();
    }

    const INICIADORES = [
        iniciarFormMision, iniciarFormLogro, iniciarFormDiaria, iniciarFormArticulo, iniciarFormClase, iniciarFormMundo,
        iniciarFormNivel, iniciarFormAlumno, iniciarFormMasiva, iniciarFormEquipo, iniciarFormMeta, iniciarFormConducta,
        iniciarFormJuego,
    ];
    function iniciarFormularios(raiz = document) {
        INICIADORES.forEach(iniciar => {
            try { iniciar(raiz); } catch (err) { console.error('Error al preparar el formulario', err); }
        });
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
            // Los formularios guiados (con vista previa) necesitan la ventana ancha
            if (form.classList.contains('ancho')) dialogo.classList.replace('modal-lg', 'modal-xl');
            iniciarFormularios(contenido);
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
        iniciarFormularios();
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

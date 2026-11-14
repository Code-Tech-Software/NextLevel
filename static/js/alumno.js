/* =========================================================
   NEXT-LEVEL · Interacciones del alumno
   ========================================================= */
(function () {
    'use strict';

    // ---------- Utilidades ----------
    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

    function leerPreferencia(clave, porDefecto) {
        try { return localStorage.getItem(clave) ?? porDefecto; } catch (e) { return porDefecto; }
    }
    function guardarPreferencia(clave, valor) {
        try { localStorage.setItem(clave, valor); } catch (e) { /* modo privado */ }
    }
    function csrf() {
        const input = $('[name=csrfmiddlewaretoken]');
        return input ? input.value : '';
    }
    async function postJSON(url, datos = {}) {
        const body = new FormData();
        Object.entries(datos).forEach(([k, v]) => {
            if (Array.isArray(v)) v.forEach(x => body.append(k, x)); else body.append(k, v);
        });
        const resp = await fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrf(), 'X-Requested-With': 'XMLHttpRequest' },
            body,
        });
        return resp.json();
    }
    function escapar(texto) {
        const div = document.createElement('div');
        div.textContent = texto ?? '';
        return div.innerHTML;
    }

    // ---------- Sonidos sintetizados (sin archivos) ----------
    const Sonido = (() => {
        let ctx = null;
        let activo = leerPreferencia('nl-sonido', 'on') !== 'off';

        function tono(freq, dur, tipo = 'square', vol = 0.05, retraso = 0) {
            const t = ctx.currentTime + retraso;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = tipo;
            osc.frequency.setValueAtTime(freq, t);
            gain.gain.setValueAtTime(0.0001, t);
            gain.gain.exponentialRampToValueAtTime(vol, t + 0.01);
            gain.gain.exponentialRampToValueAtTime(0.0001, t + dur);
            osc.connect(gain).connect(ctx.destination);
            osc.start(t);
            osc.stop(t + dur + 0.02);
        }

        const efectos = {
            click: () => tono(520, 0.05, 'triangle', 0.04),
            pop: () => tono(880, 0.07, 'sine', 0.08),
            tecla: () => tono(660, 0.05, 'triangle', 0.05),
            moneda: () => { tono(988, 0.08, 'square', 0.04); tono(1319, 0.3, 'square', 0.04, 0.08); },
            exito: () => [523, 659, 784, 1047].forEach((f, i) => tono(f, 0.18, 'triangle', 0.07, i * 0.09)),
            nivel: () => [392, 523, 659, 784, 1047, 1319].forEach((f, i) => tono(f, 0.2, 'square', 0.035, i * 0.08)),
            error: () => { tono(220, 0.15, 'sawtooth', 0.04); tono(160, 0.3, 'sawtooth', 0.04, 0.12); },
            cofre: () => [330, 415, 523, 659, 880].forEach((f, i) => tono(f, 0.14, 'triangle', 0.07, i * 0.06)),
        };

        return {
            play(nombre) {
                if (!activo || !efectos[nombre]) return;
                try {
                    ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
                    if (ctx.state === 'suspended') ctx.resume();
                    efectos[nombre]();
                } catch (e) { /* sin audio */ }
            },
            alternar() {
                activo = !activo;
                guardarPreferencia('nl-sonido', activo ? 'on' : 'off');
                return activo;
            },
            get activo() { return activo; },
        };
    })();
    window.NLSonido = Sonido;

    // ---------- Confeti ----------
    function confeti(tipo = 'normal') {
        if (typeof window.confetti !== 'function') return;
        const colores = ['#10b981', '#3b82f6', '#fbbf24', '#ec4899', '#8b5cf6', '#38bdf8'];
        if (tipo === 'monedas') {
            window.confetti({ particleCount: 70, spread: 80, origin: { y: 0.6 }, colors: ['#fbbf24', '#f59e0b', '#fde047'], scalar: 1.1 });
            return;
        }
        window.confetti({ particleCount: 110, spread: 90, origin: { y: 0.6 }, colors: colores });
        setTimeout(() => {
            window.confetti({ particleCount: 60, angle: 60, spread: 70, origin: { x: 0 }, colors: colores });
            window.confetti({ particleCount: 60, angle: 120, spread: 70, origin: { x: 1 }, colors: colores });
        }, 250);
    }
    window.NLConfeti = confeti;

    // ---------- Números animados ----------
    function animarNumero(el, hasta, duracion = 900) {
        if (!el) return;
        const desde = parseInt(el.textContent.replace(/\D/g, ''), 10) || 0;
        const inicio = performance.now();
        function paso(t) {
            const p = Math.min(1, (t - inicio) / duracion);
            const eased = 1 - Math.pow(1 - p, 3);
            el.textContent = Math.round(desde + (hasta - desde) * eased).toLocaleString('es-MX');
            if (p < 1) requestAnimationFrame(paso);
        }
        requestAnimationFrame(paso);
        const stat = el.closest('.stat');
        if (stat) { stat.classList.remove('brinca'); void stat.offsetWidth; stat.classList.add('brinca'); }
    }
    window.NLActualizarMonedas = total => $$('[data-monedas]').forEach(el => animarNumero(el, total));

    // ---------- Ventana de celebración ----------
    function celebrar({ icono = '🎉', kicker = '¡Felicidades!', titulo = '', mensaje = '', monto = '', triste = false, boton = '¡Genial!' }) {
        return new Promise(resolve => {
            const capa = document.createElement('div');
            capa.className = 'celebracion' + (triste ? ' triste' : '');
            capa.setAttribute('role', 'dialog');
            capa.setAttribute('aria-modal', 'true');
            capa.innerHTML = `
                <div class="rayos"></div>
                <div class="tarjeta">
                    <div class="icono">${escapar(icono)}</div>
                    <div class="kicker">${escapar(kicker)}</div>
                    <h2>${escapar(titulo)}</h2>
                    ${monto ? `<div class="monto">${escapar(monto)}</div>` : ''}
                    ${mensaje ? `<p>${escapar(mensaje)}</p>` : ''}
                    <button type="button" class="g-btn ${triste ? 'azul' : ''} grande ancho">${escapar(boton)}</button>
                </div>`;
            document.body.appendChild(capa);
            const btn = $('button', capa);
            btn.focus();
            if (triste) Sonido.play('error'); else { Sonido.play(monto ? 'cofre' : 'nivel'); confeti(monto ? 'monedas' : 'normal'); }
            const cerrar = () => { capa.remove(); resolve(); };
            btn.addEventListener('click', () => { Sonido.play('click'); cerrar(); });
            capa.addEventListener('keydown', e => { if (e.key === 'Escape') cerrar(); });
        });
    }
    window.NLCelebrar = celebrar;

    const KICKERS = {
        logro: '¡Logro desbloqueado!',
        nivel: '¡Subiste de nivel!',
        aprobada: '¡Misión aprobada!',
        rechazada: 'Tu profe te dejó un mensaje',
        sistema: '¡Increíble!',
        cofre: '¡Tesoro!',
        diaria: 'Misión del día',
        batalla: '¡Batalla en vivo!',
    };

    async function mostrarCelebracionesPendientes() {
        const datos = $('#celebraciones-data');
        if (!datos) return;
        let lista = [];
        try { lista = JSON.parse(datos.textContent); } catch (e) { return; }
        if (!lista.length) return;
        for (const c of lista) {
            await celebrar({
                icono: c.icono, titulo: c.titulo.replace(/^Logro desbloqueado:\s*/, ''), mensaje: c.mensaje,
                kicker: KICKERS[c.tipo] || '¡Novedades!', triste: c.tipo === 'rechazada',
                boton: c.tipo === 'rechazada' ? 'Voy a corregirla' : '¡Genial!',
            });
        }
        const url = document.body.dataset.urlLeer;
        if (url) postJSON(url, { ids: lista.map(c => c.id) }).catch(() => {});
    }

    // ---------- Notificaciones ----------
    function iniciarNotificaciones() {
        const boton = $('#btn-notif');
        if (!boton) return;
        boton.addEventListener('shown.bs.dropdown', () => {
            const burbuja = $('.burbuja', boton);
            if (!burbuja) return;
            const url = document.body.dataset.urlLeer;
            if (url) postJSON(url).then(() => burbuja.remove()).catch(() => {});
        });
    }

    // ---------- Aviso de Batalla en vivo ----------
    // Cada pocos segundos pregunta (sin tocar la base de datos si hay Redis) si el profe abrió una batalla
    function iniciarAvisoBatalla() {
        const aviso = $('#aviso-batalla');
        if (!aviso) return;
        let visible = !aviso.classList.contains('oculto');
        async function revisar() {
            if (!document.hidden) {
                try {
                    const r = await fetch(aviso.dataset.urlSenal, { headers: { 'X-Requested-With': 'XMLHttpRequest' }, cache: 'no-store' });
                    if (r.ok) {
                        const datos = await r.json();
                        if (datos.en_juego && !visible) Sonido.play('pop');
                        visible = !!datos.en_juego;
                        aviso.classList.toggle('oculto', !visible);
                        if (datos.titulo) $('[data-aviso-titulo]', aviso).textContent = datos.titulo;
                    }
                } catch (e) { /* sin red: se intenta en la siguiente vuelta */ }
            }
            setTimeout(revisar, visible ? 15000 : 8000);
        }
        setTimeout(revisar, 8000);
    }

    // ---------- Sonido on/off ----------
    function iniciarBotonSonido() {
        const btn = $('#btn-sonido');
        const aplicar = () => document.body.classList.toggle('sonido-off', !Sonido.activo);
        aplicar();
        if (!btn) return;
        btn.addEventListener('click', () => { Sonido.alternar(); aplicar(); Sonido.play('pop'); });
    }

    // ---------- Misiones del día ----------
    function iniciarDiarias() {
        $$('.btn-reclamar').forEach(btn => btn.addEventListener('click', async () => {
            btn.disabled = true;
            try {
                const r = await postJSON(btn.dataset.url);
                if (!r.ok) { Sonido.play('error'); btn.disabled = false; return; }
                const fila = btn.closest('.diaria');
                fila.classList.add('reclamada');
                btn.outerHTML = '<span class="chip verde"><i class="bi bi-check-circle-fill"></i> Reclamada</span>';
                window.NLActualizarMonedas(r.total);
                await celebrar({
                    icono: $('.ico', fila)?.textContent.trim() || '⭐', kicker: 'Misión del día completada',
                    titulo: r.titulo, monto: `+${r.monedas} 💰`, mensaje: r.xp ? `y +${r.xp} XP de experiencia` : '',
                });
            } catch (e) { btn.disabled = false; }
        }));

        const reloj = $('[data-cuenta-regresiva]');
        if (reloj) {
            let restantes = parseInt(reloj.dataset.cuentaRegresiva, 10);
            const pintar = () => {
                const h = String(Math.floor(restantes / 3600)).padStart(2, '0');
                const m = String(Math.floor((restantes % 3600) / 60)).padStart(2, '0');
                const s = String(restantes % 60).padStart(2, '0');
                $('.tiempo', reloj).textContent = `${h}:${m}:${s}`;
            };
            pintar();
            setInterval(() => { restantes -= 1; if (restantes <= 0) location.reload(); else pintar(); }, 1000);
        }
    }

    // ---------- Cofres ----------
    function iniciarCofres() {
        $$('.cofre-nodo.disponible').forEach(btn => btn.addEventListener('click', async () => {
            btn.disabled = true;
            btn.classList.remove('disponible');
            Sonido.play('pop');
            try {
                const r = await postJSON(btn.dataset.url);
                if (!r.ok) { Sonido.play('error'); return; }
                btn.classList.add('abierto');
                btn.textContent = '💰';
                const etiqueta = btn.parentElement.querySelector('.cofre-etiqueta');
                if (etiqueta) etiqueta.textContent = `+${r.monedas} monedas`;
                window.NLActualizarMonedas(r.total);
                await celebrar({ icono: '💰', kicker: '¡Cofre abierto!', titulo: 'Encontraste un tesoro', monto: `+${r.monedas} 💰` });
            } catch (e) { btn.disabled = false; }
        }));
    }

    // ---------- Cuestionario por pasos ----------
    function iniciarQuiz() {
        const quiz = $('.quiz[data-carrusel]');
        if (!quiz) return;
        const preguntas = $$('.quiz-pregunta', quiz);
        if (!preguntas.length) return;
        quiz.classList.add('js');
        const barra = $('.quiz-top .barra > span', quiz);
        const contador = $('.quiz-top .contador', quiz);
        const btnAnterior = $('[data-quiz="anterior"]', quiz);
        const btnSiguiente = $('[data-quiz="siguiente"]', quiz);
        const btnEnviar = $('[data-quiz="enviar"]', quiz);
        let actual = 0;

        const respondida = i => !!$('input:checked', preguntas[i]);
        function mostrar(i) {
            actual = i;
            preguntas.forEach((p, k) => p.classList.toggle('activa', k === i));
            const contestadas = preguntas.filter((_, k) => respondida(k)).length;
            barra.style.width = `${Math.max(4, (contestadas / preguntas.length) * 100)}%`;
            contador.textContent = `${i + 1} / ${preguntas.length}`;
            btnAnterior.classList.toggle('oculto', i === 0);
            const ultima = i === preguntas.length - 1;
            btnSiguiente.classList.toggle('oculto', ultima);
            btnEnviar.classList.toggle('oculto', !ultima);
        }
        function avisar() {
            const pregunta = preguntas[actual];
            pregunta.classList.remove('quiz-pregunta');
            void pregunta.offsetWidth;
            pregunta.classList.add('quiz-pregunta');
            pregunta.animate([{ transform: 'translateX(-8px)' }, { transform: 'translateX(8px)' }, { transform: 'none' }], { duration: 300 });
            Sonido.play('error');
        }

        quiz.addEventListener('change', e => {
            if (e.target.matches('input[type=radio]')) { Sonido.play('pop'); mostrar(actual); }
        });
        btnSiguiente.addEventListener('click', () => {
            if (!respondida(actual)) return avisar();
            Sonido.play('click');
            mostrar(actual + 1);
            quiz.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
        btnAnterior.addEventListener('click', () => mostrar(actual - 1));
        quiz.closest('form').addEventListener('submit', e => {
            const faltante = preguntas.findIndex((_, k) => !respondida(k));
            if (faltante !== -1) { e.preventDefault(); mostrar(faltante); avisar(); }
        });
        mostrar(0);
    }

    // ---------- Tienda ----------
    function iniciarTienda() {
        $$('.filtro[data-filtro]').forEach(btn => btn.addEventListener('click', () => {
            $$('.filtro').forEach(b => b.classList.toggle('activo', b === btn));
            const filtro = btn.dataset.filtro;
            $$('.col-producto').forEach(col => {
                col.classList.toggle('oculto', filtro !== 'todos' && col.dataset.tipo !== filtro);
            });
            Sonido.play('click');
        }));

        $$('.form-compra').forEach(form => form.addEventListener('submit', e => {
            e.preventDefault();
            if (typeof Swal === 'undefined') return form.submit();
            Sonido.play('pop');
            const imagen = form.dataset.imagen;
            Swal.fire({
                title: `¿Comprar ${form.dataset.nombre}?`,
                html: `${imagen ? `<img src="${escapar(imagen)}" alt="" style="max-height:120px;max-width:70%;object-fit:contain;margin-bottom:12px">` : ''}
                       <div>Te costará <b style="color:#d97706;font-size:1.3rem">${escapar(form.dataset.costo)} 💰</b></div>
                       <div style="font-size:.9rem;margin-top:6px">Te quedarán ${escapar(form.dataset.restante)} monedas</div>
                       <div class="swal-tipo">${escapar(form.dataset.tipo)} · ${escapar(form.dataset.entrega)}</div>`,
                showCancelButton: true,
                reverseButtons: true,
                buttonsStyling: false,
                confirmButtonText: '<i class="bi bi-bag-check-fill"></i> ¡Sí, comprar!',
                cancelButtonText: 'Mejor no',
                customClass: { popup: 'swal-juego', confirmButton: 'g-btn', cancelButton: 'g-btn blanco' },
            }).then(r => {
                if (r.isConfirmed) { Sonido.play('moneda'); setTimeout(() => form.submit(), 250); }
            });
        }));
    }

    // ---------- Misión: foto, código, scroll ----------
    function iniciarMision() {
        $$('.subir-foto input[type=file]').forEach(input => input.addEventListener('change', () => {
            const caja = input.closest('.subir-foto');
            const archivo = input.files[0];
            if (!archivo) return caja.classList.remove('con-foto');
            const lector = new FileReader();
            lector.onload = e => { $('img.vista', caja).src = e.target.result; caja.classList.add('con-foto'); };
            lector.readAsDataURL(archivo);
        }));

        $$('.copiar[data-objetivo]').forEach(btn => btn.addEventListener('click', async () => {
            const codigo = document.getElementById(btn.dataset.objetivo);
            try {
                await navigator.clipboard.writeText(codigo.textContent);
                btn.innerHTML = '<i class="bi bi-check2"></i> ¡Copiado!';
                Sonido.play('pop');
                setTimeout(() => { btn.innerHTML = '<i class="bi bi-clipboard"></i> Copiar'; }, 1800);
            } catch (e) { /* sin portapapeles */ }
        }));

        // ---------- Llavero de apps: copiar un dato y mostrar u ocultar la contraseña ----------
        async function copiarTexto(texto) {
            try {
                await navigator.clipboard.writeText(texto);
                return true;
            } catch (e) {
                // Respaldo para navegadores sin portapapeles moderno
                const area = document.createElement('textarea');
                area.value = texto;
                area.setAttribute('readonly', '');
                area.style.position = 'fixed';
                area.style.opacity = '0';
                document.body.appendChild(area);
                area.select();
                let ok = false;
                try { ok = document.execCommand('copy'); } catch (err) { ok = false; }
                area.remove();
                return ok;
            }
        }
        function alternarSecreto(boton, mostrar) {
            const valor = boton.closest('.llave-dato')?.querySelector('[data-secreto]');
            if (!valor) return;
            valor.textContent = mostrar ? valor.dataset.secreto : '••••••••';
            valor.classList.toggle('tapado', !mostrar);
            boton.setAttribute('aria-pressed', mostrar ? 'true' : 'false');
            boton.innerHTML = mostrar ? '<i class="bi bi-eye-slash"></i>' : '<i class="bi bi-eye"></i>';
            clearTimeout(boton._ocultar);
            // Se vuelve a ocultar sola, por si alguien está viendo la pantalla
            if (mostrar) boton._ocultar = setTimeout(() => alternarSecreto(boton, false), 15000);
        }
        document.addEventListener('click', async e => {
            const copiar = e.target.closest('[data-copiar]');
            if (copiar) {
                if (await copiarTexto(copiar.dataset.copiar)) {
                    copiar.classList.add('copiado');
                    copiar.innerHTML = '<i class="bi bi-check2"></i>';
                    Sonido.play('pop');
                    setTimeout(() => { copiar.classList.remove('copiado'); copiar.innerHTML = '<i class="bi bi-clipboard"></i>'; }, 1500);
                }
                return;
            }
            const revelar = e.target.closest('[data-revelar]');
            if (revelar) alternarSecreto(revelar, revelar.getAttribute('aria-pressed') !== 'true');
        });

        const resultado = $('#resultado-mision');
        if (resultado) {
            setTimeout(() => {
                Sonido.play('exito');
                confeti();
            }, 300);
        }

        const actual = $('.nodo.actual');
        if (actual) setTimeout(() => actual.scrollIntoView({ behavior: 'smooth', block: 'center' }), 450);
    }

    // ---------- Selección de jugador y teclado de PIN ----------
    function iniciarPin() {
        const buscador = $('#buscar-jugador');
        if (buscador) {
            buscador.addEventListener('input', () => {
                const q = buscador.value.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
                $$('.col-jugador').forEach(col => {
                    col.classList.toggle('oculto', !col.dataset.nombre.includes(q));
                });
            });
        }

        $$('.modal-pin').forEach(modal => {
            const form = $('form', modal);
            const input = $('input[name=pin]', modal);
            const puntos = $('.pin-puntos', modal);
            let valor = '';

            const pintar = () => $$('i', puntos).forEach((p, i) => p.classList.toggle('lleno', i < valor.length));
            const teclear = digito => {
                if (valor.length >= 4) return;
                valor += digito;
                Sonido.play('tecla');
                pintar();
                if (valor.length === 4) {
                    input.value = valor;
                    puntos.classList.add('ok');
                    Sonido.play('exito');
                    setTimeout(() => form.submit(), 280);
                }
            };
            const borrar = () => { valor = valor.slice(0, -1); puntos.classList.remove('error', 'ok'); pintar(); Sonido.play('click'); };

            $$('.tecla[data-digito]', modal).forEach(t => t.addEventListener('click', () => teclear(t.dataset.digito)));
            $('.tecla[data-accion=borrar]', modal)?.addEventListener('click', borrar);

            modal.addEventListener('keydown', e => {
                if (/^[0-9]$/.test(e.key)) { teclear(e.key); marcarTecla(e.key); }
                else if (e.key === 'Backspace') borrar();
            });
            function marcarTecla(d) {
                const t = $(`.tecla[data-digito="${d}"]`, modal);
                if (!t) return;
                t.classList.add('presionada');
                setTimeout(() => t.classList.remove('presionada'), 120);
            }
            modal.addEventListener('show.bs.modal', () => { valor = ''; puntos.classList.remove('error', 'ok'); pintar(); });
            modal.addEventListener('shown.bs.modal', () => modal.querySelector('.modal-content').focus());

            if (modal.dataset.error === '1' && window.bootstrap) {
                const instancia = new bootstrap.Modal(modal);
                instancia.show();
                setTimeout(() => { puntos.classList.add('error'); Sonido.play('error'); }, 350);
            }
            // Llegó desde el QR de su credencial: su tarjeta se abre sola
            if (modal.dataset.abrir === '1' && window.bootstrap) {
                bootstrap.Modal.getOrCreateInstance(modal).show();
            }
        });
    }

    // ---------- Pulsaciones de botones ----------
    function iniciarClicks() {
        document.addEventListener('pointerdown', e => {
            if (e.target.closest('.g-btn, .nodo, .filtro, .mundo-card')) Sonido.play('click');
        });
    }

    // ---------- Avisos del profe y cumpleaños ----------
    function iniciarAvisosProfe() {
        const LLAVE = 'nl-avisos-leidos';
        let leidos = [];
        try { leidos = JSON.parse(localStorage.getItem(LLAVE) || '[]'); } catch (e) { leidos = []; }
        $$('[data-aviso]').forEach(aviso => {
            if (leidos.includes(aviso.dataset.aviso)) { aviso.remove(); return; }
            $('[data-cerrar-aviso]', aviso)?.addEventListener('click', () => {
                leidos = [...leidos.filter(id => id !== aviso.dataset.aviso), aviso.dataset.aviso].slice(-50);
                try { localStorage.setItem(LLAVE, JSON.stringify(leidos)); } catch (e) { /* sin almacenamiento */ }
                aviso.classList.add('saliendo');
                setTimeout(() => aviso.remove(), 250);
            });
        });
        // El día de su cumpleaños: confeti la primera vez que abre su tablero (en esta visita)
        if ($('[data-cumple]')) {
            let ya = false;
            try { ya = sessionStorage.getItem('nl-cumple') === new Date().toDateString(); } catch (e) { /* nada */ }
            if (!ya) {
                setTimeout(() => { confeti(); Sonido.play('nivel'); }, 500);
                try { sessionStorage.setItem('nl-cumple', new Date().toDateString()); } catch (e) { /* nada */ }
            }
        }
    }

    // ---------- Mis proyectos: subir con barra de avance, versión nueva, cambiar nombre y borrar ----------
    function iniciarProyectos() {
        const formularios = $$('form[data-subir-proyecto]');
        let iconos = {};
        try { iconos = JSON.parse($('#iconos-proyectos')?.textContent || '{}'); } catch (e) { iconos = {}; }
        const extension = n => (n.includes('.') ? n.split('.').pop().toLowerCase() : '');
        const peso = b => (b < 1e6 ? `${Math.max(1, Math.round(b / 1000))} KB` : `${(b / 1e6).toFixed(1).replace(/\.0$/, '')} MB`);
        const sugerido = n => {
            const base = n.replace(/\.[^.]+$/, '').replace(/_/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 80);
            return base ? base[0].toUpperCase() + base.slice(1) : '';
        };
        // Recarga la página aunque solo cambie el #ancla (si no, el navegador solo se desplaza y no se ve el cambio)
        const irA = url => {
            const destino = new URL(url, window.location.href);
            if (destino.pathname === window.location.pathname) {
                history.replaceState(null, '', destino.pathname + destino.search + destino.hash);
                window.location.reload();
            } else {
                window.location.href = destino.href;
            }
        };

        formularios.forEach(form => {
            const entrada = $('[data-entrada]', form);
            const zona = $('[data-zona]', form);
            const destino = $('[data-destino]', form);
            const nombre = $('[data-nombre]', form);
            const pista = $('[data-pista]', form);
            const campoNombre = $('[data-campo-nombre]', form);
            const error = $('[data-error]', form);
            const progreso = $('[data-progreso]', form);
            const barra = $('[data-progreso-barra]', form);
            const textoProgreso = $('[data-progreso-texto]', form);
            const boton = $('[data-boton-guardar]', form);
            const automatico = form.hasAttribute('data-auto');
            const maximo = Number(form.dataset.max || 0);
            const aceptadas = (form.dataset.acepta || '').split(',').map(e => e.replace('.', '')).filter(Boolean);
            let enviando = false;

            const mostrarError = texto => {
                if (!error) return;
                error.textContent = texto || '';
                error.hidden = !texto;
                if (texto) Sonido.play('error');
            };
            const actualizarDestino = () => {
                if (campoNombre) campoNombre.hidden = Boolean(destino && destino.value);
            };
            const problema = archivo => {
                const ext = extension(archivo.name);
                if (!ext) return 'Ese archivo no tiene extensión (como .sb3 o .ino). Guárdalo desde su programa y vuelve a intentar.';
                if (aceptadas.length && !aceptadas.includes(ext)) return `Los archivos .${ext} no se pueden guardar aquí. Abre «¿Qué archivos puedo guardar?» para ver cuáles sí.`;
                if (!archivo.size) return 'Ese archivo está vacío. Ábrelo en su programa, guárdalo otra vez y vuelve a intentar.';
                if (maximo && archivo.size > maximo) return `Tu archivo pesa ${peso(archivo.size)} y lo más que se puede guardar es ${form.dataset.maxTexto || peso(maximo)} por archivo.`;
                return '';
            };

            function elegir() {
                const archivo = entrada.files[0];
                mostrarError('');
                zona?.classList.toggle('con-archivo', Boolean(archivo));
                if (!archivo) return;
                const fallo = problema(archivo);
                if (fallo) {
                    mostrarError(fallo);
                    entrada.value = '';
                    zona?.classList.remove('con-archivo');
                    return;
                }
                if (zona) {
                    $('[data-nombre-archivo]', zona).textContent = archivo.name;
                    $('[data-peso]', zona).textContent = peso(archivo.size);
                    $('[data-icono]', zona).textContent = iconos[extension(archivo.name)] || '📦';
                }
                Sonido.play('pop');
                if (automatico) return enviar();
                // ¿Ya tiene un proyecto con este mismo archivo? Entonces es su versión nueva
                if (destino) {
                    const igual = Array.from(destino.options).find(o => o.dataset.archivo && o.dataset.archivo === archivo.name.toLowerCase());
                    if (igual) destino.value = igual.value;
                    if (pista) {
                        pista.hidden = !igual;
                        pista.textContent = igual ? `🔁 Ya tienes «${igual.textContent.trim()}» con este archivo: se guardará como su versión nueva. Si es otro proyecto, cámbialo arriba.` : '';
                    }
                    actualizarDestino();
                }
                if (nombre && (!nombre.value.trim() || nombre.dataset.auto === '1')) {
                    nombre.value = sugerido(archivo.name);
                    nombre.dataset.auto = '1';
                }
            }

            function terminar(mensaje) {
                enviando = false;
                form.classList.remove('enviando');
                if (boton) boton.disabled = false;
                if (progreso) progreso.hidden = true;
                if (automatico) entrada.value = '';   // para poder elegir el mismo archivo otra vez
                mostrarError(mensaje);
            }

            function enviar() {
                if (enviando) return;
                const archivo = entrada.files[0];
                if (!archivo) { mostrarError('📂 Primero elige el archivo de tu proyecto.'); return; }
                const fallo = problema(archivo);
                if (fallo) { mostrarError(fallo); return; }
                enviando = true;
                mostrarError('');
                form.classList.add('enviando');
                if (boton) boton.disabled = true;
                if (progreso) progreso.hidden = false;
                if (barra) barra.style.width = '0%';
                if (textoProgreso) textoProgreso.textContent = 'Subiendo…';

                const xhr = new XMLHttpRequest();
                xhr.open('POST', form.action);
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                xhr.setRequestHeader('X-CSRFToken', csrf());
                xhr.upload.addEventListener('progress', e => {
                    if (!e.lengthComputable) return;
                    const pct = Math.round(e.loaded * 100 / e.total);
                    if (barra) barra.style.width = `${pct}%`;
                    if (textoProgreso) textoProgreso.textContent = pct < 100 ? `Subiendo… ${pct} %` : 'Guardando en tu carpeta…';
                });
                xhr.addEventListener('load', () => {
                    let datos = null;
                    try { datos = JSON.parse(xhr.responseText); } catch (e) { datos = null; }
                    if (xhr.status >= 200 && xhr.status < 300 && datos && datos.ok) {
                        if (barra) barra.style.width = '100%';
                        if (textoProgreso) textoProgreso.textContent = '¡Guardado! ✅';
                        irA(datos.redirect);
                    } else {
                        terminar((datos && datos.mensaje) || 'No se pudo guardar tu archivo. Inténtalo otra vez en un momento.');
                    }
                });
                xhr.addEventListener('error', () => terminar('Se cortó el internet mientras subías tu archivo. Revisa la conexión e inténtalo otra vez.'));
                xhr.send(new FormData(form));
            }

            entrada.addEventListener('change', elegir);
            destino?.addEventListener('change', () => { if (pista) pista.hidden = true; actualizarDestino(); });
            nombre?.addEventListener('input', () => { nombre.dataset.auto = ''; });
            form.addEventListener('submit', e => { e.preventDefault(); enviar(); });
            if (zona) {
                ['dragenter', 'dragover'].forEach(t => zona.addEventListener(t, () => zona.classList.add('arrastrando')));
                ['dragleave', 'drop'].forEach(t => zona.addEventListener(t, () => zona.classList.remove('arrastrando')));
            }
        });

        // Si suelta el archivo en cualquier parte de la página, va al formulario principal (y no se abre en el navegador)
        const principal = formularios.find(f => !f.hasAttribute('data-auto'));
        if (principal) {
            window.addEventListener('dragover', e => { if (!e.target.closest?.('input[type=file]')) e.preventDefault(); });
            window.addEventListener('drop', e => {
                if (e.target.closest?.('input[type=file]') || !e.dataTransfer?.files?.length) return;
                e.preventDefault();
                const entrada = $('[data-entrada]', principal);
                try { entrada.files = e.dataTransfer.files; } catch (err) { return; }
                entrada.dispatchEvent(new Event('change'));
                principal.scrollIntoView({ behavior: 'smooth', block: 'center' });
            });
        }

        $$('[data-renombrar]').forEach(btn => btn.addEventListener('click', async () => {
            if (typeof Swal === 'undefined') return;
            const r = await Swal.fire({
                title: '✏️ Nuevo nombre',
                input: 'text',
                inputValue: btn.dataset.nombre,
                inputAttributes: { maxlength: 80, 'aria-label': 'Nuevo nombre del proyecto' },
                showCancelButton: true,
                reverseButtons: true,
                buttonsStyling: false,
                confirmButtonText: 'Guardar',
                cancelButtonText: 'Cancelar',
                customClass: { popup: 'swal-juego', confirmButton: 'g-btn', cancelButton: 'g-btn blanco' },
                inputValidator: valor => (!valor.trim() ? 'Escribe el nuevo nombre.' : undefined),
            });
            if (!r.isConfirmed) return;
            try {
                const datos = await postJSON(btn.dataset.renombrar, { nombre: r.value });
                if (datos.ok) return irA(datos.redirect);
                Swal.fire({ icon: 'error', title: '¡Ups!', text: datos.mensaje, buttonsStyling: false, customClass: { popup: 'swal-juego', confirmButton: 'g-btn rojo' } });
            } catch (e) {
                Swal.fire({ icon: 'error', title: '¡Ups!', text: 'No se pudo cambiar el nombre. Inténtalo otra vez.', buttonsStyling: false, customClass: { popup: 'swal-juego', confirmButton: 'g-btn rojo' } });
            }
        }));

        $$('form[data-confirmar-g]').forEach(form => form.addEventListener('submit', e => {
            if (form.dataset.confirmado) return;
            e.preventDefault();
            const enviar = () => { form.dataset.confirmado = '1'; form.submit(); };
            if (typeof Swal === 'undefined') { if (window.confirm(form.dataset.confirmarG)) enviar(); return; }
            Sonido.play('pop');
            Swal.fire({
                title: form.dataset.titulo || '¿Seguro?',
                text: form.dataset.confirmarG,
                icon: 'warning',
                showCancelButton: true,
                reverseButtons: true,
                buttonsStyling: false,
                confirmButtonText: form.dataset.boton || 'Sí',
                cancelButtonText: 'Mejor no',
                customClass: { popup: 'swal-juego', confirmButton: 'g-btn rojo', cancelButton: 'g-btn blanco' },
            }).then(r => { if (r.isConfirmed) enviar(); });
        }));
    }

    document.addEventListener('DOMContentLoaded', () => {
        // Los modales viven en <body> para que ningún contenedor con z-index los tape
        $$('.modal').forEach(modal => document.body.appendChild(modal));
        iniciarBotonSonido();
        iniciarNotificaciones();
        iniciarDiarias();
        iniciarCofres();
        iniciarQuiz();
        iniciarTienda();
        iniciarMision();
        iniciarPin();
        iniciarClicks();
        iniciarAvisoBatalla();
        iniciarAvisosProfe();
        iniciarProyectos();
        mostrarCelebracionesPendientes();
        $$('.barra > span[data-ancho]').forEach(barra => {
            requestAnimationFrame(() => { barra.style.width = barra.dataset.ancho + '%'; });
        });
    });
})();

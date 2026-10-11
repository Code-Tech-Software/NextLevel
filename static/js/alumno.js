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
        });
    }

    // ---------- Pulsaciones de botones ----------
    function iniciarClicks() {
        document.addEventListener('pointerdown', e => {
            if (e.target.closest('.g-btn, .nodo, .filtro, .mundo-card')) Sonido.play('click');
        });
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
        mostrarCelebracionesPendientes();
        $$('.barra > span[data-ancho]').forEach(barra => {
            requestAnimationFrame(() => { barra.style.width = barra.dataset.ancho + '%'; });
        });
    });
})();

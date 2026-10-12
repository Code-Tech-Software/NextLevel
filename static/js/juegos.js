/* =========================================================
   Next-Level · Motor de minijuegos
   «Mecanografía de meteoros» y «Teclado misterioso».
   Corre igual en el alumno (misiones y Arcade) y en el panel
   del profe (vista previa «Probar», sin guardar nada).
   ========================================================= */
(function () {
    'use strict';

    const esc = t => String(t ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
    const sinAcentos = t => t.normalize('NFD').replace(/[̀-ͯ]/g, '');
    const azar = lista => lista[Math.floor(Math.random() * lista.length)];
    const miles = n => Number(n || 0).toLocaleString('es-MX');

    // ---------- Sonidos: respetan el botón de sonido del alumno (en el panel no suenan) ----------
    let audio = null;
    function tono(freq, dur, tipo = 'square', vol = 0.04, retraso = 0) {
        if (!window.NLSonido || !window.NLSonido.activo) return;
        try {
            audio = audio || new (window.AudioContext || window.webkitAudioContext)();
            if (audio.state === 'suspended') audio.resume();
            const t = audio.currentTime + retraso;
            const osc = audio.createOscillator();
            const gain = audio.createGain();
            osc.type = tipo;
            osc.frequency.setValueAtTime(freq, t);
            gain.gain.setValueAtTime(0.0001, t);
            gain.gain.exponentialRampToValueAtTime(vol, t + 0.01);
            gain.gain.exponentialRampToValueAtTime(0.0001, t + dur);
            osc.connect(gain).connect(audio.destination);
            osc.start(t);
            osc.stop(t + dur + 0.02);
        } catch (e) { /* sin audio */ }
    }
    const sfx = {
        tecla: () => tono(760, 0.035, 'triangle', 0.03),
        error: () => tono(170, 0.12, 'sawtooth', 0.035),
        boom: () => { tono(160, 0.16, 'sawtooth', 0.05); tono(90, 0.22, 'square', 0.03, 0.04); },
        acierto: () => { tono(880, 0.06, 'triangle', 0.05); tono(1320, 0.09, 'triangle', 0.04, 0.05); },
        estrella: () => [988, 1319, 1568].forEach((f, i) => tono(f, 0.12, 'square', 0.035, i * 0.07)),
        golpe: () => tono(110, 0.3, 'sawtooth', 0.06),
        cuenta: () => tono(520, 0.12, 'square', 0.04),
        ya: () => tono(1040, 0.25, 'square', 0.05),
        fin: () => [523, 659, 784, 1047].forEach((f, i) => tono(f, 0.18, 'triangle', 0.06, i * 0.1)),
        triste: () => [392, 330, 262].forEach((f, i) => tono(f, 0.2, 'triangle', 0.05, i * 0.14)),
    };

    // ---------- Reglas (las mismas que Misiones/minijuegos.py) ----------
    const VELOCIDADES = { lenta: { intervalo: 2.8, caida: 10 }, normal: { intervalo: 2.1, caida: 7.5 }, rapida: { intervalo: 1.6, caida: 5.8 } };
    const estrellasDe = c => (c >= 90 ? 3 : c >= 70 ? 2 : c >= 50 ? 1 : 0);

    function completar(plantilla, cfg = {}) {
        if (plantilla === 'atajos') {
            const atajos = (cfg.atajos || []).filter(a => cfg.catalogo?.[a]);
            return { atajos: atajos.length >= 2 ? atajos : Object.keys(cfg.catalogo || {}).slice(0, 4), catalogo: cfg.catalogo || {},
                rondas: cfg.rondas || 10, modo: cfg.modo === 'ninja' ? 'ninja' : 'aprende' };
        }
        if (plantilla === 'mensaje') {
            const palabras = [...new Set((cfg.palabras || []).map(normalizarSecreto))].filter(p => p.length >= 2 && p.length <= 12);
            const lista = palabras.length >= 3 ? palabras : ['ROBOT', 'MOUSE', 'TECLADO', 'MONITOR'];
            return { cifrado: cfg.cifrado || 'simbolos', palabras: lista, rondas: Math.min(cfg.rondas || 5, lista.length),
                desplazamiento: cfg.desplazamiento || 3, intentos: cfg.intentos || 3 };
        }
        if (plantilla === 'rutas') {
            return { modo: cfg.modo === 'buscar' ? 'buscar' : 'ruta', dificultad: ['media', 'dificil'].includes(cfg.dificultad) ? cfg.dificultad : 'facil',
                rondas: cfg.rondas || 5 };
        }
        if (plantilla === 'formato') {
            const frases = (cfg.frases || []).filter(f => f.split(' ').length >= 2);
            return { dificultad: ['media', 'dificil'].includes(cfg.dificultad) ? cfg.dificultad : 'facil', rondas: cfg.rondas || 5,
                frases: frases.length >= 3 ? frases : ['Mi robot tiene dos motores', 'El teclado sirve para escribir', 'Guarda tu trabajo cada rato'],
                intentos: cfg.intentos || 3 };
        }
        if (plantilla === 'clasifica') {
            const validas = (cfg.categorias || []).filter(c => c.nombre && (c.tarjetas || []).length);
            const categorias = validas.length >= 2 ? validas.slice(0, 3) : [
                { nombre: 'Seguro', emoji: '✅', tarjetas: ['Pedir permiso antes de descargar', 'Usar una contraseña difícil'] },
                { nombre: 'Peligroso', emoji: '⚠️', tarjetas: ['Dar tu contraseña', 'Abrir enlaces raros'] },
            ];
            const total = categorias.reduce((n, c) => n + c.tarjetas.length, 0);
            return { categorias, rondas: Math.min(cfg.rondas || 10, total), tiempo: cfg.tiempo ?? 8 };
        }
        if (plantilla === 'robot') {
            const dificultad = TABLEROS[cfg.dificultad] ? cfg.dificultad : 'facil';
            return {
                dificultad, niveles: cfg.niveles || 5, modo: cfg.modo === 'giros' ? 'giros' : 'flechas', bucles: !!cfg.bucles,
                intentos: cfg.intentos || 3, tablero: cfg.tablero || TABLEROS[dificultad],
            };
        }
        if (plantilla === 'teclado') {
            return { teclas: cfg.teclas || 'ASDFGHJKLÑ', rondas: cfg.rondas || 20, modo: cfg.modo === 'reto' ? 'reto' : 'guiado' };
        }
        const velocidad = VELOCIDADES[cfg.velocidad] ? cfg.velocidad : 'normal';
        const duracion = cfg.duracion || 60;
        return {
            palabras: (cfg.palabras || []).length >= 3 ? cfg.palabras : ['monitor', 'teclado', 'mouse', 'bocina', 'memoria'],
            duracion, velocidad, vidas: cfg.vidas || 3, acentos: cfg.acentos === 'exactos' ? 'exactos' : 'opcionales',
            meta: cfg.meta || Math.max(5, Math.round(duracion / VELOCIDADES[velocidad].intervalo * 0.7)),
            ...VELOCIDADES[velocidad],
        };
    }

    function calificarLocal(plantilla, cfg, s) {
        if (['atajos', 'mensaje', 'rutas', 'formato'].includes(plantilla)) {
            const c = Math.round(s.aciertos * 100 / cfg.rondas);
            const intentos = s.aciertos + s.errores;
            return {
                calificacion: c, estrellas: estrellasDe(c), puntaje: s.aciertos * 100 + s.perfectos * 50, aciertos: s.aciertos,
                errores: s.errores, precision: intentos ? Math.round(s.aciertos * 100 / intentos) : 0, ppm: 0,
            };
        }
        if (plantilla === 'clasifica') {
            const c = Math.round(s.aciertos * 100 / cfg.rondas);
            return {
                calificacion: c, estrellas: estrellasDe(c), puntaje: s.aciertos * 100 + s.rapidas * 50, aciertos: s.aciertos,
                errores: s.completadas - s.aciertos, precision: s.completadas ? Math.round(s.aciertos * 100 / s.completadas) : 0, ppm: 0,
            };
        }
        if (plantilla === 'robot') {
            const c = Math.round(s.resueltos * 100 / cfg.niveles);
            const intentos = s.resueltos + s.errores;
            return {
                calificacion: c, estrellas: estrellasDe(c), puntaje: s.resueltos * 150 + s.perfectos * 75, aciertos: s.resueltos,
                errores: s.errores, precision: intentos ? Math.round(s.resueltos * 100 / intentos) : 0, ppm: 0,
            };
        }
        if (plantilla === 'teclado') {
            const c = Math.round(s.aciertos * 100 / cfg.rondas);
            const presionadas = s.completadas + s.errores;
            return {
                calificacion: c, estrellas: estrellasDe(c), puntaje: s.aciertos * 100 + (s.completadas - s.aciertos) * 40 + s.rapidas * 50,
                aciertos: s.aciertos, errores: s.errores, precision: presionadas ? Math.round(s.completadas * 100 / presionadas) : 0, ppm: 0,
            };
        }
        const c = Math.min(100, Math.round(s.destruidos * 100 / cfg.meta));
        const teclas = s.caracteres + s.errores;
        return {
            calificacion: c, estrellas: estrellasDe(c), puntaje: s.caracteres * 10 + s.destruidos * 20 + s.vidas * 50,
            aciertos: s.destruidos, errores: s.errores, precision: teclas ? Math.round(s.caracteres * 100 / teclas) : 0,
            ppm: s.duracion >= 5 ? Math.min(200, Math.round((s.caracteres / 5) / (s.duracion / 60))) : 0,
        };
    }

    // =========================================================
    // MECANOGRAFÍA DE METEOROS
    // =========================================================
    function motorMeteoros(zonaJuego, cfg, hud, fin) {
        zonaJuego.innerHTML = `
            <div class="jm-cielo" aria-hidden="true"></div>
            <div class="jm-zona" data-zona></div>
            <div class="jm-suelo" data-suelo aria-hidden="true"><div class="jm-escudo"></div><div class="jm-ciudad">🏠🏫🏢🏡🏬🏠</div></div>
            <div class="jm-consola" data-consola>
                <div class="jm-escrito" data-escrito></div>
                <input class="jm-entrada" data-entrada type="text" autocomplete="off" autocorrect="off" autocapitalize="off"
                       spellcheck="false" enterkeyhint="done" aria-label="Escribe la palabra de un meteoro">
            </div>`;
        const zona = zonaJuego.querySelector('[data-zona]');
        const suelo = zonaJuego.querySelector('[data-suelo]');
        const consola = zonaJuego.querySelector('[data-consola]');
        const escrito = zonaJuego.querySelector('[data-escrito]');
        const entrada = zonaJuego.querySelector('[data-entrada]');
        const normalizar = t => (cfg.acentos === 'exactos' ? t.toLowerCase() : sinAcentos(t.toLowerCase()));
        const palabras = cfg.palabras.map(texto => ({ texto, norm: normalizar(texto) }));
        const cortes = [50, 70, 90].map(p => Math.ceil(cfg.meta * p / 100));

        let meteoros = [];
        let t = 0;
        let ultimoCuadro = 0;
        let proximo = 0.4;
        let cuadro = null;
        let activo = false;
        let pausado = false;
        let vidas = cfg.vidas;
        let destruidos = 0;
        let caracteres = 0;
        let errores = 0;
        let puntos = 0;
        let objetivo = null;
        let valorValido = '';
        let hudPrevio = '';

        function pintarHud() {
            const restante = Math.max(0, Math.ceil(cfg.duracion - t));
            const estrellas = estrellasDe(Math.min(100, Math.round(destruidos * 100 / cfg.meta)));
            const html = `
                <span class="chip-hud ${restante <= 10 ? 'alerta' : ''}"><i class="bi bi-stopwatch"></i> ${restante}s</span>
                <span class="chip-hud vidas" title="Vidas">${'❤️'.repeat(Math.max(0, vidas))}${'🖤'.repeat(Math.max(0, cfg.vidas - vidas))}</span>
                <span class="chip-hud">☄️ ${destruidos}/${cfg.meta}</span>
                <span class="chip-hud estrellas" title="Estrellas">${[1, 2, 3].map(i => `<span class="${i <= estrellas ? 'on' : ''}">★</span>`).join('')}</span>
                <span class="chip-hud puntos">${miles(puntos)}</span>`;
            if (html !== hudPrevio) { hud.innerHTML = html; hudPrevio = html; }
        }
        function pintarEscrito() {
            escrito.innerHTML = valorValido ? esc(valorValido) : '<span class="ph">Escribe la palabra de un meteoro…</span>';
        }
        function marcar(m, largo) {
            m.el.querySelector('.ok').textContent = m.texto.slice(0, largo);
            m.el.querySelector('.resto').textContent = m.texto.slice(largo);
            m.el.classList.toggle('fijado', largo > 0);
        }
        function progreso(m) { return (t - m.nacido) / m.caida; }

        function elegirPalabra() {
            const enPantalla = new Set(meteoros.map(m => m.norm));
            const iniciales = new Set(meteoros.map(m => m.norm[0]));
            let opciones = palabras.filter(p => !enPantalla.has(p.norm) && !iniciales.has(p.norm[0]));
            if (!opciones.length) opciones = palabras.filter(p => !enPantalla.has(p.norm));
            return opciones.length ? azar(opciones) : null;
        }
        function lanzar() {
            const palabra = elegirPalabra();
            if (!palabra) return;
            const avance = Math.min(1, t / cfg.duracion);
            const el = document.createElement('div');
            el.className = 'jm-meteoro';
            el.innerHTML = `<span class="roca" aria-hidden="true">☄️</span><span class="palabra"><span class="ok"></span><span class="resto">${esc(palabra.texto)}</span></span>`;
            el.style.left = `${14 + Math.random() * 72}%`;
            zona.appendChild(el);
            meteoros.push({ ...palabra, el, nacido: t, caida: cfg.caida * (1 - 0.25 * avance) });
        }
        function efecto(clase, html, m) {
            const fx = document.createElement('div');
            fx.className = clase;
            fx.innerHTML = html;
            const caja = m.el.getBoundingClientRect();
            const base = zona.getBoundingClientRect();
            fx.style.left = `${caja.left - base.left + caja.width / 2}px`;
            fx.style.top = `${caja.top - base.top + caja.height / 2}px`;
            zona.appendChild(fx);
            setTimeout(() => fx.remove(), 900);
        }
        function quitar(m, clase) {
            meteoros = meteoros.filter(x => x !== m);
            m.el.classList.add(clase);
            setTimeout(() => m.el.remove(), 450);
        }
        function limpiarEntrada() {
            objetivo = null;
            valorValido = '';
            entrada.value = '';
            pintarEscrito();
        }

        function destruir(m) {
            const antes = estrellasDe(Math.min(100, Math.round(destruidos * 100 / cfg.meta)));
            destruidos += 1;
            caracteres += m.texto.length;
            const ganados = m.texto.length * 10 + 20;
            puntos += ganados;
            efecto('jm-boom', '💥', m);
            efecto('jm-puntos', `+${ganados}`, m);
            quitar(m, 'destruido');
            limpiarEntrada();
            if (estrellasDe(Math.min(100, Math.round(destruidos * 100 / cfg.meta))) > antes) {
                sfx.estrella();
                hud.classList.remove('brillo');
                void hud.offsetWidth;
                hud.classList.add('brillo');
            } else {
                sfx.boom();
            }
        }
        function impacto(m) {
            quitar(m, 'impacto');
            vidas -= 1;
            sfx.golpe();
            suelo.classList.remove('golpe');
            void suelo.offsetWidth;
            suelo.classList.add('golpe');
            zonaJuego.classList.remove('temblor');
            void zonaJuego.offsetWidth;
            zonaJuego.classList.add('temblor');
            if (objetivo === m) limpiarEntrada();
            if (vidas <= 0) terminar(false);
        }

        function alEscribir() {
            if (!activo) return;
            const valor = entrada.value.replace(/\s+/g, ' ').replace(/^ /, '');
            const n = normalizar(valor);
            let candidato = null;
            if (n) {
                candidato = objetivo && meteoros.includes(objetivo) && objetivo.norm.startsWith(n) ? objetivo
                    : meteoros.filter(m => m.norm.startsWith(n)).sort((a, b) => progreso(b) - progreso(a))[0] || null;
            }
            if (n && !candidato) {
                // Letra equivocada: se rechaza y se queda lo último que sí coincidía
                errores += 1;
                sfx.error();
                entrada.value = valorValido;
                consola.classList.remove('mal');
                void consola.offsetWidth;
                consola.classList.add('mal');
                clearTimeout(consola.quitarMal);
                consola.quitarMal = setTimeout(() => consola.classList.remove('mal'), 350);
                return;
            }
            if (valor.length > valorValido.length) sfx.tecla();
            if (objetivo && objetivo !== candidato && meteoros.includes(objetivo)) marcar(objetivo, 0);
            objetivo = candidato;
            valorValido = valor;
            pintarEscrito();
            if (objetivo) {
                marcar(objetivo, valor.length);
                if (n === objetivo.norm) destruir(objetivo);
            }
        }

        function bucle(ahora) {
            if (!activo) return;
            const dt = ultimoCuadro ? Math.min(0.1, (ahora - ultimoCuadro) / 1000) : 0;
            ultimoCuadro = ahora;
            if (!pausado) {
                t += dt;
                if (t >= proximo && t < cfg.duracion - 1) {
                    lanzar();
                    const avance = Math.min(1, t / cfg.duracion);
                    proximo = t + cfg.intervalo * (1 - 0.3 * avance) * (0.85 + Math.random() * 0.3);
                }
                const alto = zona.clientHeight - 64;
                for (const m of meteoros.slice()) {
                    const p = progreso(m);
                    if (p >= 1) { impacto(m); if (!activo) return; continue; }
                    m.el.style.transform = `translate(-50%, ${Math.max(0, p * alto)}px)`;
                    m.el.classList.toggle('cerca', p > 0.72);
                }
                pintarHud();
                if (t >= cfg.duracion) { terminar(true); return; }
            }
            cuadro = requestAnimationFrame(bucle);
        }

        function enfocar() { if (activo) entrada.focus({ preventScroll: true }); }
        const alCambiarVisibilidad = () => { pausado = document.hidden; ultimoCuadro = 0; };
        const alTeclear = e => {
            if (e.key !== 'Enter') return;
            e.preventDefault();
            if (objetivo && meteoros.includes(objetivo)) marcar(objetivo, 0);
            limpiarEntrada();
        };

        function terminar(sobrevivio) {
            if (!activo) return;
            activo = false;
            cancelAnimationFrame(cuadro);
            document.removeEventListener('visibilitychange', alCambiarVisibilidad);
            entrada.disabled = true;
            entrada.blur();
            meteoros.forEach(m => m.el.classList.add('congelado'));
            pintarHud();
            setTimeout(() => fin({ destruidos, caracteres, errores, vidas: sobrevivio ? vidas : 0, duracion: Math.round(t) }), 700);
        }

        return {
            iniciar() {
                activo = true;
                pintarEscrito();
                pintarHud();
                entrada.addEventListener('input', alEscribir);
                entrada.addEventListener('keydown', alTeclear);
                entrada.addEventListener('blur', () => setTimeout(enfocar, 60));
                zonaJuego.addEventListener('pointerdown', () => setTimeout(enfocar, 0));
                document.addEventListener('visibilitychange', alCambiarVisibilidad);
                enfocar();
                cuadro = requestAnimationFrame(bucle);
            },
            detener() {
                activo = false;
                cancelAnimationFrame(cuadro);
                document.removeEventListener('visibilitychange', alCambiarVisibilidad);
            },
            cortes,
        };
    }

    // =========================================================
    // TECLADO MISTERIOSO
    // =========================================================
    const FILAS = ['1234567890', 'QWERTYUIOP', 'ASDFGHJKLÑ', 'ZXCVBNM'];

    function motorTeclado(zonaJuego, cfg, hud, fin) {
        const teclas = [...cfg.teclas];
        const conNumeros = teclas.some(k => /\d/.test(k));
        zonaJuego.innerHTML = `
            <div class="jt-zona">
                <div class="jt-caja" data-caja><span class="jt-letra" data-letra aria-live="assertive"></span></div>
                <div class="jt-mensaje" data-mensaje></div>
                <div class="jt-barra"><span data-barra></span></div>
                <div class="jt-teclado" data-teclado>
                    ${FILAS.map((fila, i) => (i === 0 && !conNumeros ? '' : `<div class="fila f${i}">${[...fila].map(k => `
                        <button type="button" tabindex="-1" class="jt-tecla ${teclas.includes(k) ? 'en-juego' : ''} ${k === 'F' || k === 'J' ? 'guia' : ''}"
                                data-tecla="${k}">${k}</button>`).join('')}</div>`)).join('')}
                    <div class="fila"><span class="jt-espacio"></span></div>
                </div>
            </div>`;
        const caja = zonaJuego.querySelector('[data-caja]');
        const letra = zonaJuego.querySelector('[data-letra]');
        const mensaje = zonaJuego.querySelector('[data-mensaje]');
        const barra = zonaJuego.querySelector('[data-barra]');
        const teclado = zonaJuego.querySelector('[data-teclado]');
        const boton = k => teclado.querySelector(`[data-tecla="${k}"]`);

        let completadas = 0;
        let aciertos = 0;
        let errores = 0;
        let rapidas = 0;
        let puntos = 0;
        let objetivo = null;
        let anterior = null;
        let erroresRonda = 0;
        let inicioRonda = 0;
        let inicio = 0;
        let activo = false;
        let esperando = false;
        let reloj = null;

        function pintarHud() {
            const segundos = inicio ? Math.floor((performance.now() - inicio) / 1000) : 0;
            const estrellas = estrellasDe(Math.round(aciertos * 100 / cfg.rondas));
            hud.innerHTML = `
                <span class="chip-hud">🔤 ${Math.min(completadas + 1, cfg.rondas)}/${cfg.rondas}</span>
                <span class="chip-hud">✅ ${aciertos}</span>
                <span class="chip-hud"><i class="bi bi-stopwatch"></i> ${segundos}s</span>
                <span class="chip-hud estrellas" title="Estrellas">${[1, 2, 3].map(i => `<span class="${i <= estrellas ? 'on' : ''}">★</span>`).join('')}</span>
                <span class="chip-hud puntos">${miles(puntos)}</span>`;
        }
        function animar(el, clase, duracion = 0) {
            el.classList.remove(clase);
            void el.offsetWidth;
            el.classList.add(clase);
            if (duracion) setTimeout(() => el.classList.remove(clase), duracion);
        }
        function siguiente() {
            if (completadas >= cfg.rondas) { terminar(); return; }
            let k;
            do { k = azar(teclas); } while (teclas.length > 1 && k === anterior);
            anterior = k;
            objetivo = k;
            erroresRonda = 0;
            inicioRonda = performance.now();
            letra.textContent = k;
            caja.classList.remove('mal');
            animar(caja, 'pop');
            teclado.querySelectorAll('.objetivo').forEach(b => b.classList.remove('objetivo', 'pista'));
            if (cfg.modo === 'guiado') boton(k)?.classList.add('objetivo');
            mensaje.textContent = cfg.modo === 'guiado' ? '¡Presiona en tu teclado la tecla que brilla!' : '¿Dónde está esta tecla? ¡Encuéntrala en tu teclado!';
            barra.style.width = `${completadas * 100 / cfg.rondas}%`;
            pintarHud();
        }
        function presionar(k) {
            if (!activo || esperando || !objetivo) return;
            const b = boton(k);
            if (k === objetivo) {
                completadas += 1;
                if (!erroresRonda) {
                    aciertos += 1;
                    puntos += 100;
                    if ((performance.now() - inicioRonda) / 1000 < 1.5) {
                        rapidas += 1;
                        puntos += 50;
                        mensaje.textContent = '⚡ ¡Súper rápido!';
                    } else {
                        mensaje.textContent = azar(['¡Bien!', '¡Excelente!', '¡Eso es!', '¡Muy bien!']);
                    }
                } else {
                    puntos += 40;
                    mensaje.textContent = '¡La encontraste!';
                }
                if (b) animar(b, 'bien', 260);
                sfx.acierto();
                esperando = true;
                barra.style.width = `${completadas * 100 / cfg.rondas}%`;
                pintarHud();
                setTimeout(() => { esperando = false; siguiente(); }, 280);
            } else {
                errores += 1;
                erroresRonda += 1;
                sfx.error();
                if (b) animar(b, 'mal', 320);
                animar(caja, 'mal');
                if (cfg.modo === 'reto' && erroresRonda >= 2) {
                    boton(objetivo)?.classList.add('objetivo', 'pista');
                    mensaje.textContent = '💡 ¡Pista! Busca la tecla que brilla';
                } else {
                    mensaje.textContent = `Esa es la ${k}. ¡Intenta otra vez!`;
                }
            }
        }
        const alTeclear = e => {
            if (e.ctrlKey || e.metaKey || e.altKey) return;
            const k = (e.key || '').toUpperCase();
            if (k.length !== 1 || !/[A-ZÑ0-9]/.test(k)) return;
            e.preventDefault();
            if (!e.repeat) presionar(k);
        };
        const alTocar = e => {
            const b = e.target.closest('[data-tecla]');
            if (b) presionar(b.dataset.tecla);
        };
        function terminar() {
            if (!activo) return;
            activo = false;
            clearInterval(reloj);
            document.removeEventListener('keydown', alTeclear);
            teclado.querySelectorAll('.objetivo').forEach(b => b.classList.remove('objetivo', 'pista'));
            letra.textContent = '🏁';
            mensaje.textContent = '¡Terminaste!';
            barra.style.width = '100%';
            const duracion = Math.round((performance.now() - inicio) / 1000);
            setTimeout(() => fin({ completadas, aciertos, errores, rapidas, duracion }), 600);
        }

        return {
            iniciar() {
                activo = true;
                inicio = performance.now();
                document.addEventListener('keydown', alTeclear);
                teclado.addEventListener('click', alTocar);
                reloj = setInterval(pintarHud, 500);
                siguiente();
            },
            detener() {
                activo = false;
                clearInterval(reloj);
                document.removeEventListener('keydown', alTeclear);
            },
        };
    }

    // =========================================================
    // DETECTIVE DIGITAL (clasificar tarjetas)
    // =========================================================
    const COLORES_GRUPO = ['#0ea5e9', '#f97316', '#a855f7'];
    const barajar = lista => {
        for (let i = lista.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [lista[i], lista[j]] = [lista[j], lista[i]];
        }
        return lista;
    };

    function motorClasifica(zonaJuego, cfg, hud, fin) {
        const grupos = cfg.categorias;
        const teclas = grupos.length === 2 ? ['ArrowLeft', 'ArrowRight'] : ['ArrowLeft', 'ArrowDown', 'ArrowRight'];
        const flechas = grupos.length === 2 ? ['←', '→'] : ['←', '↓', '→'];
        // El mazo toma tarjetas al azar; si se piden más de las que hay, se vuelve a barajar
        const todas = grupos.flatMap((g, i) => g.tarjetas.map(texto => ({ texto, grupo: i })));
        const mazo = [];
        while (mazo.length < cfg.rondas) mazo.push(...barajar(todas.slice()));
        mazo.length = cfg.rondas;

        zonaJuego.innerHTML = `
            <div class="jc-zona">
                <div class="jc-reloj ${cfg.tiempo ? '' : 'invisible'}"><span data-reloj></span></div>
                <div class="jc-mesa" data-mesa></div>
                <div class="jc-mensaje" data-mensaje aria-live="polite"></div>
                <div class="jc-grupos g${grupos.length}">
                    ${grupos.map((g, i) => `
                        <button type="button" class="jc-grupo" data-grupo="${i}" style="--gc:${COLORES_GRUPO[i]}">
                            <span class="e">${esc(g.emoji)}</span><span class="n">${esc(g.nombre)}</span>
                            <span class="atajo">${flechas[i]}</span>
                        </button>`).join('')}
                </div>
            </div>`;
        const mesa = zonaJuego.querySelector('[data-mesa]');
        const mensaje = zonaJuego.querySelector('[data-mensaje]');
        const barraReloj = zonaJuego.querySelector('[data-reloj]');
        const botonGrupo = i => zonaJuego.querySelector(`[data-grupo="${i}"]`);

        let indice = 0;
        let completadas = 0;
        let aciertos = 0;
        let rapidas = 0;
        let racha = 0;
        let mejorRacha = 0;
        let puntos = 0;
        let actual = null;
        let tarjeta = null;
        let inicioTarjeta = 0;
        let inicio = 0;
        let activo = false;
        let esperando = false;
        let reloj = null;

        function pintarHud() {
            const estrellas = estrellasDe(Math.round(aciertos * 100 / cfg.rondas));
            hud.innerHTML = `
                <span class="chip-hud">🃏 ${Math.min(indice + 1, cfg.rondas)}/${cfg.rondas}</span>
                <span class="chip-hud">✅ ${aciertos}</span>
                <span class="chip-hud ${racha >= 3 ? 'racha' : ''}">🔥 ${racha}</span>
                <span class="chip-hud estrellas" title="Estrellas">${[1, 2, 3].map(i => `<span class="${i <= estrellas ? 'on' : ''}">★</span>`).join('')}</span>
                <span class="chip-hud puntos">${miles(puntos)}</span>`;
        }
        function animar(el, clase, duracion) {
            if (!el) return;
            el.classList.remove(clase);
            void el.offsetWidth;
            el.classList.add(clase);
            setTimeout(() => el.classList.remove(clase), duracion);
        }
        function volar(el, destino) {
            const a = el.getBoundingClientRect();
            const b = destino.getBoundingClientRect();
            el.style.transition = 'transform .35s ease-in, opacity .35s ease-in';
            el.style.transform = `translate(${b.left + b.width / 2 - (a.left + a.width / 2)}px, ${b.top + b.height / 2 - (a.top + a.height / 2)}px) scale(.25) rotate(8deg)`;
            el.style.opacity = '0';
        }

        function nueva() {
            if (!activo) return;
            if (indice >= mazo.length) { terminar(); return; }
            actual = mazo[indice];
            mesa.innerHTML = `
                <div class="jc-tarjeta" data-tarjeta>
                    <span class="contador">${indice + 1} / ${mazo.length}</span>
                    <span class="texto">${esc(actual.texto)}</span>
                    <span class="pista">¿A qué grupo pertenece?</span>
                </div>`;
            tarjeta = mesa.querySelector('[data-tarjeta]');
            arrastrable(tarjeta);
            inicioTarjeta = performance.now();
            esperando = false;
            pintarHud();
        }

        function responder(grupo) {
            if (!activo || esperando || !actual) return;
            esperando = true;
            const segundos = (performance.now() - inicioTarjeta) / 1000;
            const correcto = grupos[actual.grupo];
            completadas += 1;
            if (grupo === actual.grupo) {
                const rapida = cfg.tiempo ? segundos < cfg.tiempo * 0.45 : segundos < 2.5;
                aciertos += 1;
                racha += 1;
                mejorRacha = Math.max(mejorRacha, racha);
                if (rapida) rapidas += 1;
                puntos += 100 + (rapida ? 50 : 0);
                sfx.acierto();
                animar(botonGrupo(grupo), 'bien', 450);
                volar(tarjeta, botonGrupo(grupo));
                mensaje.className = 'jc-mensaje ok';
                mensaje.textContent = racha >= 3 ? `🔥 ¡Racha de ${racha}!` : rapida ? '⚡ ¡Rapidísimo!' : azar(['¡Bien!', '¡Correcto!', '¡Eso es!']);
            } else {
                racha = 0;
                sfx.error();
                tarjeta.classList.add('mal');
                if (grupo !== null) animar(botonGrupo(grupo), 'mal', 500);
                animar(botonGrupo(actual.grupo), 'correcto', 1200);
                mensaje.className = 'jc-mensaje error';
                mensaje.innerHTML = `${grupo === null ? '⏰ ¡Se acabó el tiempo! ' : ''}Era <b>${esc(correcto.emoji)} ${esc(correcto.nombre)}</b>`;
            }
            indice += 1;
            pintarHud();
            setTimeout(nueva, grupo === actual.grupo ? 450 : 1400);
        }

        // Arrastrar la tarjeta hasta un grupo (o deslizarla a un lado si son dos)
        function arrastrable(el) {
            let x0 = 0;
            let y0 = 0;
            let moviendo = false;
            const grupoBajo = (x, y) => document.elementsFromPoint(x, y).map(n => n.closest?.('[data-grupo]')).find(Boolean);
            el.addEventListener('pointerdown', e => {
                if (esperando) return;
                moviendo = true;
                x0 = e.clientX;
                y0 = e.clientY;
                el.setPointerCapture(e.pointerId);
                el.classList.add('arrastrando');
            });
            el.addEventListener('pointermove', e => {
                if (!moviendo) return;
                const dx = e.clientX - x0;
                const dy = e.clientY - y0;
                el.style.transform = `translate(${dx}px, ${dy}px) rotate(${dx / 18}deg)`;
                zonaJuego.querySelectorAll('[data-grupo]').forEach(b => b.classList.remove('encima'));
                grupoBajo(e.clientX, e.clientY)?.classList.add('encima');
            });
            const soltar = e => {
                if (!moviendo) return;
                moviendo = false;
                el.classList.remove('arrastrando');
                zonaJuego.querySelectorAll('[data-grupo]').forEach(b => b.classList.remove('encima'));
                const dx = e.clientX - x0;
                const bajo = grupoBajo(e.clientX, e.clientY);
                if (bajo) responder(Number(bajo.dataset.grupo));
                else if (grupos.length === 2 && Math.abs(dx) > 90) responder(dx < 0 ? 0 : 1);
                else el.style.transform = '';
            };
            el.addEventListener('pointerup', soltar);
            el.addEventListener('pointercancel', soltar);
        }

        const alTeclear = e => {
            const porFlecha = teclas.indexOf(e.key);
            const porNumero = /^[1-3]$/.test(e.key) ? Number(e.key) - 1 : -1;
            const grupo = porFlecha >= 0 ? porFlecha : porNumero < grupos.length ? porNumero : -1;
            if (grupo < 0) return;
            e.preventDefault();
            if (!e.repeat) responder(grupo);
        };
        const alTocar = e => {
            const b = e.target.closest('[data-grupo]');
            if (b) responder(Number(b.dataset.grupo));
        };

        function terminar() {
            if (!activo) return;
            activo = false;
            clearInterval(reloj);
            document.removeEventListener('keydown', alTeclear);
            mesa.innerHTML = '<div class="jc-tarjeta fin"><span class="texto">🏁 ¡Caso cerrado!</span></div>';
            const duracion = Math.round((performance.now() - inicio) / 1000);
            setTimeout(() => fin({ completadas, aciertos, rapidas, racha: mejorRacha, duracion }), 600);
        }

        return {
            iniciar() {
                activo = true;
                inicio = performance.now();
                document.addEventListener('keydown', alTeclear);
                zonaJuego.querySelector('.jc-grupos').addEventListener('click', alTocar);
                if (cfg.tiempo) {
                    reloj = setInterval(() => {
                        if (!actual || esperando) return;
                        const restante = Math.max(0, 1 - (performance.now() - inicioTarjeta) / 1000 / cfg.tiempo);
                        barraReloj.style.width = `${restante * 100}%`;
                        barraReloj.classList.toggle('poco', restante < 0.3);
                        if (restante <= 0) responder(null);
                    }, 80);
                }
                nueva();
            },
            detener() {
                activo = false;
                clearInterval(reloj);
                document.removeEventListener('keydown', alTeclear);
            },
        };
    }

    // =========================================================
    // ROBOT PROGRAMADOR
    // =========================================================
    const TABLEROS = {
        facil: { tam: 5, obstaculos: [3, 5], camino: [3, 6] },
        media: { tam: 6, obstaculos: [6, 9], camino: [5, 9] },
        dificil: { tam: 7, obstaculos: [11, 15], camino: [8, 13] },
    };
    const DX = [0, 1, 0, -1];
    const DY = [-1, 0, 1, 0];
    const BLOQUES = {
        arriba: { e: '⬆️', t: 'Arriba', dir: 0 }, derecha: { e: '➡️', t: 'Derecha', dir: 1 },
        abajo: { e: '⬇️', t: 'Abajo', dir: 2 }, izquierda: { e: '⬅️', t: 'Izquierda', dir: 3 },
        avanzar: { e: '⬆️', t: 'Avanzar' }, girarIzq: { e: '↺', t: 'Girar izq.' }, girarDer: { e: '↻', t: 'Girar der.' },
        rep2: { e: '🔁', t: '×2', veces: 2 }, rep3: { e: '🔁', t: '×3', veces: 3 },
    };
    const entero = n => Math.floor(Math.random() * n);

    // Laberinto al azar que siempre tiene solución; «optimo» es el programa más corto sin repetir
    function generarLaberinto(tablero, modo) {
        const { tam, obstaculos: [omin, omax], camino: [cmin, cmax] } = tablero;
        const indice = (x, y) => y * tam + x;
        for (let intento = 0; intento < 400; intento++) {
            const inicio = { x: entero(tam), y: entero(tam) };
            const rocas = new Set();
            const cuantas = omin + entero(omax - omin + 1);
            while (rocas.size < cuantas) {
                const c = entero(tam * tam);
                if (c !== indice(inicio.x, inicio.y)) rocas.add(c);
            }
            const libre = (x, y) => x >= 0 && y >= 0 && x < tam && y < tam && !rocas.has(indice(x, y));
            const distancia = new Map([[indice(inicio.x, inicio.y), 0]]);
            const cola = [inicio];
            while (cola.length) {
                const { x, y } = cola.shift();
                for (let d = 0; d < 4; d++) {
                    const nx = x + DX[d];
                    const ny = y + DY[d];
                    if (libre(nx, ny) && !distancia.has(indice(nx, ny))) {
                        distancia.set(indice(nx, ny), distancia.get(indice(x, y)) + 1);
                        cola.push({ x: nx, y: ny });
                    }
                }
            }
            const candidatas = [...distancia].filter(([, d]) => d >= cmin && d <= cmax).map(([c]) => c);
            if (!candidatas.length) continue;
            const metaIndice = azar(candidatas);
            const meta = { x: metaIndice % tam, y: Math.floor(metaIndice / tam) };
            const dir = entero(4);
            let optimo = distancia.get(metaIndice);
            if (modo === 'giros') {
                // Camino más corto contando también los giros (estado = casilla + dirección)
                const clave = (x, y, d) => `${x},${y},${d}`;
                const vistos = new Map([[clave(inicio.x, inicio.y, dir), 0]]);
                const pendientes = [{ x: inicio.x, y: inicio.y, d: dir }];
                optimo = null;
                while (pendientes.length && optimo === null) {
                    const s = pendientes.shift();
                    const pasos = vistos.get(clave(s.x, s.y, s.d));
                    for (const sig of [{ x: s.x + DX[s.d], y: s.y + DY[s.d], d: s.d }, { ...s, d: (s.d + 3) % 4 }, { ...s, d: (s.d + 1) % 4 }]) {
                        if (!libre(sig.x, sig.y) || vistos.has(clave(sig.x, sig.y, sig.d))) continue;
                        vistos.set(clave(sig.x, sig.y, sig.d), pasos + 1);
                        if (sig.x === meta.x && sig.y === meta.y) { optimo = pasos + 1; break; }
                        pendientes.push(sig);
                    }
                }
            }
            return { tam, inicio, dir, meta, rocas, optimo };
        }
        return { tam, inicio: { x: 0, y: 0 }, dir: 1, meta: { x: 3, y: 0 }, rocas: new Set(), optimo: 3 };
    }

    function motorRobot(zonaJuego, cfg, hud, fin) {
        const giros = cfg.modo === 'giros';
        const paleta = [...(giros ? ['girarIzq', 'avanzar', 'girarDer'] : ['izquierda', 'arriba', 'abajo', 'derecha']),
            ...(cfg.bucles ? ['rep2', 'rep3'] : [])];
        const MAXIMO = 24;
        zonaJuego.innerHTML = `
            <div class="jr-zona">
                <div class="jr-tablero" data-tablero></div>
                <div class="jr-panel">
                    <div class="jr-mensaje" data-mensaje aria-live="polite"></div>
                    <div class="jr-programa" data-programa></div>
                    <div class="jr-paleta">
                        ${paleta.map(b => `<button type="button" class="jr-bloque ${b.startsWith('rep') ? 'repetir' : ''}" data-bloque="${b}" title="${BLOQUES[b].t}">
                            <span class="e">${BLOQUES[b].e}</span><span class="t">${BLOQUES[b].t}</span></button>`).join('')}
                    </div>
                    <div class="jr-acciones">
                        <button type="button" class="jr-accion" data-borrar title="Borrar el último (⌫)"><i class="bi bi-backspace"></i></button>
                        <button type="button" class="jr-accion" data-limpiar title="Borrar todo"><i class="bi bi-trash3"></i></button>
                        <button type="button" class="jr-ejecutar" data-ejecutar><i class="bi bi-play-fill"></i> Ejecutar</button>
                    </div>
                    <div class="jr-info" data-info></div>
                </div>
            </div>`;
        const tableroEl = zonaJuego.querySelector('[data-tablero]');
        const mensaje = zonaJuego.querySelector('[data-mensaje]');
        const programaEl = zonaJuego.querySelector('[data-programa]');
        const info = zonaJuego.querySelector('[data-info]');
        const ejecutarBtn = zonaJuego.querySelector('[data-ejecutar]');

        let nivel = 0;
        let resueltos = 0;
        let perfectos = 0;
        let errores = 0;
        let puntos = 0;
        let intentos = cfg.intentos;
        let laberinto = null;
        let robot = null;
        let robotEl = null;
        let programa = [];
        let corriendo = false;
        let activo = false;
        let inicio = 0;
        let pausas = [];

        const esperar = ms => new Promise(r => { pausas.push(setTimeout(r, ms)); });

        function pintarHud() {
            const estrellas = estrellasDe(Math.round(resueltos * 100 / cfg.niveles));
            hud.innerHTML = `
                <span class="chip-hud">🧩 ${Math.min(nivel + 1, cfg.niveles)}/${cfg.niveles}</span>
                <span class="chip-hud">🔋 ${resueltos}</span>
                <span class="chip-hud" title="Intentos">${'❤️'.repeat(intentos)}${'🖤'.repeat(cfg.intentos - intentos)}</span>
                <span class="chip-hud estrellas" title="Estrellas">${[1, 2, 3].map(i => `<span class="${i <= estrellas ? 'on' : ''}">★</span>`).join('')}</span>
                <span class="chip-hud puntos">${miles(puntos)}</span>`;
        }
        function decir(texto, tipo = '') {
            mensaje.className = `jr-mensaje ${tipo}`;
            mensaje.innerHTML = texto;
        }
        function pintarPrograma(activoIndice = -1, repIndice = -1) {
            programaEl.innerHTML = programa.length
                ? programa.map((b, i) => `<button type="button" class="jr-chip ${b.startsWith('rep') ? 'repetir' : ''} ${i === activoIndice || i === repIndice ? 'activo' : ''}"
                        data-quitar="${i}" title="Quitar">${BLOQUES[b].e}${b.startsWith('rep') ? `<small>${BLOQUES[b].t}</small>` : ''}</button>`).join('')
                : `<span class="vacio">${giros ? 'Toca «Avanzar» y los giros para armar tu programa' : 'Toca las flechas para armar tu programa'}</span>`;
            info.innerHTML = `${programa.length}/${MAXIMO} bloques · Código perfecto: <b>${laberinto.optimo}</b> bloques o menos`;
        }
        function colocarRobot(animado = true) {
            robotEl.classList.toggle('sin-animacion', !animado);
            robotEl.style.setProperty('--x', robot.x);
            robotEl.style.setProperty('--y', robot.y);
            robotEl.style.setProperty('--giro', `${robot.giro}deg`);
        }
        function cargarNivel() {
            laberinto = generarLaberinto(cfg.tablero, cfg.modo);
            const { tam, inicio: ini, meta, rocas } = laberinto;
            tableroEl.style.setProperty('--tam', tam);
            let celdas = '';
            for (let y = 0; y < tam; y++) {
                for (let x = 0; x < tam; x++) {
                    const c = y * tam + x;
                    const tipo = rocas.has(c) ? 'roca' : x === meta.x && y === meta.y ? 'meta' : x === ini.x && y === ini.y ? 'inicio' : '';
                    celdas += `<div class="jr-celda ${tipo}" data-celda="${x},${y}">${tipo === 'roca' ? '🪨' : tipo === 'meta' ? '🔋' : ''}</div>`;
                }
            }
            tableroEl.innerHTML = `${celdas}<div class="jr-robot" data-robot><span class="orbita" aria-hidden="true"><span class="dir">▲</span></span><span class="cara">🤖</span></div>`;
            robotEl = tableroEl.querySelector('[data-robot]');
            robot = { x: ini.x, y: ini.y, dir: laberinto.dir, giro: laberinto.dir * 90 };
            colocarRobot(false);
            programa = [];
            intentos = cfg.intentos;
            pintarPrograma();
            pintarHud();
            decir(nivel === 0
                ? (giros ? '🤖 El robot avanza hacia donde apunta su flecha. ¡Llévalo a la 🔋!' : '🤖 Arma un programa con flechas para llevar al robot a la 🔋.')
                : `🧩 Laberinto ${nivel + 1}. ¡Tú puedes!`);
        }
        function reiniciarRobot() {
            const { inicio: ini, dir } = laberinto;
            robot = { x: ini.x, y: ini.y, dir, giro: dir * 90 };
            tableroEl.querySelectorAll('.rastro, .choque').forEach(c => c.classList.remove('rastro', 'choque'));
            colocarRobot(true);
        }

        function agregar(bloque) {
            if (corriendo || !activo) return;
            if (programa.length >= MAXIMO) { decir('📏 ¡Programa muy largo! Usa menos bloques.', 'error'); return; }
            programa.push(bloque);
            sfx.tecla();
            pintarPrograma();
        }
        function expandir() {
            const pasos = [];
            for (let i = 0; i < programa.length; i++) {
                const b = programa[i];
                if (BLOQUES[b].veces) {
                    const siguiente = programa[i + 1];
                    if (siguiente && !BLOQUES[siguiente].veces) {
                        for (let k = 0; k < BLOQUES[b].veces; k++) pasos.push({ b: siguiente, i: i + 1, rep: i });
                        i += 1;
                    }
                    continue;
                }
                pasos.push({ b, i, rep: -1 });
            }
            return pasos;
        }

        async function ejecutar() {
            if (corriendo || !activo) return;
            if (!programa.length) { decir('👆 Primero arma tu programa con los bloques.', 'error'); return; }
            corriendo = true;
            zonaJuego.classList.add('corriendo');
            reiniciarRobot();
            await esperar(250);
            let resultado = 'corto';
            for (const paso of expandir()) {
                if (!activo) return;
                pintarPrograma(paso.i, paso.rep);
                const b = BLOQUES[paso.b];
                if (paso.b === 'girarIzq' || paso.b === 'girarDer') {
                    robot.dir = (robot.dir + (paso.b === 'girarIzq' ? 3 : 1)) % 4;
                    robot.giro += paso.b === 'girarIzq' ? -90 : 90;
                    colocarRobot();
                    sfx.tecla();
                    await esperar(300);
                    continue;
                }
                if (b.dir !== undefined) {
                    robot.giro += ((b.dir - robot.dir + 6) % 4) * 90 - 180;
                    robot.dir = b.dir;
                }
                const nx = robot.x + DX[robot.dir];
                const ny = robot.y + DY[robot.dir];
                const fuera = nx < 0 || ny < 0 || nx >= laberinto.tam || ny >= laberinto.tam;
                if (fuera || laberinto.rocas.has(ny * laberinto.tam + nx)) {
                    colocarRobot();
                    tableroEl.querySelector(`[data-celda="${nx},${ny}"]`)?.classList.add('choque');
                    robotEl.classList.remove('choca');
                    void robotEl.offsetWidth;
                    robotEl.classList.add('choca');
                    resultado = fuera ? 'fuera' : 'roca';
                    break;
                }
                tableroEl.querySelector(`[data-celda="${robot.x},${robot.y}"]`)?.classList.add('rastro');
                robot.x = nx;
                robot.y = ny;
                colocarRobot();
                sfx.tecla();
                await esperar(330);
                if (robot.x === laberinto.meta.x && robot.y === laberinto.meta.y) { resultado = 'meta'; break; }
            }
            if (!activo) return;
            pintarPrograma();
            if (resultado === 'meta') await exito(); else await fallo(resultado);
            zonaJuego.classList.remove('corriendo');
            corriendo = false;
        }

        async function exito() {
            const perfecto = programa.length <= laberinto.optimo;
            resueltos += 1;
            puntos += 150 + (perfecto ? 75 : 0);
            if (perfecto) perfectos += 1;
            tableroEl.querySelector('.jr-celda.meta')?.classList.add('cargada');
            robotEl.classList.add('feliz');
            sfx.estrella();
            decir(perfecto ? '✨ ¡Código perfecto! +225' : '🔋 ¡Batería cargada! +150', 'ok');
            pintarHud();
            await esperar(1300);
            siguienteNivel();
        }
        async function fallo(motivo) {
            errores += 1;
            intentos -= 1;
            sfx.error();
            pintarHud();
            const texto = { fuera: '🚧 ¡El robot se salió del tablero!', roca: '💥 ¡Chocaste con una roca!', corto: '🤔 El robot no llegó a la batería.' }[motivo];
            if (intentos > 0) {
                decir(`${texto} Revisa tu código y vuelve a intentarlo.`, 'error');
                await esperar(900);
                reiniciarRobot();
            } else {
                decir(`${texto} Se acabaron los intentos de este laberinto.`, 'error');
                await esperar(1600);
                siguienteNivel();
            }
        }
        function siguienteNivel() {
            if (!activo) return;
            nivel += 1;
            if (nivel >= cfg.niveles) { terminar(); return; }
            cargarNivel();
        }

        const TECLAS = giros
            ? { ArrowUp: 'avanzar', ArrowLeft: 'girarIzq', ArrowRight: 'girarDer' }
            : { ArrowUp: 'arriba', ArrowDown: 'abajo', ArrowLeft: 'izquierda', ArrowRight: 'derecha' };
        const alTeclear = e => {
            if (TECLAS[e.key]) { e.preventDefault(); agregar(TECLAS[e.key]); return; }
            if (e.key === 'Backspace') { e.preventDefault(); if (!corriendo) { programa.pop(); pintarPrograma(); } return; }
            if (e.key === 'Enter') { e.preventDefault(); ejecutar(); }
        };
        const alTocar = e => {
            const bloque = e.target.closest('[data-bloque]');
            if (bloque) { agregar(bloque.dataset.bloque); return; }
            const quitar = e.target.closest('[data-quitar]');
            if (quitar && !corriendo) { programa.splice(Number(quitar.dataset.quitar), 1); pintarPrograma(); return; }
            if (e.target.closest('[data-borrar]') && !corriendo) { programa.pop(); pintarPrograma(); return; }
            if (e.target.closest('[data-limpiar]') && !corriendo) { programa = []; pintarPrograma(); return; }
            if (e.target.closest('[data-ejecutar]')) ejecutar();
        };

        function terminar() {
            if (!activo) return;
            activo = false;
            document.removeEventListener('keydown', alTeclear);
            decir('🏁 ¡Misión de programación completada!', 'ok');
            ejecutarBtn.disabled = true;
            const duracion = Math.round((performance.now() - inicio) / 1000);
            setTimeout(() => fin({ resueltos, perfectos, errores, duracion }), 700);
        }

        return {
            iniciar() {
                activo = true;
                inicio = performance.now();
                document.addEventListener('keydown', alTeclear);
                zonaJuego.addEventListener('click', alTocar);
                cargarNivel();
            },
            detener() {
                activo = false;
                pausas.forEach(clearTimeout);
                pausas = [];
                document.removeEventListener('keydown', alTeclear);
            },
        };
    }

    // ---------- Piezas comunes de los juegos por rondas ----------
    function hudRondas(hud, { icono, ronda, total, aciertos, puntos, extra = '' }) {
        const estrellas = estrellasDe(Math.round(aciertos * 100 / total));
        hud.innerHTML = `
            <span class="chip-hud">${icono} ${Math.min(ronda + 1, total)}/${total}</span>
            <span class="chip-hud">✅ ${aciertos}</span>${extra}
            <span class="chip-hud estrellas" title="Estrellas">${[1, 2, 3].map(i => `<span class="${i <= estrellas ? 'on' : ''}">★</span>`).join('')}</span>
            <span class="chip-hud puntos">${miles(puntos)}</span>`;
    }
    function reanimar(el, clase, duracion = 0) {
        if (!el) return;
        el.classList.remove(clase);
        void el.offsetWidth;
        el.classList.add(clase);
        if (duracion) setTimeout(() => el.classList.remove(clase), duracion);
    }
    function mazoDe(opciones, total) {
        const mazo = [];
        while (mazo.length < total) mazo.push(...barajar(opciones.slice()));
        mazo.length = total;
        return mazo;
    }

    // =========================================================
    // ATAJOS NINJA
    // =========================================================
    const ES_MAC = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);

    function motorAtajos(zonaJuego, cfg, hud, fin) {
        const catalogo = cfg.catalogo;
        const mod = ES_MAC ? '⌘' : 'Ctrl';
        const tactil = window.matchMedia('(pointer: coarse)').matches;
        const mazo = mazoDe(cfg.atajos.flatMap(a => catalogo[a].situaciones.map(texto => ({ atajo: a, texto }))), cfg.rondas);
        zonaJuego.innerHTML = `
            <div class="ja-zona">
                <div class="ja-dojo">
                    <div class="ja-ninja" data-ninja>🥷</div>
                    <div class="ja-pergamino" data-pergamino>
                        <span class="contador" data-contador></span>
                        <span class="e" data-emoji></span>
                        <span class="texto" data-texto></span>
                        <span class="pista" data-pista></span>
                    </div>
                </div>
                <div class="ja-teclas" data-teclas aria-hidden="true"></div>
                <div class="ja-mensaje" data-mensaje aria-live="polite"></div>
                <div class="ja-opciones ${tactil ? '' : 'd-none'}" data-opciones></div>
                <button type="button" class="ja-sin-teclado ${tactil ? 'd-none' : ''}" data-sin-teclado>¿No tienes teclado? Toca aquí para elegir</button>
            </div>`;
        const $z = sel => zonaJuego.querySelector(sel);
        const pergamino = $z('[data-pergamino]');
        const ninja = $z('[data-ninja]');
        const mensaje = $z('[data-mensaje]');
        const teclasEl = $z('[data-teclas]');
        const opcionesEl = $z('[data-opciones]');

        let ronda = 0;
        let completadas = 0;
        let aciertos = 0;
        let perfectos = 0;
        let errores = 0;
        let erroresRonda = 0;
        let puntos = 0;
        let actual = null;
        let activo = false;
        let esperando = false;
        let inicio = 0;
        let ctrlAbajo = false;

        const combo = tecla => `<kbd>${mod}</kbd><span class="mas">+</span><kbd>${tecla}</kbd>`;
        const pintarHud = () => hudRondas(hud, { icono: '🥷', ronda, total: cfg.rondas, aciertos, puntos });
        function pintarTeclas(letra) {
            teclasEl.innerHTML = `<kbd class="${ctrlAbajo ? 'abajo' : ''}">${mod}</kbd><span class="mas">+</span><kbd class="${letra ? 'abajo' : ''}">${letra || '?'}</kbd>`;
        }
        function mostrarPista() {
            const a = catalogo[actual.atajo];
            $z('[data-pista]').innerHTML = `${combo(a.tecla)} <span>${esc(a.nombre)}</span>`;
        }
        function pintarOpciones() {
            const correcta = actual.atajo;
            const otras = barajar(Object.keys(catalogo).filter(k => k !== correcta)).slice(0, 2);
            opcionesEl.innerHTML = barajar([correcta, ...otras]).map(k => `
                <button type="button" class="ja-opcion" data-tecla="${catalogo[k].tecla}">${mod} + ${catalogo[k].tecla}</button>`).join('');
        }
        function nueva() {
            if (!activo) return;
            if (ronda >= mazo.length) { terminar(); return; }
            actual = mazo[ronda];
            erroresRonda = 0;
            esperando = false;
            const a = catalogo[actual.atajo];
            $z('[data-contador]').textContent = `Misión ${ronda + 1} de ${mazo.length}`;
            $z('[data-emoji]').textContent = a.emoji;
            $z('[data-texto]').textContent = actual.texto;
            $z('[data-pista]').innerHTML = '';
            if (cfg.modo === 'aprende') mostrarPista();
            pergamino.classList.remove('cortado', 'mal');
            reanimar(pergamino, 'entra');
            mensaje.className = 'ja-mensaje';
            mensaje.textContent = cfg.modo === 'aprende' ? 'Mantén presionada Ctrl y toca la letra' : '¿Qué atajo usarías?';
            pintarTeclas(null);
            pintarOpciones();
            pintarHud();
        }
        function responder(tecla) {
            if (!activo || esperando || !actual) return;
            const a = catalogo[actual.atajo];
            if (tecla === a.tecla) {
                esperando = true;
                completadas += 1;
                aciertos += 1;
                puntos += 100;
                if (!erroresRonda) { perfectos += 1; puntos += 50; }
                sfx.acierto();
                reanimar(ninja, 'ataca', 600);
                pergamino.classList.add('cortado');
                mensaje.className = 'ja-mensaje ok';
                mensaje.innerHTML = `${erroresRonda ? '¡Lo lograste!' : azar(['⚡ ¡Corte limpio!', '🥷 ¡Ninja experto!', '¡Perfecto!'])} ${combo(a.tecla)} es <b>${esc(a.nombre)}</b>`;
                ronda += 1;
                pintarHud();
                setTimeout(nueva, 900);
                return;
            }
            errores += 1;
            erroresRonda += 1;
            sfx.error();
            reanimar(pergamino, 'mal', 400);
            const otro = Object.values(catalogo).find(x => x.tecla === tecla);
            if (erroresRonda >= 3) {
                esperando = true;
                completadas += 1;
                ronda += 1;
                mostrarPista();
                mensaje.className = 'ja-mensaje error';
                mensaje.innerHTML = `Era ${combo(a.tecla)}: <b>${esc(a.nombre)}</b>. ¡La próxima la sacas!`;
                pintarHud();
                setTimeout(nueva, 1800);
                return;
            }
            mostrarPista();
            mensaje.className = 'ja-mensaje error';
            mensaje.innerHTML = otro ? `${combo(tecla)} es <b>${esc(otro.nombre)}</b>. Intenta otra vez.` : 'Esa combinación no es. Mira la pista.';
        }

        const alBajar = e => {
            if (e.key === 'Control' || e.key === 'Meta') { ctrlAbajo = true; pintarTeclas(null); return; }
            const letra = (e.key || '').toUpperCase();
            if (letra.length !== 1 || !/[A-Z]/.test(letra)) return;
            const conCtrl = ES_MAC ? e.metaKey || e.ctrlKey : e.ctrlKey;
            e.preventDefault();
            e.stopPropagation();
            if (e.repeat || !activo || esperando) return;
            pintarTeclas(letra);
            if (!conCtrl) {
                mensaje.className = 'ja-mensaje error';
                mensaje.innerHTML = `¡Te faltó mantener presionada <kbd>${mod}</kbd>!`;
                reanimar(teclasEl, 'mal', 400);
                return;
            }
            responder(letra);
        };
        const alSubir = e => { if (e.key === 'Control' || e.key === 'Meta') { ctrlAbajo = false; pintarTeclas(null); } };
        const alTocar = e => {
            const opcion = e.target.closest('[data-tecla]');
            if (opcion) { responder(opcion.dataset.tecla); return; }
            if (e.target.closest('[data-sin-teclado]')) {
                opcionesEl.classList.remove('d-none');
                e.target.closest('[data-sin-teclado]').classList.add('d-none');
            }
        };

        function terminar() {
            if (!activo) return;
            activo = false;
            document.removeEventListener('keydown', alBajar, true);
            document.removeEventListener('keyup', alSubir, true);
            $z('[data-texto]').textContent = '🏁 ¡Entrenamiento terminado!';
            $z('[data-pista]').innerHTML = '';
            setTimeout(() => fin({ completadas, aciertos, perfectos, errores, duracion: Math.round((performance.now() - inicio) / 1000) }), 600);
        }

        return {
            iniciar() {
                activo = true;
                inicio = performance.now();
                // En fase de captura, para que el navegador no abra «Guardar», «Imprimir» ni «Buscar»
                document.addEventListener('keydown', alBajar, true);
                document.addEventListener('keyup', alSubir, true);
                zonaJuego.addEventListener('click', alTocar);
                nueva();
            },
            detener() {
                activo = false;
                document.removeEventListener('keydown', alBajar, true);
                document.removeEventListener('keyup', alSubir, true);
            },
        };
    }

    // =========================================================
    // MENSAJE SECRETO
    // =========================================================
    const ALFABETO = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ';
    const MORSE = {
        A: '·−', B: '−···', C: '−·−·', D: '−··', E: '·', F: '··−·', G: '−−·', H: '····', I: '··', J: '·−−−', K: '−·−', L: '·−··',
        M: '−−', N: '−·', Ñ: '−−·−−', O: '−−−', P: '·−−·', Q: '−−·−', R: '·−·', S: '···', T: '−', U: '··−', V: '···−', W: '·−−',
        X: '−··−', Y: '−·−−', Z: '−−··',
    };
    const SIMBOLOS = ['🍎', '🐝', '🌙', '🐬', '⭐', '🔥', '🍇', '🏠', '🍦', '🧃', '🔑', '🦁', '🍄', '🎵', '🐧', '🐙', '🍕', '👑', '🌈',
        '☀️', '🌳', '🦄', '🌋', '🐳', '🎸', '🍋', '⚡'];
    function normalizarSecreto(palabra) {
        return String(palabra).toUpperCase().replace(/Ñ/g, '\u0000').normalize('NFD').replace(/[̀-ͯ]/g, '')
            .replace(/\u0000/g, 'Ñ').split('').filter(c => ALFABETO.includes(c)).join('');
    }
    function codigoDe(letra, cfg) {
        const i = ALFABETO.indexOf(letra);
        if (cfg.cifrado === 'morse') return MORSE[letra];
        if (cfg.cifrado === 'binario') return (i + 1).toString(2).padStart(5, '0');
        if (cfg.cifrado === 'cesar') return ALFABETO[(i + cfg.desplazamiento) % ALFABETO.length];
        return SIMBOLOS[i];
    }

    function motorMensaje(zonaJuego, cfg, hud, fin) {
        const mazo = mazoDe(cfg.palabras, cfg.rondas);
        const explica = {
            simbolos: '🔣 Cada dibujo es una letra. Búscalo en la tabla.',
            cesar: `🏛️ Cada letra se recorrió ${cfg.desplazamiento} lugar${cfg.desplazamiento === 1 ? '' : 'es'} en el abecedario. La tabla te dice cuál era.`,
            morse: '📡 Puntos y rayas: busca cada código en la tabla.',
            binario: '💻 Cada letra es su número en binario (A = 1, B = 2…). Búscalo en la tabla.',
        }[cfg.cifrado];
        zonaJuego.innerHTML = `
            <div class="js-zona cifrado-${cfg.cifrado}">
                <div class="js-cabeza"><span class="js-sobre">✉️</span><div><div class="t" data-contador></div><div class="d">${esc(explica)}</div></div></div>
                <div class="js-palabra" data-palabra></div>
                <div class="js-mensaje" data-mensaje aria-live="polite"></div>
                <div class="js-acciones">
                    <button type="button" class="js-pista" data-pista><i class="bi bi-lightbulb"></i> Pista</button>
                    <button type="button" class="js-revisar" data-revisar><i class="bi bi-unlock"></i> Revisar</button>
                </div>
                <div class="js-tabla">
                    <div class="t">🗝️ Tabla de pistas</div>
                    <div class="js-claves">${[...ALFABETO].map(l => `<span class="clave"><b>${esc(codigoDe(l, cfg))}</b><i>${l}</i></span>`).join('')}</div>
                </div>
            </div>`;
        const $z = sel => zonaJuego.querySelector(sel);
        const palabraEl = $z('[data-palabra]');
        const mensaje = $z('[data-mensaje]');
        const pistaBtn = $z('[data-pista]');

        let ronda = 0;
        let completadas = 0;
        let aciertos = 0;
        let perfectos = 0;
        let errores = 0;
        let puntos = 0;
        let actual = '';
        let intentos = cfg.intentos;
        let limpia = true;
        let activo = false;
        let esperando = false;
        let inicio = 0;

        const casillas = () => [...palabraEl.querySelectorAll('[data-letra]')];
        const pintarHud = () => hudRondas(hud, { icono: '✉️', ronda, total: cfg.rondas, aciertos, puntos,
            extra: `<span class="chip-hud" title="Intentos">${'❤️'.repeat(intentos)}${'🖤'.repeat(cfg.intentos - intentos)}</span>` });

        function nueva() {
            if (!activo) return;
            if (ronda >= mazo.length) { terminar(); return; }
            actual = mazo[ronda];
            intentos = cfg.intentos;
            limpia = true;
            esperando = false;
            $z('[data-contador]').textContent = `Mensaje secreto ${ronda + 1} de ${mazo.length}`;
            palabraEl.innerHTML = [...actual].map((letra, i) => `
                <div class="js-par">
                    <span class="codigo">${esc(codigoDe(letra, cfg))}</span>
                    <input type="text" class="js-letra" data-letra="${i}" autocomplete="off" autocapitalize="characters" spellcheck="false" aria-label="Letra ${i + 1}">
                </div>`).join('');
            reanimar(palabraEl, 'entra');
            pistaBtn.disabled = false;
            mensaje.className = 'js-mensaje';
            mensaje.textContent = 'Escribe una letra en cada casilla y presiona «Revisar».';
            pintarHud();
            setTimeout(() => casillas()[0]?.focus(), 80);
        }
        function revisar() {
            if (!activo || esperando) return;
            const lista = casillas();
            if (lista.some(c => !c.value)) {
                mensaje.className = 'js-mensaje error';
                mensaje.textContent = '✏️ Te faltan casillas por llenar.';
                lista.find(c => !c.value)?.focus();
                return;
            }
            let todas = true;
            lista.forEach((c, i) => {
                const bien = normalizarSecreto(c.value) === actual[i];
                c.classList.toggle('bien', bien);
                c.classList.toggle('mal', !bien);
                c.readOnly = bien;
                if (!bien) todas = false;
            });
            if (todas) {
                esperando = true;
                completadas += 1;
                aciertos += 1;
                puntos += 100;
                if (limpia) { perfectos += 1; puntos += 50; }
                sfx.estrella();
                palabraEl.classList.add('descifrada');
                mensaje.className = 'js-mensaje ok';
                mensaje.innerHTML = `🔓 ¡Mensaje descifrado! <b>${esc(actual)}</b>${limpia ? ' · ✨ sin pistas ni errores' : ''}`;
                ronda += 1;
                pintarHud();
                setTimeout(() => { palabraEl.classList.remove('descifrada'); nueva(); }, 1300);
                return;
            }
            errores += 1;
            intentos -= 1;
            limpia = false;
            sfx.error();
            reanimar(palabraEl, 'temblor', 400);
            pintarHud();
            if (intentos <= 0) {
                esperando = true;
                completadas += 1;
                ronda += 1;
                lista.forEach((c, i) => { c.value = actual[i]; c.readOnly = true; });
                mensaje.className = 'js-mensaje error';
                mensaje.innerHTML = `Era <b>${esc(actual)}</b>. ¡El siguiente lo descifras!`;
                pintarHud();
                setTimeout(nueva, 2000);
                return;
            }
            mensaje.className = 'js-mensaje error';
            mensaje.textContent = 'Las casillas rojas no coinciden. Revisa la tabla y corrígelas.';
            lista.find(c => c.classList.contains('mal'))?.select();
        }
        function pista() {
            if (!activo || esperando || pistaBtn.disabled) return;
            const pendientes = casillas().filter(c => !c.readOnly);
            if (!pendientes.length) return;
            const c = azar(pendientes);
            c.value = actual[Number(c.dataset.letra)];
            c.readOnly = true;
            c.classList.remove('mal');
            c.classList.add('bien', 'pista');
            limpia = false;
            pistaBtn.disabled = true;
            mensaje.className = 'js-mensaje';
            mensaje.textContent = '💡 Te regalamos una letra.';
        }

        // Si llegan varias letras juntas (pegar, autocompletar del celular) se reparten en las casillas siguientes
        const alEscribir = e => {
            const c = e.target.closest('[data-letra]');
            if (!c) return;
            const letras = [...normalizarSecreto(c.value)];
            c.classList.remove('mal');
            if (!letras.length) { c.value = ''; return; }
            const lista = casillas();
            let indice = Number(c.dataset.letra);
            c.value = letras.shift();
            letras.forEach(letra => {
                const sig = lista.slice(indice + 1).find(x => !x.readOnly);
                if (!sig) return;
                sig.value = letra;
                sig.classList.remove('mal');
                indice = Number(sig.dataset.letra);
            });
            lista.slice(indice + 1).find(x => !x.readOnly)?.focus();
        };
        const alTeclear = e => {
            const c = e.target.closest?.('[data-letra]');
            if (e.key === 'Enter') { e.preventDefault(); revisar(); return; }
            if (c && e.key === 'Backspace' && !c.value) {
                const previas = casillas().slice(0, Number(c.dataset.letra)).reverse();
                const anterior = previas.find(x => !x.readOnly);
                if (anterior) { e.preventDefault(); anterior.value = ''; anterior.focus(); }
            }
        };
        const alTocar = e => {
            if (e.target.closest('[data-revisar]')) revisar();
            else if (e.target.closest('[data-pista]')) pista();
        };

        function terminar() {
            if (!activo) return;
            activo = false;
            palabraEl.innerHTML = '<div class="js-fin">🏁 ¡Todos los mensajes revisados!</div>';
            setTimeout(() => fin({ completadas, aciertos, perfectos, errores, duracion: Math.round((performance.now() - inicio) / 1000) }), 600);
        }

        return {
            iniciar() {
                activo = true;
                inicio = performance.now();
                zonaJuego.addEventListener('input', alEscribir);
                zonaJuego.addEventListener('keydown', alTeclear);
                // Al entrar a una casilla se selecciona su letra: escribir encima la reemplaza
                zonaJuego.addEventListener('focusin', e => { if (e.target.matches?.('[data-letra]') && !e.target.readOnly) e.target.select(); });
                zonaJuego.addEventListener('click', alTocar);
                nueva();
            },
            detener() { activo = false; },
        };
    }

    // =========================================================
    // EXPLORADOR DE RUTAS
    // =========================================================
    const ICONOS_ARCHIVO = { docx: '📝', pptx: '📊', xlsx: '📈', pdf: '📕', jpg: '🖼️', png: '🖼️', mp3: '🎵', mp4: '🎬', ino: '🤖', txt: '📄', exe: '⚙️', sb3: '🐱' };
    const ICONOS_LUGAR = { Escritorio: '🖥️', Documentos: '📄', Descargas: '⬇️', Imágenes: '🖼️', Música: '🎵', Videos: '🎬' };
    const nuevaCarpeta = (nombre, hijos) => ({ nombre, hijos });
    function arbolDeArchivos(dificultad) {
        const dificil = dificultad === 'dificil';
        const escuela = [
            nuevaCarpeta('Ciencias', ['tarea_ciencias.docx', 'experimento.pptx', ...(dificil ? [nuevaCarpeta('Experimentos', ['volcan.docx', 'plantas.pptx'])] : [])]),
            nuevaCarpeta('Matemáticas', ['tablas.xlsx', 'problemas.docx']),
            nuevaCarpeta('Español', ['cuento.docx', 'poema.docx']),
            ...(dificil ? [nuevaCarpeta('Historia', ['independencia.pptx', 'linea_tiempo.pdf'])] : []),
        ];
        const raiz = [
            nuevaCarpeta('Documentos', [
                nuevaCarpeta('Escuela', escuela),
                nuevaCarpeta('Proyectos', [nuevaCarpeta('Robot', ['codigo_robot.ino', 'diagrama.png', ...(dificil ? [nuevaCarpeta('Versiones', ['codigo_v2.ino', 'codigo_v3.ino'])] : [])]), 'ideas.txt']),
                'horario.pdf',
                ...(dificil ? [nuevaCarpeta('Nueva carpeta', []), nuevaCarpeta('Copias', ['tarea_vieja.docx'])] : []),
            ]),
            nuevaCarpeta('Imágenes', [nuevaCarpeta('Vacaciones', ['playa.jpg', 'pastel.jpg']), nuevaCarpeta('Dibujos', ['mi_robot.png', 'dragon.png']), 'foto_grupo.jpg']),
            nuevaCarpeta('Música', [nuevaCarpeta('Favoritas', ['cancion_feliz.mp3', 'himno.mp3']), 'tono.mp3']),
            nuevaCarpeta('Descargas', ['instalador.exe', 'libro.pdf', 'fondo.jpg', ...(dificultad !== 'facil' ? ['juego_scratch.sb3'] : [])]),
        ];
        if (dificultad !== 'facil') {
            raiz.push(nuevaCarpeta('Videos', [nuevaCarpeta('Clase', ['tutorial_scratch.mp4', 'robot_bailando.mp4']), 'cumpleaños.mp4']));
            raiz.push(nuevaCarpeta('Escritorio', [nuevaCarpeta('Tareas', ['pendientes.txt']), 'lista_compras.txt']));
        }
        return nuevaCarpeta('Este equipo', raiz);
    }
    function archivosDe(carpeta, ruta = []) {
        return carpeta.hijos.flatMap(h => (typeof h === 'string' ? [{ nombre: h, ruta }] : archivosDe(h, [...ruta, h.nombre])));
    }

    function motorRutas(zonaJuego, cfg, hud, fin) {
        const arbol = arbolDeArchivos(cfg.dificultad);
        const rango = { facil: [1, 2], media: [2, 3], dificil: [3, 4] }[cfg.dificultad];
        let candidatos = archivosDe(arbol).filter(a => a.ruta.length >= rango[0] && a.ruta.length <= rango[1]);
        if (!candidatos.length) candidatos = archivosDe(arbol);
        const mazo = mazoDe(candidatos, cfg.rondas);
        zonaJuego.innerHTML = `
            <div class="jx-zona">
                <div class="jx-mision" data-mision></div>
                <div class="jx-ventana">
                    <div class="jx-titulo"><span>📁 Explorador de archivos</span><span class="puntos-ventana"><i></i><i></i><i></i></span></div>
                    <div class="jx-barra">
                        <button type="button" data-atras title="Atrás"><i class="bi bi-arrow-left"></i></button>
                        <button type="button" data-subir title="Subir un nivel"><i class="bi bi-arrow-up"></i></button>
                        <div class="jx-ruta" data-ruta></div>
                    </div>
                    <div class="jx-cuerpo">
                        <nav class="jx-lateral" data-lateral></nav>
                        <div class="jx-contenido" data-contenido></div>
                    </div>
                </div>
                <div class="jx-mensaje" data-mensaje aria-live="polite"></div>
            </div>`;
        const $z = sel => zonaJuego.querySelector(sel);
        const mensaje = $z('[data-mensaje]');

        let ronda = 0;
        let completadas = 0;
        let aciertos = 0;
        let perfectos = 0;
        let errores = 0;
        let puntos = 0;
        let actual = null;
        let ruta = [];
        let historial = [];
        let clics = 0;
        let fallosArchivo = 0;
        let activo = false;
        let esperando = false;
        let inicio = 0;

        const optimo = () => actual.ruta.length + 1;
        const carpetaEn = r => r.reduce((carpeta, nombre) => carpeta.hijos.find(h => typeof h !== 'string' && h.nombre === nombre), arbol);
        const icono = nombre => ICONOS_ARCHIVO[nombre.split('.').pop()] || '📄';
        const pintarHud = () => hudRondas(hud, { icono: '📁', ronda, total: cfg.rondas, aciertos, puntos,
            extra: `<span class="chip-hud" title="Clics">👆 ${clics}</span>` });

        function pintar() {
            const carpeta = carpetaEn(ruta);
            $z('[data-ruta]').innerHTML = [`<button type="button" data-ir="0">💻 Este equipo</button>`,
                ...ruta.map((n, i) => `<i class="bi bi-chevron-right"></i><button type="button" data-ir="${i + 1}">${esc(n)}</button>`)].join('');
            $z('[data-lateral]').innerHTML = arbol.hijos.map(h => `
                <button type="button" class="${ruta[0] === h.nombre ? 'activo' : ''}" data-lugar="${esc(h.nombre)}">${ICONOS_LUGAR[h.nombre] || '📁'} ${esc(h.nombre)}</button>`).join('');
            const hijos = carpeta.hijos.slice().sort((a, b) => (typeof a === 'string') - (typeof b === 'string'));
            $z('[data-contenido]').innerHTML = hijos.length ? hijos.map(h => (typeof h === 'string'
                ? `<button type="button" class="jx-item archivo" data-archivo="${esc(h)}"><span class="i">${icono(h)}</span><span class="n">${esc(h)}</span></button>`
                : `<button type="button" class="jx-item" data-carpeta="${esc(h.nombre)}"><span class="i">📁</span><span class="n">${esc(h.nombre)}</span></button>`)).join('')
                : '<div class="jx-vacia">Esta carpeta está vacía</div>';
            $z('[data-atras]').disabled = !historial.length;
            $z('[data-subir]').disabled = !ruta.length;
            pintarHud();
        }
        function irA(nuevaRuta) {
            historial.push(ruta);
            ruta = nuevaRuta;
            contarClic();
            pintar();
        }
        function contarClic() {
            clics += 1;
            if (clics >= optimo() + 10) rendirse();
        }
        function nueva() {
            if (!activo) return;
            if (ronda >= mazo.length) { terminar(); return; }
            actual = mazo[ronda];
            ruta = [];
            historial = [];
            clics = 0;
            fallosArchivo = 0;
            esperando = false;
            $z('[data-mision]').innerHTML = `
                <span class="contador">Archivo ${ronda + 1} de ${mazo.length}</span>
                <span class="objetivo">🎯 Encuentra <b>${icono(actual.nombre)} ${esc(actual.nombre)}</b></span>
                ${cfg.modo === 'ruta' ? `<span class="pista">🧭 ${['Este equipo', ...actual.ruta].map(esc).join(' › ')}</span>` : '<span class="pista">🔎 ¿En qué carpeta lo guardarías?</span>'}
                <span class="minimo">Mínimo: ${optimo()} clics</span>`;
            mensaje.className = 'jx-mensaje';
            mensaje.textContent = '';
            pintar();
        }
        function encontrado() {
            esperando = true;
            completadas += 1;
            const extra = clics - optimo();
            const perfecto = extra <= 0 && !fallosArchivo;
            if (extra <= 3) {
                aciertos += 1;
                puntos += 100 + (perfecto ? 50 : 0);
                if (perfecto) perfectos += 1;
            }
            errores += Math.max(0, extra);
            sfx.acierto();
            mensaje.className = `jx-mensaje ${extra <= 3 ? 'ok' : 'error'}`;
            mensaje.innerHTML = perfecto ? `🎯 ¡Directo al archivo! ${clics} clics, el mínimo.`
                : extra <= 3 ? `📁 ¡Lo encontraste en ${clics} clics! El mínimo era ${optimo()}.`
                    : `Lo encontraste, pero con ${clics} clics (el mínimo era ${optimo()}). ¡Intenta ir más directo!`;
            mensaje.innerHTML += `<div class="ruta-final">📍 ${['Este equipo', ...actual.ruta, actual.nombre].map(esc).join(' › ')}</div>`;
            ronda += 1;
            pintarHud();
            setTimeout(nueva, 2000);
        }
        function rendirse() {
            if (esperando) return;
            esperando = true;
            completadas += 1;
            errores += clics;
            sfx.error();
            mensaje.className = 'jx-mensaje error';
            mensaje.innerHTML = `Demasiados clics. Estaba en: <b>${['Este equipo', ...actual.ruta].map(esc).join(' › ')}</b>`;
            ronda += 1;
            pintarHud();
            setTimeout(nueva, 2400);
        }

        const alTocar = e => {
            if (!activo || esperando) return;
            const carpeta = e.target.closest('[data-carpeta]');
            const archivo = e.target.closest('[data-archivo]');
            const lugar = e.target.closest('[data-lugar]');
            const miga = e.target.closest('[data-ir]');
            if (carpeta) { sfx.tecla(); irA([...ruta, carpeta.dataset.carpeta]); return; }
            if (lugar) { sfx.tecla(); irA([lugar.dataset.lugar]); return; }
            if (miga) { irA(ruta.slice(0, Number(miga.dataset.ir))); return; }
            if (e.target.closest('[data-subir]') && ruta.length) { irA(ruta.slice(0, -1)); return; }
            if (e.target.closest('[data-atras]') && historial.length) { ruta = historial.pop(); contarClic(); pintar(); return; }
            if (archivo) {
                contarClic();
                if (esperando) return;
                if (archivo.dataset.archivo === actual.nombre && ruta.join('/') === actual.ruta.join('/')) { encontrado(); return; }
                fallosArchivo += 1;
                sfx.error();
                reanimar(archivo, 'mal', 400);
                mensaje.className = 'jx-mensaje error';
                mensaje.innerHTML = `Ese es <b>${esc(archivo.dataset.archivo)}</b>, no el que buscas.`;
                pintarHud();
            }
        };

        function terminar() {
            if (!activo) return;
            activo = false;
            $z('[data-mision]').innerHTML = '<span class="objetivo">🏁 ¡Exploración terminada!</span>';
            setTimeout(() => fin({ completadas, aciertos, perfectos, errores, duracion: Math.round((performance.now() - inicio) / 1000) }), 600);
        }

        return {
            iniciar() {
                activo = true;
                inicio = performance.now();
                zonaJuego.addEventListener('click', alTocar);
                nueva();
            },
            detener() { activo = false; },
        };
    }

    // =========================================================
    // COPIA EL FORMATO
    // =========================================================
    const COLORES_TEXTO = { '': ['Negro', '#1e293b'], rojo: ['Rojo', '#dc2626'], azul: ['Azul', '#2563eb'], verde: ['Verde', '#16a34a'] };
    const formatoVacio = () => ({ b: false, i: false, u: false, color: '', grande: false });
    const NOMBRE_PROP = { b: 'en negrita', i: 'en cursiva', u: 'subrayada', grande: 'más grande' };

    function formatoObjetivo(palabras, dificultad) {
        const formatos = palabras.map(formatoVacio);
        let alineacion = 'izquierda';
        const tramo = () => {
            const largo = 1 + entero(Math.min(2, palabras.length - 1));
            const desde = entero(palabras.length - largo + 1);
            return Array.from({ length: largo }, (_, k) => desde + k);
        };
        if (dificultad === 'facil') {
            const prop = azar(['b', 'i', 'u']);
            formatos.forEach(f => { f[prop] = true; });
        } else if (dificultad === 'media') {
            const props = barajar(['b', 'i', 'u', 'color']).slice(0, 1 + entero(2));
            tramo().forEach(k => props.forEach(p => { formatos[k][p] = p === 'color' ? azar(['rojo', 'azul', 'verde']) : true; }));
            if (Math.random() < 0.5) alineacion = 'centro';
        } else {
            const primero = tramo();
            barajar(['b', 'i', 'u']).slice(0, 1 + entero(2)).forEach(p => primero.forEach(k => { formatos[k][p] = true; }));
            const libres = palabras.map((_, k) => k).filter(k => !primero.includes(k));
            const segundo = libres.length ? [azar(libres)] : primero;
            const color = azar(['rojo', 'azul', 'verde']);
            segundo.forEach(k => { formatos[k].color = color; if (Math.random() < 0.6) formatos[k].grande = true; });
            alineacion = azar(['izquierda', 'centro', 'derecha']);
        }
        return { formatos, alineacion };
    }

    function motorFormato(zonaJuego, cfg, hud, fin) {
        const mazo = mazoDe(cfg.frases, cfg.rondas);
        zonaJuego.innerHTML = `
            <div class="jf-zona">
                <div class="jf-hoja modelo"><span class="etq">📄 Modelo</span><p data-modelo></p></div>
                <div class="jf-barra" role="toolbar" aria-label="Formato">
                    <div class="grupo">
                        <button type="button" data-prop="b" title="Negrita (Ctrl+B)"><b>N</b></button>
                        <button type="button" data-prop="i" title="Cursiva (Ctrl+I)"><i>K</i></button>
                        <button type="button" data-prop="u" title="Subrayado (Ctrl+U)"><u>S</u></button>
                    </div>
                    <div class="grupo colores">
                        ${Object.entries(COLORES_TEXTO).map(([k, [n, hex]]) => `<button type="button" data-color="${k}" title="${n}" style="--cc:${hex}"><span></span></button>`).join('')}
                    </div>
                    <div class="grupo">
                        <button type="button" data-tam title="Letra grande">A<sup>+</sup></button>
                    </div>
                    <div class="grupo">
                        <button type="button" data-alinear="izquierda" title="Alinear a la izquierda"><i class="bi bi-text-left"></i></button>
                        <button type="button" data-alinear="centro" title="Centrar"><i class="bi bi-text-center"></i></button>
                        <button type="button" data-alinear="derecha" title="Alinear a la derecha"><i class="bi bi-text-right"></i></button>
                    </div>
                    <div class="grupo"><button type="button" data-todo title="Seleccionar todo (Ctrl+A)">Todo</button></div>
                </div>
                <div class="jf-hoja tuya"><span class="etq">✏️ Tu texto <small>· toca las palabras para seleccionarlas</small></span><p data-tuyo></p></div>
                <div class="jf-pie">
                    <span class="jf-seleccion" data-seleccion></span>
                    <button type="button" class="jf-comprobar" data-comprobar><i class="bi bi-check2-circle"></i> Comprobar</button>
                </div>
                <div class="jf-mensaje" data-mensaje aria-live="polite"></div>
            </div>`;
        const $z = sel => zonaJuego.querySelector(sel);
        const modeloEl = $z('[data-modelo]');
        const tuyoEl = $z('[data-tuyo]');
        const mensaje = $z('[data-mensaje]');

        let ronda = 0;
        let completadas = 0;
        let aciertos = 0;
        let perfectos = 0;
        let errores = 0;
        let puntos = 0;
        let palabras = [];
        let objetivo = null;
        let mio = null;
        let seleccion = new Set();
        let intentos = cfg.intentos;
        let activo = false;
        let esperando = false;
        let inicio = 0;

        const pintarHud = () => hudRondas(hud, { icono: '🎨', ronda, total: cfg.rondas, aciertos, puntos,
            extra: `<span class="chip-hud" title="Intentos">${'❤️'.repeat(intentos)}${'🖤'.repeat(cfg.intentos - intentos)}</span>` });
        const estilo = f => [f.b ? 'font-weight:900' : '', f.i ? 'font-style:italic' : '', f.u ? 'text-decoration:underline' : '',
            f.color ? `color:${COLORES_TEXTO[f.color][1]}` : '', f.grande ? 'font-size:1.45em' : ''].filter(Boolean).join(';');
        function pintarTexto(el, estado, interactivo) {
            el.style.textAlign = { izquierda: 'left', centro: 'center', derecha: 'right' }[estado.alineacion];
            el.innerHTML = palabras.map((p, k) => (interactivo
                ? `<span class="palabra ${seleccion.has(k) ? 'sel' : ''}" data-k="${k}" style="${estilo(estado.formatos[k])}">${esc(p)}</span>`
                : `<span style="${estilo(estado.formatos[k])}">${esc(p)}</span>`)).join(' ');
        }
        function pintarBarra() {
            const sel = [...seleccion];
            const todas = prop => sel.length > 0 && sel.every(k => mio.formatos[k][prop]);
            ['b', 'i', 'u'].forEach(p => $z(`[data-prop="${p}"]`).classList.toggle('activo', todas(p)));
            $z('[data-tam]').classList.toggle('activo', todas('grande'));
            zonaJuego.querySelectorAll('[data-color]').forEach(b => b.classList.toggle('activo', sel.length > 0 && sel.every(k => mio.formatos[k].color === b.dataset.color)));
            zonaJuego.querySelectorAll('[data-alinear]').forEach(b => b.classList.toggle('activo', mio.alineacion === b.dataset.alinear));
            $z('[data-seleccion]').textContent = sel.length ? `${sel.length} palabra${sel.length === 1 ? '' : 's'} seleccionada${sel.length === 1 ? '' : 's'}` : 'Selecciona palabras para darles formato';
        }
        function pintar() {
            pintarTexto(tuyoEl, mio, true);
            pintarBarra();
            pintarHud();
        }
        function nueva() {
            if (!activo) return;
            if (ronda >= mazo.length) { terminar(); return; }
            palabras = mazo[ronda].split(' ');
            do { objetivo = formatoObjetivo(palabras, cfg.dificultad); }
            while (objetivo.alineacion === 'izquierda' && objetivo.formatos.every(f => !f.b && !f.i && !f.u && !f.color && !f.grande));
            mio = { formatos: palabras.map(formatoVacio), alineacion: 'izquierda' };
            seleccion = new Set();
            intentos = cfg.intentos;
            esperando = false;
            pintarTexto(modeloEl, objetivo, false);
            reanimar(modeloEl.parentElement, 'entra');
            mensaje.className = 'jf-mensaje';
            mensaje.textContent = `Texto ${ronda + 1} de ${mazo.length}: haz que tu texto quede igual al modelo.`;
            pintar();
        }
        function aplicar(prop, valor) {
            if (!seleccion.size) {
                mensaje.className = 'jf-mensaje error';
                mensaje.textContent = '👆 Primero selecciona las palabras (o usa «Todo»).';
                reanimar(tuyoEl.parentElement, 'temblor', 400);
                return;
            }
            const sel = [...seleccion];
            if (prop === 'color') sel.forEach(k => { mio.formatos[k].color = valor; });
            else {
                const poner = !sel.every(k => mio.formatos[k][prop]);
                sel.forEach(k => { mio.formatos[k][prop] = poner; });
            }
            sfx.tecla();
            pintar();
        }
        function diferencia() {
            for (let k = 0; k < palabras.length; k++) {
                const a = mio.formatos[k];
                const o = objetivo.formatos[k];
                for (const p of ['b', 'i', 'u', 'grande']) {
                    if (a[p] !== o[p]) return `«${palabras[k]}» ${o[p] ? 'debe ir' : 'no va'} ${NOMBRE_PROP[p]}.`;
                }
                if (a.color !== o.color) return `«${palabras[k]}» va en color ${COLORES_TEXTO[o.color][0].toLowerCase()}.`;
            }
            if (mio.alineacion !== objetivo.alineacion) {
                return `El párrafo va ${{ izquierda: 'a la izquierda', centro: 'centrado', derecha: 'a la derecha' }[objetivo.alineacion]}.`;
            }
            return null;
        }
        function comprobar() {
            if (!activo || esperando) return;
            const falta = diferencia();
            if (!falta) {
                esperando = true;
                completadas += 1;
                aciertos += 1;
                puntos += 100;
                const perfecto = intentos === cfg.intentos;
                if (perfecto) { perfectos += 1; puntos += 50; }
                seleccion = new Set();
                pintar();
                sfx.estrella();
                tuyoEl.parentElement.classList.add('igual');
                mensaje.className = 'jf-mensaje ok';
                mensaje.textContent = perfecto ? '✨ ¡Idéntico al modelo a la primera!' : '🎨 ¡Quedó igual al modelo!';
                ronda += 1;
                pintarHud();
                setTimeout(() => { tuyoEl.parentElement.classList.remove('igual'); nueva(); }, 1300);
                return;
            }
            errores += 1;
            intentos -= 1;
            sfx.error();
            reanimar(tuyoEl.parentElement, 'temblor', 400);
            if (intentos <= 0) {
                esperando = true;
                completadas += 1;
                ronda += 1;
                mio = JSON.parse(JSON.stringify(objetivo));
                seleccion = new Set();
                pintar();
                mensaje.className = 'jf-mensaje error';
                mensaje.textContent = 'Así quedaba. ¡En el siguiente lo logras!';
                setTimeout(nueva, 2200);
                return;
            }
            mensaje.className = 'jf-mensaje error';
            mensaje.textContent = `Casi. ${falta}`;
            pintarHud();
        }

        const alTocar = e => {
            if (!activo || esperando) return;
            const palabra = e.target.closest('[data-k]');
            if (palabra) {
                const k = Number(palabra.dataset.k);
                if (seleccion.has(k)) seleccion.delete(k); else seleccion.add(k);
                pintar();
                return;
            }
            const prop = e.target.closest('[data-prop]');
            if (prop) { aplicar(prop.dataset.prop); return; }
            const color = e.target.closest('[data-color]');
            if (color) { aplicar('color', color.dataset.color); return; }
            if (e.target.closest('[data-tam]')) { aplicar('grande'); return; }
            const alinear = e.target.closest('[data-alinear]');
            if (alinear) { mio.alineacion = alinear.dataset.alinear; sfx.tecla(); pintar(); return; }
            if (e.target.closest('[data-todo]')) { seleccion = new Set(palabras.map((_, k) => k)); pintar(); return; }
            if (e.target.closest('[data-comprobar]')) comprobar();
        };
        const alTeclear = e => {
            if (!activo || esperando) return;
            const ctrl = e.ctrlKey || e.metaKey;
            const letra = (e.key || '').toUpperCase();
            if (ctrl && { B: 'b', I: 'i', U: 'u' }[letra]) { e.preventDefault(); e.stopPropagation(); aplicar({ B: 'b', I: 'i', U: 'u' }[letra]); }
            else if (ctrl && letra === 'A') { e.preventDefault(); e.stopPropagation(); seleccion = new Set(palabras.map((_, k) => k)); pintar(); }
            else if (e.key === 'Enter') { e.preventDefault(); comprobar(); }
        };

        function terminar() {
            if (!activo) return;
            activo = false;
            document.removeEventListener('keydown', alTeclear, true);
            mensaje.className = 'jf-mensaje ok';
            mensaje.textContent = '🏁 ¡Documento terminado!';
            setTimeout(() => fin({ completadas, aciertos, perfectos, errores, duracion: Math.round((performance.now() - inicio) / 1000) }), 600);
        }

        return {
            iniciar() {
                activo = true;
                inicio = performance.now();
                zonaJuego.addEventListener('click', alTocar);
                document.addEventListener('keydown', alTeclear, true);
                nueva();
            },
            detener() {
                activo = false;
                document.removeEventListener('keydown', alTeclear, true);
            },
        };
    }

    const MOTORES = {
        meteoros: motorMeteoros, teclado: motorTeclado, clasifica: motorClasifica, robot: motorRobot,
        atajos: motorAtajos, mensaje: motorMensaje, rutas: motorRutas, formato: motorFormato,
    };

    // Textos de cada juego: cortes de estrellas, consejo inicial, lo que falta y datos del resultado
    const plural = (n, uno, varios) => `${n} ${n === 1 ? uno : varios}`;
    const TEXTOS = {
        meteoros: {
            corte: (cfg, p) => plural(Math.ceil(cfg.meta * p / 100), 'meteoro', 'meteoros'),
            tip: cfg => `💡 Escribe la palabra completa${cfg.acentos === 'opcionales' ? ' (los acentos son opcionales)' : ''}. Enter borra lo que llevas.`,
            falta: cfg => `destruye ${plural(Math.ceil(cfg.meta / 2), 'meteoro', 'meteoros')}`,
            datos: (r, cfg, e) => [`☄️ ${r.aciertos} meteoros`, `🎯 ${r.precision}% precisión`, `⌨️ ${r.ppm} palabras/min`,
                ...(e.vidas ? [`❤️ +${e.vidas * 50} por vidas`] : [])],
        },
        teclado: {
            corte: (cfg, p) => `${Math.ceil(cfg.rondas * p / 100)} a la primera`,
            tip: cfg => (cfg.modo === 'guiado' ? '💡 La tecla correcta brilla en el teclado de la pantalla. ¡Búscala en el tuyo!'
                : '🕵️ Modo reto: solo verás la letra. Si fallas dos veces te damos una pista.'),
            falta: cfg => `acierta ${Math.ceil(cfg.rondas / 2)} teclas a la primera`,
            datos: (r, cfg, e) => [`✅ ${r.aciertos} de ${cfg.rondas} a la primera`, `🎯 ${r.precision}% precisión`, `⏱️ ${e.duracion} s`],
        },
        clasifica: {
            corte: (cfg, p) => plural(Math.ceil(cfg.rondas * p / 100), 'correcta', 'correctas'),
            tip: cfg => `💡 Toca el grupo correcto, arrastra la tarjeta o usa las flechas.${cfg.tiempo ? ` Tienes ${cfg.tiempo} segundos por tarjeta.` : ''}`,
            falta: cfg => `acierta ${plural(Math.ceil(cfg.rondas / 2), 'tarjeta', 'tarjetas')}`,
            datos: (r, cfg, e) => [`✅ ${r.aciertos} de ${cfg.rondas} correctas`, `🔥 Mejor racha: ${e.racha || 0}`, `⏱️ ${e.duracion} s`],
        },
        robot: {
            corte: (cfg, p) => plural(Math.ceil(cfg.niveles * p / 100), 'laberinto', 'laberintos'),
            tip: cfg => (cfg.modo === 'giros'
                ? '🔄 «Avanzar» mueve al robot hacia donde apunta su flecha y los giros lo voltean sin moverlo. Tienes 3 intentos por laberinto.'
                : '➡️ Cada flecha mueve al robot una casilla. Arma todo el programa y luego presiona ▶. Tienes 3 intentos por laberinto.')
                + (cfg.bucles ? ' 🔁 repite la instrucción que sigue.' : ''),
            falta: cfg => `resuelve ${plural(Math.ceil(cfg.niveles / 2), 'laberinto', 'laberintos')}`,
            datos: (r, cfg, e) => [`🔋 ${r.aciertos} de ${cfg.niveles} laberintos`, `✨ ${e.perfectos || 0} con código perfecto`, `⏱️ ${e.duracion} s`],
        },
        atajos: {
            corte: (cfg, p) => plural(Math.ceil(cfg.rondas * p / 100), 'situación', 'situaciones'),
            tip: cfg => (cfg.modo === 'ninja'
                ? '🥷 Modo ninja: no hay pistas. Si fallas, te mostramos la combinación. Tienes 3 intentos por situación.'
                : '💡 Mantén presionada la tecla Ctrl y luego toca la letra. Te mostramos la combinación para que la aprendas.'),
            falta: cfg => `resuelve ${plural(Math.ceil(cfg.rondas / 2), 'situación', 'situaciones')}`,
            datos: (r, cfg, e) => [`✅ ${r.aciertos} de ${cfg.rondas} resueltas`, `⚡ ${e.perfectos || 0} al primer intento`, `⏱️ ${e.duracion} s`],
        },
        mensaje: {
            corte: (cfg, p) => plural(Math.ceil(cfg.rondas * p / 100), 'mensaje', 'mensajes'),
            tip: cfg => `💡 Usa la tabla de pistas: cada código es una letra. Tienes ${cfg.intentos} intentos y una pista por mensaje.`,
            falta: cfg => `descifra ${plural(Math.ceil(cfg.rondas / 2), 'mensaje', 'mensajes')}`,
            datos: (r, cfg, e) => [`🔓 ${r.aciertos} de ${cfg.rondas} descifrados`, `✨ ${e.perfectos || 0} sin pistas ni errores`, `⏱️ ${e.duracion} s`],
        },
        rutas: {
            corte: (cfg, p) => plural(Math.ceil(cfg.rondas * p / 100), 'archivo', 'archivos'),
            tip: cfg => (cfg.modo === 'buscar'
                ? '🔎 Piensa dónde guardarías cada archivo: las canciones en Música, las fotos en Imágenes, las tareas en Documentos…'
                : '🧭 Sigue la ruta que te damos abriendo cada carpeta en orden.') + ' Si te pasas por más de 3 clics del mínimo, no cuenta.',
            falta: cfg => `encuentra ${plural(Math.ceil(cfg.rondas / 2), 'archivo', 'archivos')} con pocos clics`,
            datos: (r, cfg, e) => [`📁 ${r.aciertos} de ${cfg.rondas} encontrados`, `🎯 ${e.perfectos || 0} con los clics mínimos`, `⏱️ ${e.duracion} s`],
        },
        formato: {
            corte: (cfg, p) => plural(Math.ceil(cfg.rondas * p / 100), 'texto', 'textos'),
            tip: () => '✏️ Toca las palabras para seleccionarlas y usa la barra de herramientas. Ctrl+B, Ctrl+I y Ctrl+U también funcionan.',
            falta: cfg => `iguala ${plural(Math.ceil(cfg.rondas / 2), 'texto', 'textos')}`,
            datos: (r, cfg, e) => [`🎨 ${r.aciertos} de ${cfg.rondas} iguales al modelo`, `✨ ${e.perfectos || 0} a la primera`, `⏱️ ${e.duracion} s`],
        },
    };

    // =========================================================
    // PANTALLA DEL JUEGO (intro → cuenta regresiva → juego → resultado)
    // =========================================================
    function abrir(opciones) {
        const juego = opciones.juego;
        const cfg = completar(juego.plantilla, juego.config);
        const capa = document.createElement('div');
        capa.className = `jg-pantalla jg-${juego.plantilla}`;
        capa.setAttribute('role', 'dialog');
        capa.setAttribute('aria-modal', 'true');
        capa.setAttribute('aria-label', juego.nombre);
        capa.innerHTML = `
            <div class="jg-barra">
                <div class="jg-titulo"><span class="e">${esc(juego.icono)}</span><span class="t">${esc(juego.nombre)}</span>
                    ${opciones.demo ? '<span class="jg-demo">Vista previa</span>' : ''}</div>
                <div class="jg-hud" data-hud></div>
                <button type="button" class="jg-cerrar" data-cerrar aria-label="Salir del juego"><i class="bi bi-x-lg"></i></button>
            </div>
            <div class="jg-escenario">
                <div class="jg-juego" data-juego></div>
                <div class="jg-capa" data-capa></div>
            </div>`;
        // Dentro de una ventana de Bootstrap abierta, para que su «trampa de foco» no robe el teclado
        (document.querySelector('.modal.show') || document.body).appendChild(capa);
        document.body.classList.add('jg-abierto');
        let zonaJuego = capa.querySelector('[data-juego]');
        const hud = capa.querySelector('[data-hud]');
        const panel = capa.querySelector('[data-capa]');
        let motor = null;
        let partida = null;
        let cerrado = false;
        let huboCambios = false;

        const textos = TEXTOS[juego.plantilla];
        const corte = p => textos.corte(cfg, p);

        function mostrar(html) { panel.innerHTML = html; panel.classList.add('visible'); panel.scrollTop = 0; }
        function ocultar() { panel.classList.remove('visible'); panel.innerHTML = ''; }

        function cerrar() {
            if (cerrado) return;
            cerrado = true;
            motor?.detener();
            capa.classList.add('saliendo');
            document.body.classList.remove('jg-abierto');
            document.removeEventListener('keydown', alTeclaGlobal, true);
            setTimeout(() => capa.remove(), 200);
            opciones.alCerrar?.(huboCambios);
        }
        // Enter empieza o vuelve a jugar; Escape sale (nunca a media partida ni cierra lo que hay detrás)
        function alTeclaGlobal(e) {
            if (e.key === 'Escape') {
                e.preventDefault();
                e.stopPropagation();
                if (panel.classList.contains('visible')) cerrar();
                return;
            }
            if (e.key !== 'Enter' || !panel.classList.contains('visible')) return;
            const principal = panel.querySelector('[data-empezar], [data-otra]');
            if (principal && !principal.disabled) { e.preventDefault(); principal.click(); }
        }
        document.addEventListener('keydown', alTeclaGlobal, true);
        capa.querySelector('[data-cerrar]').addEventListener('click', cerrar);

        function intro() {
            hud.innerHTML = '';
            const info = juego.info || {};
            mostrar(`<div class="jg-tarjeta">
                <div class="jg-icono-grande">${esc(juego.icono)}</div>
                <h2>${esc(juego.nombre)}</h2>
                <p class="jg-como">${esc(info.como || '')}</p>
                <div class="jg-meta"><span>🎯 ${esc(juego.meta || '')}</span></div>
                <div class="jg-cortes"><span>⭐ ${corte(50)}</span><span>⭐⭐ ${corte(70)}</span><span>⭐⭐⭐ ${corte(90)}</span></div>
                <p class="jg-tip">${esc(textos.tip(cfg))}</p>
                <button type="button" class="jg-boton" data-empezar><i class="bi bi-play-fill"></i> ¡Jugar!</button>
            </div>`);
            const empezarBtn = panel.querySelector('[data-empezar]');
            empezarBtn.addEventListener('click', empezar);
            setTimeout(() => empezarBtn.focus(), 50);
        }

        function error(texto) {
            mostrar(`<div class="jg-tarjeta"><div class="jg-icono-grande">😵</div><h2>¡Ups!</h2><p class="jg-como">${esc(texto)}</p>
                <div class="jg-acciones"><button type="button" class="jg-boton" data-salir>Salir</button></div></div>`);
            panel.querySelector('[data-salir]').addEventListener('click', cerrar);
        }

        function cuentaRegresiva() {
            return new Promise(resolver => {
                let n = 3;
                mostrar('<div class="jg-cuenta pop" data-cuenta>3</div>');
                sfx.cuenta();
                const reloj = setInterval(() => {
                    const el = panel.querySelector('[data-cuenta]');
                    if (!el || cerrado) { clearInterval(reloj); return; }
                    n -= 1;
                    if (n > 0) { el.textContent = n; sfx.cuenta(); }
                    else if (n === 0) { el.textContent = '¡YA!'; sfx.ya(); }
                    else { clearInterval(reloj); resolver(); return; }
                    el.classList.remove('pop');
                    void el.offsetWidth;
                    el.classList.add('pop');
                }, 650);
            });
        }

        async function empezar() {
            panel.querySelectorAll('button').forEach(b => { b.disabled = true; });
            partida = null;
            if (!opciones.demo) {
                try { partida = await opciones.iniciar(); } catch (e) { error(e.message || 'No se pudo empezar. Revisa tu conexión.'); return; }
            }
            await cuentaRegresiva();
            if (cerrado) return;
            ocultar();
            const limpia = document.createElement('div');
            limpia.className = `jg-juego jg-juego-${juego.plantilla}`;
            limpia.dataset.juego = '';
            zonaJuego.replaceWith(limpia);
            zonaJuego = limpia;
            motor = MOTORES[juego.plantilla](zonaJuego, cfg, hud, terminar);
            motor.iniciar();
        }

        async function terminar(estadisticas) {
            motor = null;
            mostrar('<div class="jg-tarjeta"><div class="jg-cargando"><span class="spinner-border spinner-border-sm"></span> Contando tu botín…</div></div>');
            let resumen;
            if (opciones.demo) {
                resumen = { ...calificarLocal(juego.plantilla, cfg, estadisticas), demo: true };
            } else {
                try {
                    resumen = await opciones.terminar(partida, estadisticas);
                    huboCambios = true;
                } catch (e) { error(e.message || 'No se pudo guardar tu partida.'); return; }
            }
            resultado(resumen, estadisticas);
        }

        function lineasBotin(r) {
            const lineas = [];
            const nota = `Calificación <b>${(r.calificacion / 10).toFixed(1)}</b>`;
            const falta = textos.falta(cfg);
            if (r.demo) {
                lineas.push(`<div class="nota">${nota} · 👀 Vista previa: esta partida no se guarda.</div>`);
            } else if (r.mision) {
                const m = r.mision;
                if (m.primera) lineas.push(`<div class="ok">🗺️ ¡Misión superada! · ${nota}</div>`);
                else if (m.mejoro) lineas.push(`<div class="ok">📈 ¡Mejoraste tu calificación de la misión! · ${nota}</div>`);
                else if (m.aprobada) lineas.push(`<div class="nota">${nota}. Tu mejor calificación en la misión sigue igual: ¡supérala para ganar más estrellas!</div>`);
                else lineas.push(`<div class="nota">${nota}. Para superar la misión ${falta}. ¡Tú puedes!</div>`);
            } else if (r.premio_diario) {
                lineas.push('<div class="ok">🎁 ¡Premio del día de este juego!</div>');
            } else if (opciones.monedasArcade && r.estrellas) {
                lineas.push('<div class="nota">Ya cobraste el premio de hoy de este juego. ¡Sigue jugando por el récord!</div>');
            } else if (opciones.monedasArcade) {
                lineas.push(`<div class="nota">Consigue al menos ⭐ (${corte(50)}) para ganar monedas.</div>`);
            }
            if (r.monedas || r.xp) {
                lineas.push(`<div class="premio">${r.monedas ? `<span>🪙 +${r.monedas}</span>` : ''}${r.xp ? `<span>⚡ +${r.xp} XP</span>` : ''}</div>`);
            }
            return lineas.join('');
        }

        function ranking(r) {
            if (!r.ranking || !r.ranking.length) return '';
            const medallas = ['🥇', '🥈', '🥉'];
            const filas = r.ranking.map((f, i) => `
                <div class="fila ${f.alumno_id === opciones.alumnoId ? 'yo' : ''}">
                    <span class="pos">${medallas[i] || i + 1}</span><span class="n">${esc(f.nombre)}</span><b>${miles(f.puntaje)}</b>
                </div>`).join('');
            const extra = r.posicion && r.posicion > r.ranking.length ? `<div class="fila yo"><span class="pos">${r.posicion}</span><span class="n">Tú vas en el lugar #${r.posicion}</span></div>` : '';
            return `<div class="jg-ranking"><div class="t">🏆 Top de la semana</div>${filas}${extra}</div>`;
        }

        function resultado(r, estadisticas) {
            const titulos = ['¡Casi!', '¡Lo lograste!', '¡Muy bien!', '¡Increíble!'];
            const datos = textos.datos(r, cfg, estadisticas);
            mostrar(`<div class="jg-tarjeta jg-final">
                <div class="jg-resultado-titulo">${titulos[r.estrellas] || titulos[0]}</div>
                <div class="jg-estrellas">${[1, 2, 3].map(i => `<span class="${i <= r.estrellas ? 'on' : ''}" style="--i:${i}">⭐</span>`).join('')}</div>
                <div class="jg-puntaje"><span>Puntaje</span><b>${miles(r.puntaje)}</b></div>
                ${r.record ? '<div class="jg-record">🏆 ¡Nuevo récord personal!</div>' : (r.mejor ? `<div class="jg-mejor">Tu récord: ${miles(r.mejor)}</div>` : '')}
                <div class="jg-datos">${datos.map(d => `<span>${d}</span>`).join('')}</div>
                <div class="jg-botin">${lineasBotin(r)}</div>
                ${ranking(r)}
                <div class="jg-acciones">
                    <button type="button" class="jg-boton secundario" data-otra><i class="bi bi-arrow-repeat"></i> Jugar otra vez</button>
                    <button type="button" class="jg-boton" data-salir>${esc(opciones.textoSalir || 'Salir')}</button>
                </div>
            </div>`);
            panel.querySelector('[data-otra]').addEventListener('click', empezar);
            panel.querySelector('[data-salir]').addEventListener('click', cerrar);
            if (r.estrellas) sfx.fin(); else sfx.triste();
            if ((r.estrellas >= 2 || r.record) && typeof window.NLConfeti === 'function') window.NLConfeti(r.record ? 'monedas' : 'normal');
            if (r.total_monedas !== undefined && typeof window.NLActualizarMonedas === 'function') window.NLActualizarMonedas(r.total_monedas);
        }

        intro();
        return { cerrar };
    }

    // =========================================================
    // CONEXIÓN CON EL SERVIDOR (lado del alumno)
    // =========================================================
    async function pedir(url, cuerpo, csrf, json = false) {
        const r = await fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest', ...(json ? { 'Content-Type': 'application/json' } : {}) },
            body: json ? JSON.stringify(cuerpo) : new URLSearchParams(cuerpo),
        });
        let datos = {};
        try { datos = await r.json(); } catch (e) { /* respuesta sin JSON */ }
        if (!r.ok || !datos.ok) throw new Error(datos.mensaje || 'Algo salió mal. Inténtalo de nuevo.');
        return datos;
    }

    // Botones con data-jugar: abren el juego descrito en el <script type="application/json"> indicado
    document.addEventListener('click', e => {
        const boton = e.target.closest('[data-jugar]');
        if (!boton) return;
        e.preventDefault();
        let juego;
        try { juego = JSON.parse(document.getElementById(boton.dataset.jugar).textContent); } catch (err) { return; }
        const demo = boton.hasAttribute('data-demo');
        const csrf = boton.dataset.csrf;
        abrir({
            juego,
            demo,
            alumnoId: Number(boton.dataset.alumno) || null,
            monedasArcade: Number(boton.dataset.monedasArcade) || 0,
            textoSalir: boton.dataset.textoSalir,
            iniciar: async () => (await pedir(boton.dataset.urlIniciar, boton.dataset.mision ? { mision: boton.dataset.mision } : {}, csrf)).partida,
            terminar: (partida, estadisticas) => pedir(boton.dataset.urlTerminar.replace('/0/', `/${partida}/`), estadisticas, csrf, true),
            alCerrar: huboCambios => { if (huboCambios && boton.hasAttribute('data-recargar')) location.reload(); },
        });
    });

    // Pestañas «Semana / Siempre» del ranking de un juego
    document.addEventListener('click', e => {
        const boton = e.target.closest('[data-tab-ranking]');
        if (!boton) return;
        const caja = boton.closest('.ranking-juego');
        caja.querySelectorAll('[data-tab-ranking]').forEach(b => b.classList.toggle('activo', b === boton));
        caja.querySelectorAll('[data-ranking]').forEach(l => l.classList.toggle('d-none', l.dataset.ranking !== boton.dataset.tabRanking));
    });

    window.NLJuegos = { abrir, completar, calificarLocal, codigoDe, normalizarSecreto };
})();

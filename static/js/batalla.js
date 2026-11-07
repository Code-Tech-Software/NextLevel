/* =========================================================
   NEXT-LEVEL · Batalla en vivo (proyector del profe y pantalla del alumno)

   No hay conexión abierta: cada segundo se pregunta «¿cambió algo?» con la ficha que se tiene y el servidor
   contesta {cambio: false} casi siempre. Los relojes corren aquí con lo que faltaba cuando llegó el estado.
   ========================================================= */
(function () {
    'use strict';

    const raiz = document.getElementById('batalla');
    if (!raiz) return;

    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
    const escena = $('[data-escena]', raiz);
    const Sonido = window.NLSonido || { play() {}, alternar() { return true; }, activo: true };
    const COLORES = ['coral', 'cielo', 'ambar', 'esmeralda', 'uva', 'rosa'];
    const MEDALLAS = ['🥇', '🥈', '🥉'];

    function escapar(texto) {
        const div = document.createElement('div');
        div.textContent = texto ?? '';
        return div.innerHTML;
    }
    const numero = n => Number(n || 0).toLocaleString('es-MX');
    const ordinal = n => ({ 1: '1.er', 2: '2.º', 3: '3.er' }[n] || `${n}.º`);
    const plural = (n, uno, varios) => `${n} ${n === 1 ? uno : varios}`;

    function csrf() {
        const input = $('[name=csrfmiddlewaretoken]');
        return input ? input.value : '';
    }
    async function pedir(url, datos) {
        const opciones = { headers: { 'X-Requested-With': 'XMLHttpRequest' }, cache: 'no-store' };
        if (datos) {
            const body = new FormData();
            Object.entries(datos).forEach(([k, v]) => body.append(k, v));
            Object.assign(opciones, { method: 'POST', body });
            opciones.headers['X-CSRFToken'] = csrf();
        }
        const r = await fetch(url, opciones);
        let json = null;
        try { json = await r.json(); } catch (e) { /* respuesta sin JSON */ }
        if (!r.ok && !(json && (json.mensaje || json.salir))) throw new Error('Error ' + r.status);
        return json || {};
    }

    // ---------- Estado y relojes ----------
    let estado = JSON.parse($('#batalla-estado').textContent);
    let recibido = performance.now();
    const transcurrido = () => performance.now() - recibido;
    const faltaPreparar = () => Math.max(0, (estado.inicio_ms || 0) - transcurrido());
    const faltaContestar = () => Math.max(0, (estado.restante_ms || 0) - transcurrido());

    function aviso(texto, tipo = 'info') {
        let caja = $('.bt-aviso');
        if (!caja) {
            caja = document.createElement('div');
            caja.className = 'bt-aviso';
            caja.setAttribute('role', 'status');
            document.body.appendChild(caja);
        }
        caja.textContent = texto;
        caja.dataset.tipo = tipo;
        caja.classList.add('visible');
        clearTimeout(caja._t);
        caja._t = setTimeout(() => caja.classList.remove('visible'), 3200);
    }

    function confetiPodio() {
        if (typeof window.confetti !== 'function') return;
        const colores = ['#fde047', '#f59e0b', '#38bdf8', '#a855f7', '#10b981', '#fb7185'];
        const fin = Date.now() + 1800;
        (function lluvia() {
            window.confetti({ particleCount: 6, angle: 60, spread: 70, origin: { x: 0, y: 0.7 }, colors: colores });
            window.confetti({ particleCount: 6, angle: 120, spread: 70, origin: { x: 1, y: 0.7 }, colors: colores });
            if (Date.now() < fin) requestAnimationFrame(lluvia);
        })();
    }

    // Consulta periódica: una a la vez, más lenta si la pestaña está escondida, y avisa si se pierde la red
    function consultar({ url, ficha, aplicar, intervalo, alFallar, alVolver }) {
        let fallos = 0;
        let pendiente = null;
        async function paso() {
            try {
                const sep = url.includes('?') ? '&' : '?';
                const datos = await pedir(`${url}${sep}ficha=${encodeURIComponent(ficha())}`);
                if (fallos) { fallos = 0; alVolver?.(); }
                aplicar(datos);
            } catch (e) {
                fallos += 1;
                if (fallos === 3) alFallar?.();
            }
            const espera = document.hidden ? 5000 : intervalo() * (fallos ? Math.min(fallos, 4) : 1);
            pendiente = setTimeout(paso, espera);
        }
        pendiente = setTimeout(paso, intervalo());
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) { clearTimeout(pendiente); paso(); }
        });
    }

    // ---------- Piezas compartidas ----------
    function htmlOpciones(opciones, clase = '') {
        return opciones.map((o, i) => `
            <div class="bt-op c-${COLORES[i % COLORES.length]} ${clase}" data-op="${i}">
                <span class="letra">${o.letra}</span><span class="txt">${escapar(o.texto)}</span>
            </div>`).join('');
    }

    function htmlPodio(podio, conMonedas) {
        const orden = [1, 0, 2].filter(i => podio[i]);
        return `<div class="podio bt-podio">${orden.map(i => {
            const j = podio[i];
            const pos = i + 1;
            return `<div class="podio-lugar p${pos}">
                <div class="avatar-wrap">${pos === 1 ? '<span class="corona">👑</span>' : ''}<img src="${escapar(j.avatar)}" alt="" class="avatar"></div>
                <div class="n">${escapar(j.nombre)} ${escapar(j.apellido)} ${escapar(j.equipo || '')}</div>
                <div class="pts">${numero(j.puntos)}</div>
                ${conMonedas && j.monedas ? `<div class="premio"><i class="bi bi-coin"></i> +${j.monedas}</div>` : ''}
                <div class="podio-bloque">${pos}</div>
            </div>`;
        }).join('')}</div>`;
    }

    function htmlEquipos(equipos, titulo = '🛡️ Equipos') {
        if (!equipos || !equipos.length) return '';
        return `<div class="bt-equipos"><h3>${titulo}</h3>${equipos.map(e => `
            <div class="bt-equipo"><span class="pos">${e.posicion <= 3 ? MEDALLAS[e.posicion - 1] : e.posicion}</span>
            <span class="e">${escapar(e.emoji)}</span><span class="n">${escapar(e.nombre)}</span>
            <span class="v">${numero(e.promedio)}</span></div>`).join('')}</div>`;
    }

    // =====================================================
    // PROYECTOR (profe)
    // =====================================================
    function iniciarProyector() {
        const urls = raiz.dataset;
        const principal = $('[data-principal]', raiz);
        const secundario = $('[data-secundario]', raiz);
        const contador = $('[data-contador]', raiz);
        let escenaActual = '';
        let ocupado = false;
        let revelando = false;
        let ultimoSegundo = null;
        let celebrado = false;

        async function accion(nombre, extra = {}) {
            if (ocupado) return;
            ocupado = true;
            principal.disabled = true;
            try {
                const datos = await pedir(urls.urlAccion, { accion: nombre, v: estado.v, ...extra });
                if (datos.estado) aplicar(datos.estado);
            } catch (e) {
                aviso('No se pudo. Revisa la conexión e inténtalo otra vez.', 'error');
            } finally {
                ocupado = false;
                principal.disabled = estado.estado === 'sala' && !(estado.jugadores || []).length;
            }
        }

        function aplicar(nuevo) {
            if (!nuevo || (nuevo.v < estado.v)) return;   // una respuesta vieja que llegó tarde
            estado = nuevo;
            recibido = performance.now();
            pintar();
        }

        function boton(el, texto, alHacer, icono = '') {
            el.hidden = !texto;
            if (!texto) return;
            el.innerHTML = `${icono ? `<i class="bi ${icono}"></i> ` : ''}${texto}`;
            el.onclick = alHacer;
        }

        function pintar() {
            $('[data-total-jugadores]', raiz).textContent = estado.total_jugadores;
            const clave = `${estado.estado}:${estado.indice}`;
            const nueva = clave !== escenaActual;
            escenaActual = clave;
            contador.hidden = estado.estado === 'sala' || estado.estado === 'final';
            contador.textContent = `${estado.indice + 1} / ${estado.total}`;

            if (estado.estado === 'sala') pintarSala(nueva);
            else if (estado.estado === 'pregunta') pintarPregunta(nueva);
            else if (estado.estado === 'resultado') pintarResultado(nueva);
            else pintarFinal(nueva);
        }

        // ---------- Sala de espera ----------
        function pintarSala(nueva) {
            if (nueva) {
                escena.innerHTML = `
                    <div class="bp-sala">
                        <section class="bp-entrar">
                            <h2>¡Entra a la batalla!</h2>
                            <ol>
                                <li><span>1</span><div>Abre <b>${escapar(urls.sitio)}</b></div></li>
                                <li><span>2</span><div>Elige <b>${escapar(urls.clase)}</b> y escribe tu PIN</div></li>
                                <li><span>3</span><div>Toca <b>⚔️ ¡Batalla en vivo!</b></div></li>
                            </ol>
                            <div class="bp-qr" data-qr hidden></div>
                        </section>
                        <section class="bp-lobby">
                            <div class="bp-lobby-titulo"><b data-n>0</b> <span data-n-texto>en la sala</span></div>
                            <div class="bp-avatares" data-avatares></div>
                            <div class="bp-esperando" data-esperando><span class="e">👀</span>Esperando a los primeros valientes…</div>
                        </section>
                    </div>`;
                pintarQr();
            }
            const lista = $('[data-avatares]', escena);
            const ids = new Set(estado.jugadores.map(j => String(j.id)));
            $$('[data-jugador]', lista).forEach(el => { if (!ids.has(el.dataset.jugador)) el.remove(); });
            let nuevos = 0;
            estado.jugadores.forEach(j => {
                if ($(`[data-jugador="${j.id}"]`, lista)) return;
                const chip = document.createElement('button');
                chip.type = 'button';
                chip.className = 'bp-avatar' + (nueva ? '' : ' entra');
                chip.dataset.jugador = j.id;
                chip.title = `Sacar a ${j.nombre} de la sala`;
                chip.innerHTML = `<img src="${escapar(j.avatar)}" alt="" class="avatar"><span class="n">${escapar(j.nombre)} ${escapar(j.apellido)}</span>${j.equipo ? `<span class="eq">${escapar(j.equipo)}</span>` : ''}<i class="bi bi-x-circle-fill quitar" aria-hidden="true"></i>`;
                chip.addEventListener('click', () => quitar(j));
                lista.appendChild(chip);
                nuevos += 1;
            });
            if (nuevos && !nueva) Sonido.play('pop');
            $('[data-n]', escena).textContent = estado.jugadores.length;
            $('[data-n-texto]', escena).textContent = estado.jugadores.length === 1 ? 'jugador en la sala' : 'jugadores en la sala';
            $('[data-esperando]', escena).hidden = estado.jugadores.length > 0;
            boton(principal, estado.jugadores.length ? '¡Empezar!' : 'Esperando jugadores…', () => accion('empezar'), 'bi-play-fill');
            principal.disabled = !estado.jugadores.length;
            boton(secundario, '');
        }

        async function quitar(jugador) {
            if (typeof Swal !== 'undefined') {
                const r = await Swal.fire({
                    title: `¿Sacar a ${jugador.nombre}?`, text: 'Si fue un error, puede volver a entrar.',
                    showCancelButton: true, confirmButtonText: 'Sacar', cancelButtonText: 'Cancelar', reverseButtons: true,
                    buttonsStyling: false, customClass: { popup: 'swal-juego', confirmButton: 'g-btn rojo', cancelButton: 'g-btn blanco' },
                });
                if (!r.isConfirmed) return;
            }
            accion('quitar', { jugador: jugador.id });
        }

        function pintarQr() {
            const caja = $('[data-qr]', escena);
            if (!caja || typeof window.qrcode !== 'function') return;
            try {
                const qr = window.qrcode(0, 'M');
                qr.addData(urls.urlEntrar);
                qr.make();
                caja.innerHTML = qr.createSvgTag({ cellSize: 4, margin: 0, scalable: true }) + '<span>o escanea</span>';
                caja.hidden = false;
            } catch (e) { /* sin QR */ }
        }

        // ---------- Pregunta ----------
        function pintarPregunta(nueva) {
            const p = estado.pregunta;
            if (nueva) {
                revelando = false;
                ultimoSegundo = null;
                escena.innerHTML = `
                    <div class="bp-pregunta">
                        <div class="bp-prep" data-prep><div class="k">Pregunta ${estado.indice + 1} de ${estado.total}</div><div class="n" data-prep-n>3</div><div class="t">¡Prepárense!</div></div>
                        <div class="bp-enunciado">${escapar(p.texto)}</div>
                        <div class="bp-opciones n${p.opciones.length}">${htmlOpciones(p.opciones)}</div>
                        <div class="bp-pie">
                            <div class="bp-reloj" data-reloj><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="44" class="fondo"/><circle cx="50" cy="50" r="44" class="avance" data-anillo/></svg><span data-seg>${estado.segundos}</span></div>
                            <div class="bp-contestaron">
                                <div class="t"><b data-resp>0</b> de <b data-de>0</b> contestaron</div>
                                <div class="barra-bp"><span data-resp-barra></span></div>
                                <div class="faltan" data-faltan></div>
                            </div>
                        </div>
                    </div>`;
            }
            const total = estado.total_jugadores || 0;
            $('[data-resp]', escena).textContent = estado.respondieron || 0;
            $('[data-de]', escena).textContent = total;
            $('[data-resp-barra]', escena).style.width = (total ? (estado.respondieron || 0) * 100 / total : 0) + '%';
            const faltan = estado.faltan || [];
            $('[data-faltan]', escena).textContent = faltan.length && faltan.length <= 3 && estado.respondieron ? `Faltan: ${faltan.join(', ')}` : '';
            boton(principal, 'Mostrar respuesta', () => accion('revelar'), 'bi-eye-fill');
            boton(secundario, 'Terminar', terminarYa);
            // Si ya contestaron todos, no hay que esperar al reloj
            if (total && estado.respondieron >= total && !faltaPreparar()) revelarPronto(700);
        }

        function revelarPronto(retraso) {
            if (revelando) return;
            revelando = true;
            setTimeout(() => accion('revelar'), retraso);
        }

        // ---------- Resultado ----------
        function pintarResultado(nueva) {
            const p = estado.pregunta;
            const maximo = Math.max(1, ...p.opciones.map(o => o.votos));
            const ultima = estado.indice + 1 >= estado.total;
            if (nueva) {
                Sonido.play('exito');
                escena.innerHTML = `
                    <div class="bp-resultado">
                        <section class="bp-res-izq">
                            <div class="bp-enunciado chico">${escapar(p.texto)}</div>
                            <div class="bp-barras">${p.opciones.map((o, i) => `
                                <div class="bp-barra c-${COLORES[i % COLORES.length]} ${o.correcta ? 'correcta' : 'incorrecta'}">
                                    <span class="letra">${o.correcta ? '<i class="bi bi-check-lg"></i>' : o.letra}</span>
                                    <span class="txt">${escapar(o.texto)}</span>
                                    <span class="relleno" style="--ancho:${o.votos * 100 / maximo}%"></span>
                                    <span class="votos">${o.votos}</span>
                                </div>`).join('')}
                            </div>
                            <div class="bp-dato">✅ <b>${estado.aciertos_pregunta}</b> de ${plural(estado.respondieron, 'respuesta', 'respuestas')} correctas</div>
                        </section>
                        <aside class="bp-top">
                            <h3>🏆 Los mejores</h3>
                            ${(estado.ranking || []).map(j => `
                                <div class="bp-fila">
                                    <span class="pos">${j.posicion}</span>
                                    <img src="${escapar(j.avatar)}" alt="" class="avatar">
                                    <span class="n">${escapar(j.nombre)} ${escapar(j.apellido)} ${escapar(j.equipo)}</span>
                                    ${j.sube > 0 ? `<span class="sube">▲${j.sube}</span>` : ''}
                                    ${j.gano ? `<span class="gano">+${numero(j.gano)}</span>` : ''}
                                    <span class="pts">${numero(j.puntos)}</span>
                                </div>`).join('')}
                            ${htmlEquipos(estado.equipos)}
                        </aside>
                    </div>`;
                requestAnimationFrame(() => requestAnimationFrame(() => $$('.relleno', escena).forEach(r => r.classList.add('lleno'))));
            }
            boton(principal, ultima ? 'Ver el podio' : 'Siguiente pregunta', () => accion('siguiente'), ultima ? 'bi-trophy-fill' : 'bi-arrow-right');
            boton(secundario, ultima ? '' : 'Terminar', terminarYa);
        }

        // ---------- Final ----------
        function pintarFinal(nueva) {
            if (nueva || !estado.premios_entregados || !escena.dataset.listo) {
                escena.dataset.listo = estado.premios_entregados ? '1' : '';
                const podio = estado.podio || [];
                const premios = estado.con_premios
                    ? `🥇 +${estado.premios[0]} · 🥈 +${estado.premios[1]} · 🥉 +${estado.premios[2]}${estado.premio_participar ? ` · +${estado.premio_participar} a todos los que jugaron` : ''}`
                    : 'Batalla de práctica: sin monedas.';
                escena.innerHTML = `
                    <div class="bp-final">
                        <section class="bp-final-podio">
                            <h2>${estado.por_equipos ? '🏆 ¡Ganó el equipo…!' : '🏆 ¡Terminó la batalla!'}</h2>
                            ${estado.por_equipos && estado.equipos?.length ? `<div class="bp-equipo-ganador">${escapar(estado.equipos[0].emoji)} ${escapar(estado.equipos[0].nombre)}</div>` : ''}
                            ${podio.length ? htmlPodio(podio, true) : '<p class="bp-vacio">Nadie contestó esta vez.</p>'}
                            <div class="bp-premios">${estado.premios_entregados ? `<i class="bi bi-check-circle-fill"></i> Premios entregados · ${premios}` : '<span class="spinner-border spinner-border-sm"></span> Repartiendo premios…'}</div>
                        </section>
                        <aside class="bp-final-lado">
                            ${htmlEquipos(estado.equipos)}
                            ${(estado.ranking || []).length > 3 ? `<h3>Los siguientes</h3>${estado.ranking.slice(3, 8).map(j => `
                                <div class="bp-fila chica"><span class="pos">${j.posicion}</span><img src="${escapar(j.avatar)}" alt="" class="avatar"><span class="n">${escapar(j.nombre)} ${escapar(j.apellido)}</span><span class="pts">${numero(j.puntos)}</span></div>`).join('')}` : ''}
                            ${(estado.resumen || []).length ? `<h3>💡 Para repasar</h3>${estado.resumen.map(f => `
                                <div class="bp-repaso"><span class="pct ${f.pct >= 75 ? 'bien' : f.pct >= 50 ? 'regular' : 'mal'}">${f.pct}%</span><span class="t">${escapar(f.texto)}</span></div>`).join('')}` : ''}
                        </aside>
                    </div>`;
                if (!celebrado && podio.length) { celebrado = true; Sonido.play('nivel'); confetiPodio(); }
            }
            boton(principal, 'Jugar otra vez', () => $('[data-form-repetir]').submit(), 'bi-arrow-repeat');
            boton(secundario, 'Ver el resumen', () => { location.href = urls.urlResumen; });
        }

        async function terminarYa() {
            if (typeof Swal !== 'undefined') {
                const r = await Swal.fire({
                    title: '¿Terminar la batalla ya?', text: 'Se reparten los premios con los puntos que llevan.',
                    showCancelButton: true, confirmButtonText: 'Terminar', cancelButtonText: 'Seguir jugando', reverseButtons: true,
                    buttonsStyling: false, customClass: { popup: 'swal-juego', confirmButton: 'g-btn rojo', cancelButton: 'g-btn blanco' },
                });
                if (!r.isConfirmed) return;
            }
            accion('terminar');
        }

        // ---------- Reloj (corre aquí; el servidor solo dice cuánto faltaba) ----------
        function reloj() {
            if (estado.estado === 'pregunta' && escena.querySelector('.bp-pregunta')) {
                const prep = faltaPreparar();
                const capa = $('[data-prep]', escena);
                capa.classList.toggle('visible', prep > 0);
                if (prep > 0) {
                    const n = Math.ceil(prep / 1000);
                    const el = $('[data-prep-n]', escena);
                    if (el.textContent !== String(n)) { el.textContent = n; Sonido.play('tecla'); }
                } else {
                    const resta = faltaContestar();
                    const seg = Math.ceil(resta / 1000);
                    $('[data-seg]', escena).textContent = seg;
                    $('[data-anillo]', escena).style.strokeDashoffset = 276.5 * (1 - resta / (estado.segundos * 1000));
                    $('[data-reloj]', escena).classList.toggle('urgente', seg <= 5);
                    if (seg <= 5 && seg > 0 && seg !== ultimoSegundo) { ultimoSegundo = seg; Sonido.play('click'); }
                    if (resta <= 0) revelarPronto(900);   // un respiro para las respuestas que vienen en camino
                }
            }
            requestAnimationFrame(reloj);
        }

        // ---------- Controles ----------
        const btnSonido = $('[data-sonido]', raiz);
        btnSonido.classList.toggle('silencio', !Sonido.activo);
        btnSonido.addEventListener('click', () => btnSonido.classList.toggle('silencio', !Sonido.alternar()));
        const pantalla = () => {
            if (document.fullscreenElement) document.exitFullscreen?.();
            else document.documentElement.requestFullscreen?.().catch(() => {});
        };
        $('[data-pantalla]', raiz).addEventListener('click', pantalla);
        document.addEventListener('keydown', e => {
            if (e.target.closest('input, textarea, select') || $('.swal2-container')) return;
            // Espacio o Enter sobre un botón ya lo presionan solos: no hay que hacerlo dos veces
            if ([' ', 'Enter'].includes(e.key) && e.target.closest('button, a')) return;
            if ([' ', 'Enter', 'ArrowRight'].includes(e.key) && !principal.hidden && !principal.disabled) {
                e.preventDefault();
                principal.click();
            } else if (e.key === 'f' || e.key === 'F') pantalla();
            else if (e.key === 'm' || e.key === 'M') btnSonido.click();
        });

        const conexion = $('[data-conexion]', raiz);
        pintar();
        requestAnimationFrame(reloj);
        consultar({
            url: urls.urlEstado,
            ficha: () => estado.ficha,
            intervalo: () => 1000,
            aplicar: datos => { if (datos.cambio && datos.estado) aplicar(datos.estado); },
            alFallar: () => { conexion.hidden = false; },
            alVolver: () => { conexion.hidden = true; },
        });
    }

    // =====================================================
    // ALUMNO
    // =====================================================
    function iniciarAlumno() {
        const urls = raiz.dataset;
        const puntosEl = $('[data-mis-puntos]', raiz);
        let escenaActual = '';
        let enviando = false;
        let ultimoResultado = '';
        let celebrado = false;

        function aplicar(nuevo) {
            if (!nuevo) return;
            estado = nuevo;
            recibido = performance.now();
            pintar();
        }

        function pintar() {
            $('[data-titulo]', raiz).textContent = estado.titulo || '';
            const conPuntos = estado.unido && estado.estado !== 'sala' && estado.estado !== 'nada';
            puntosEl.hidden = !conPuntos;
            if (conPuntos) puntosEl.textContent = numero(estado.puntos);

            let clave = estado.estado;
            // El profe en la vista de alumno no juega, pero sí ve las preguntas como las verán sus alumnos
            if (estado.estado === 'sala' && !estado.unido) clave = 'unirse';
            else if (['pregunta', 'resultado'].includes(estado.estado) && !estado.unido && !estado.vista_previa) clave = 'unirse';
            else if (estado.estado === 'pregunta') clave = `pregunta:${estado.indice}`;
            else if (estado.estado === 'resultado') clave = `resultado:${estado.indice}`;
            else if (estado.estado === 'final') clave = `final:${estado.final?.listo ? 1 : 0}`;
            if (clave === escenaActual) {
                if (estado.estado === 'pregunta' && estado.unido) marcarRespuesta();
                return;
            }
            escenaActual = clave;
            escena.className = `ba-escena escena-${clave.split(':')[0]}`;
            ({
                nada: pintarNada, unirse: pintarUnirse, sala: pintarSala, final: pintarFinal,
                pregunta: pintarPregunta, resultado: pintarResultado,
            })[clave.split(':')[0]]();
        }

        function pintarNada() {
            escena.innerHTML = `
                <div class="ba-centro">
                    <div class="ba-ilustracion">🏁</div>
                    <h2>No hay batalla ahora</h2>
                    <p>Cuando tu profe abra una, aparecerá aquí sola.</p>
                    <a href="${urls.urlMapa}" class="g-btn azul"><i class="bi bi-map-fill"></i> Volver al mapa</a>
                </div>`;
        }

        function pintarUnirse() {
            const empezada = estado.estado !== 'sala';
            escena.innerHTML = `
                <div class="ba-centro">
                    <div class="ba-avatar-grande"><img src="${escapar(urls.avatar)}" alt="" class="avatar"></div>
                    <h2>${escapar(estado.titulo)}</h2>
                    <p>${empezada ? '¡Ya empezó, pero todavía puedes entrar!' : `¡Únete y demuestra lo que sabes, ${escapar(urls.nombre)}!`}</p>
                    ${estado.vista_previa
                        ? '<div class="ba-nota-profe">👀 Así ven tus alumnos la entrada. Tú solo miras: para jugar, entra con la cuenta de un alumno.</div>'
                        : '<button type="button" class="g-btn grande oro" data-unirme>⚔️ ¡Entrar a la batalla!</button>'}
                </div>`;
            $('[data-unirme]', escena)?.addEventListener('click', unirme);
        }

        async function unirme(e) {
            const btn = e.currentTarget;
            btn.disabled = true;
            Sonido.play('pop');
            try {
                const datos = await pedir(urls.urlUnirse, {});
                if (datos.salir) { location.href = urls.urlMapa; return; }
                if (!datos.ok && datos.mensaje) aviso(datos.mensaje, 'error');
                aplicar(datos.estado);
            } catch (err) {
                btn.disabled = false;
                aviso('No se pudo entrar. Inténtalo otra vez.', 'error');
            }
        }

        function pintarSala() {
            escena.innerHTML = `
                <div class="ba-centro">
                    <div class="ba-avatar-grande brinca"><img src="${escapar(urls.avatar)}" alt="" class="avatar"></div>
                    <h2>¡Ya estás dentro, ${escapar(urls.nombre)}!</h2>
                    ${estado.equipo ? `<div class="ba-equipo">Juegas con ${escapar(estado.equipo.emoji)} <b>${escapar(estado.equipo.nombre)}</b></div>` : ''}
                    <p>Mira el proyector: tu profe empezará en un momento<span class="puntitos"><i>.</i><i>.</i><i>.</i></span></p>
                    <div class="ba-tip">💡 Responde rápido: entre más rápido aciertes, más puntos ganas. ¡Y los aciertos seguidos dan bono!</div>
                </div>`;
        }

        function pintarPregunta() {
            const p = estado.pregunta;
            escena.innerHTML = `
                <div class="ba-prep" data-prep><div class="k">Pregunta ${estado.indice + 1} de ${estado.total}</div><div class="n" data-prep-n>3</div><div class="t">¡Prepárate!</div></div>
                <div class="ba-pregunta">
                    <div class="ba-barra-tiempo"><span data-barra-tiempo></span></div>
                    <div class="ba-num">Pregunta ${estado.indice + 1} de ${estado.total} <span class="seg" data-seg></span></div>
                    <div class="ba-enunciado">${escapar(p.texto)}</div>
                    <div class="ba-opciones n${p.opciones.length}">${p.opciones.map((o, i) => `
                        <button type="button" class="bt-op c-${COLORES[i % COLORES.length]}" data-op="${i}" ${estado.vista_previa ? 'disabled' : ''}>
                            <span class="letra">${o.letra}</span><span class="txt">${escapar(o.texto)}</span>
                        </button>`).join('')}
                    </div>
                    <div class="ba-espera" data-espera hidden></div>
                    ${estado.vista_previa ? '<div class="ba-nota-profe mt-3">👀 Vista de alumno: tus alumnos tocan aquí su respuesta.</div>' : ''}
                </div>`;
            $$('[data-op]', escena).forEach(b => b.addEventListener('click', () => responder(Number(b.dataset.op))));
            marcarRespuesta();
        }

        function marcarRespuesta() {
            const elegida = estado.mi_respuesta;
            const espera = $('[data-espera]', escena);
            if (!espera) return;
            $$('[data-op]', escena).forEach(b => {
                const i = Number(b.dataset.op);
                b.disabled = estado.vista_previa || elegida != null || enviando;
                b.classList.toggle('elegida', elegida === i);
                b.classList.toggle('apagada', elegida != null && elegida !== i);
            });
            espera.hidden = elegida == null;
            if (elegida != null) espera.innerHTML = '<span class="e">✅</span> ¡Listo! Espera a que se acabe el tiempo…';
        }

        async function responder(opcion) {
            if (enviando || estado.mi_respuesta != null || faltaPreparar() > 0) return;
            enviando = true;
            Sonido.play('click');
            const indice = estado.indice;
            estado.mi_respuesta = opcion;   // se marca al instante; si falla, se quita
            marcarRespuesta();
            try {
                const datos = await pedir(urls.urlResponder, { indice, opcion });
                if (datos.salir) { location.href = urls.urlMapa; return; }
                if (!datos.ok && datos.mensaje) aviso(datos.mensaje, 'error');
                enviando = false;
                if (datos.estado) aplicar(datos.estado);
            } catch (e) {
                enviando = false;
                estado.mi_respuesta = null;
                marcarRespuesta();
                aviso('No llegó tu respuesta. ¡Tócala otra vez!', 'error');
            }
        }

        function pintarResultado() {
            const r = estado.resultado || {};
            const p = estado.pregunta;
            const correctas = (estado.correctas || []).map(i => `${p.opciones[i].letra}: ${escapar(p.opciones[i].texto)}`).join(' · ');
            let tarjeta;
            if (estado.vista_previa) {
                tarjeta = `<div class="ba-resultado nada"><div class="e">👀</div><h2>Así ven el resultado</h2><p>La correcta era<br><b>${correctas}</b></p></div>`;
            } else if (r.acerte) {
                tarjeta = `<div class="ba-resultado bien"><div class="e">🎉</div><h2>¡Correcto!</h2><div class="puntos">+${numero(r.puntos)}</div>${estado.racha >= 2 ? `<div class="racha">🔥 ¡${estado.racha} seguidas!</div>` : ''}</div>`;
            } else if (r.contesto) {
                tarjeta = `<div class="ba-resultado mal"><div class="e">😅</div><h2>¡Uy, casi!</h2><p>La correcta era<br><b>${correctas}</b></p></div>`;
            } else {
                tarjeta = `<div class="ba-resultado nada"><div class="e">⏰</div><h2>No contestaste a tiempo</h2><p>La correcta era<br><b>${correctas}</b></p></div>`;
            }
            escena.innerHTML = `
                <div class="ba-centro">
                    ${tarjeta}
                    ${estado.unido ? `<div class="ba-lugar">Vas en <b>${ordinal(estado.lugar)} lugar</b> con <b>${numero(estado.puntos)}</b> puntos</div>` : ''}
                    <p class="ba-mira">Mira el proyector para ver a los mejores 👀</p>
                </div>`;
            const marca = `${estado.indice}`;
            if (ultimoResultado !== marca) {
                ultimoResultado = marca;
                if (r.acerte) { Sonido.play('exito'); window.NLConfeti?.('monedas'); }
                else if (r.contesto) Sonido.play('error');
            }
        }

        function pintarFinal() {
            const f = estado.final || {};
            if (!f.listo) {
                escena.innerHTML = `<div class="ba-centro"><div class="ba-ilustracion gira">🏆</div><h2>¡Terminó la batalla!</h2><p>Repartiendo premios…</p></div>`;
                return;
            }
            const podio = estado.podio || [];
            const enPodio = f.posicion && f.posicion <= 3;
            const lugar = f.posicion
                ? `<div class="ba-medalla">${enPodio ? MEDALLAS[f.posicion - 1] : '🎖️'}</div><h2>${estado.por_equipos ? 'Tu equipo quedó en' : 'Quedaste en'} ${ordinal(f.posicion)} lugar</h2>`
                : '<div class="ba-medalla">🙂</div><h2>No contestaste ninguna esta vez</h2>';
            escena.innerHTML = `
                <div class="ba-centro ba-final">
                    ${lugar}
                    <div class="ba-stats">
                        <div><b>${numero(f.puntos)}</b><span>puntos</span></div>
                        <div><b>${f.aciertos}/${estado.total}</b><span>aciertos</span></div>
                        ${f.monedas ? `<div class="monedas"><b><i class="bi bi-coin"></i> +${f.monedas}</b><span>monedas</span></div>` : ''}
                        ${f.xp ? `<div class="xp"><b>+${f.xp}</b><span>XP</span></div>` : ''}
                    </div>
                    ${podio.length ? htmlPodio(podio, false) : ''}
                    ${htmlEquipos(estado.equipos, '🛡️ Así quedaron los equipos')}
                    <a href="${urls.urlMapa}" class="g-btn azul mt-3"><i class="bi bi-map-fill"></i> Volver al mapa</a>
                </div>`;
            if (!celebrado) {
                celebrado = true;
                if (enPodio) { Sonido.play('nivel'); confetiPodio(); }
                else if (f.monedas) Sonido.play('moneda');
            }
        }

        function reloj() {
            if (estado.estado === 'pregunta' && (estado.unido || estado.vista_previa)) {
                const capa = $('[data-prep]', escena);
                const prep = faltaPreparar();
                if (capa) {
                    capa.classList.toggle('visible', prep > 0);
                    if (prep > 0) {
                        const n = Math.ceil(prep / 1000);
                        const el = $('[data-prep-n]', escena);
                        if (el.textContent !== String(n)) { el.textContent = n; Sonido.play('tecla'); }
                    }
                }
                const barra = $('[data-barra-tiempo]', escena);
                if (barra && prep <= 0) {
                    const resta = faltaContestar();
                    barra.style.width = (resta * 100 / (estado.segundos * 1000)) + '%';
                    barra.classList.toggle('urgente', resta < 5000);
                    $('[data-seg]', escena).textContent = `${Math.ceil(resta / 1000)} s`;
                    if (resta <= 0 && estado.mi_respuesta == null) {
                        const espera = $('[data-espera]', escena);
                        if (espera && espera.hidden) {
                            espera.hidden = false;
                            espera.innerHTML = '<span class="e">⏰</span> ¡Se acabó el tiempo!';
                            $$('[data-op]', escena).forEach(b => { b.disabled = true; b.classList.add('apagada'); });
                        }
                    }
                }
            }
            requestAnimationFrame(reloj);
        }

        pintar();
        requestAnimationFrame(reloj);
        consultar({
            url: urls.urlEstado,
            ficha: () => estado.ficha,
            intervalo: () => (estado.estado === 'nada' || (estado.estado === 'final' && estado.final?.listo) ? 4000 : 1000),
            aplicar: datos => {
                if (datos.salir) { location.href = urls.urlMapa; return; }
                if (datos.cambio && datos.estado) aplicar(datos.estado);
            },
            alFallar: () => aviso('Se perdió la conexión… reintentando', 'error'),
            alVolver: () => aviso('¡Conectado otra vez!'),
        });
    }

    if (raiz.dataset.modo === 'proyector') iniciarProyector();
    else iniciarAlumno();
})();

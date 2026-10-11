/* =========================================================
   NEXT-LEVEL · Modo clase (celular / tablet del profesor)
   ========================================================= */
(function () {
    'use strict';
    const raiz = document.getElementById('modo-clase');
    if (!raiz) return;

    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
    const espera = ms => new Promise(r => setTimeout(r, ms));
    const toast = (texto, icono = 'success') => window.PToast && window.PToast(texto, icono);
    const claseId = raiz.dataset.clase;

    async function post(url, datos) {
        const body = new FormData();
        Object.entries(datos).forEach(([k, v]) => {
            if (Array.isArray(v)) v.forEach(x => body.append(k, x)); else body.append(k, v);
        });
        const r = await fetch(url, {
            method: 'POST', body,
            headers: { 'X-CSRFToken': $('[name=csrfmiddlewaretoken]').value, 'X-Requested-With': 'XMLHttpRequest' },
        });
        if (!r.ok) throw new Error('Error ' + r.status);
        return r.json();
    }

    // ---------- Sonidos ----------
    const Sonido = (() => {
        let ctx = null;
        let activo = true;
        try { activo = localStorage.getItem('nl-sonido-profe') !== 'off'; } catch (e) { /* sin almacenamiento */ }
        function tono(f, dur, tipo = 'triangle', vol = 0.07, retraso = 0) {
            const t = ctx.currentTime + retraso;
            const o = ctx.createOscillator();
            const g = ctx.createGain();
            o.type = tipo;
            o.frequency.setValueAtTime(f, t);
            g.gain.setValueAtTime(0.0001, t);
            g.gain.exponentialRampToValueAtTime(vol, t + 0.01);
            g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
            o.connect(g).connect(ctx.destination);
            o.start(t);
            o.stop(t + dur + 0.02);
        }
        const efectos = {
            pos: () => { tono(784, 0.12); tono(1175, 0.25, 'triangle', 0.07, 0.09); },
            neg: () => { tono(330, 0.14, 'sine', 0.08); tono(262, 0.25, 'sine', 0.08, 0.12); },
            equipo: () => [523, 659, 784].forEach((f, i) => tono(f, 0.16, 'square', 0.04, i * 0.08)),
            tick: () => tono(1200, 0.03, 'square', 0.025),
            azar: () => [523, 784, 1047].forEach((f, i) => tono(f, 0.18, 'triangle', 0.07, i * 0.1)),
            meta: () => [392, 523, 659, 784, 1047, 1319].forEach((f, i) => tono(f, 0.22, 'square', 0.04, i * 0.09)),
        };
        return {
            play(n) {
                if (!activo || !efectos[n]) return;
                try {
                    ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
                    if (ctx.state === 'suspended') ctx.resume();
                    efectos[n]();
                } catch (e) { /* sin audio */ }
            },
            alternar() {
                activo = !activo;
                try { localStorage.setItem('nl-sonido-profe', activo ? 'on' : 'off'); } catch (e) { /* nada */ }
                return activo;
            },
            get activo() { return activo; },
        };
    })();
    const textoSonido = $('[data-texto-sonido]');
    if (textoSonido) textoSonido.textContent = Sonido.activo ? 'Silenciar sonidos' : 'Activar sonidos';

    // ---------- Estado ----------
    let seleccionando = false;
    const seleccion = new Set();
    let objetivo = null;
    let deshacer = null;
    let elegidoAzar = null;
    const hojaEl = $('#mc-hoja');
    const hoja = bootstrap.Offcanvas.getOrCreateInstance(hojaEl);
    const tarjetas = () => $$('.mc-alumno');
    const visibles = () => tarjetas().filter(t => !t.classList.contains('oculto'));
    const tarjetaDe = id => $(`.mc-alumno[data-id="${id}"]`);
    const equipoDe = id => $(`.mc-equipo[data-equipo-id="${id}"]`);

    // ---------- Vista alumnos / equipos ----------
    function mostrarVista(vista) {
        $$('[data-vista]').forEach(b => b.classList.toggle('activo', b.dataset.vista === vista));
        $$('[data-panel]').forEach(p => p.classList.toggle('d-none', p.dataset.panel !== vista));
        if (vista !== 'alumnos') activarSeleccion(false);
    }
    $$('[data-vista]').forEach(btn => btn.addEventListener('click', () => mostrarVista(btn.dataset.vista)));

    $$('[data-filtro-equipo]').forEach(chip => chip.addEventListener('click', () => {
        $$('[data-filtro-equipo]').forEach(c => c.classList.toggle('activo', c === chip));
        const filtro = chip.dataset.filtroEquipo;
        tarjetas().forEach(t => t.classList.toggle('oculto', !!filtro && t.dataset.equipo !== filtro));
    }));

    // ---------- Selección múltiple ----------
    function actualizarBarra() {
        $('#mc-seleccion').classList.toggle('visible', seleccionando);
        $('[data-total-seleccion]').textContent = seleccion.size;
        $('[data-accion="premiar-seleccion"]').disabled = !seleccion.size;
    }
    function activarSeleccion(activar) {
        seleccionando = activar;
        raiz.classList.toggle('seleccionando', activar);
        $('[data-accion="seleccionar"]')?.classList.toggle('activo', activar);
        if (!activar) {
            seleccion.clear();
            tarjetas().forEach(t => t.classList.remove('elegido'));
        }
        actualizarBarra();
    }
    function alternarTarjeta(t, forzar) {
        const id = t.dataset.id;
        const elegir = forzar ?? !seleccion.has(id);
        if (elegir) seleccion.add(id); else seleccion.delete(id);
        t.classList.toggle('elegido', elegir);
        actualizarBarra();
    }

    let temporizador = null;
    let presionLarga = false;
    tarjetas().forEach(t => {
        t.addEventListener('pointerdown', () => {
            presionLarga = false;
            temporizador = setTimeout(() => {
                presionLarga = true;
                if (!seleccionando) activarSeleccion(true);
                alternarTarjeta(t, true);
                if (navigator.vibrate) navigator.vibrate(25);
            }, 480);
        });
        ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev => t.addEventListener(ev, () => clearTimeout(temporizador)));
        t.addEventListener('contextmenu', e => e.preventDefault());
        t.addEventListener('click', () => {
            if (presionLarga) { presionLarga = false; return; }
            if (seleccionando) alternarTarjeta(t);
            else abrirHoja({ tipo: 'alumnos', ids: [t.dataset.id] });
        });
    });

    $$('.mc-equipo').forEach(card => card.addEventListener('click', () => {
        abrirHoja({ tipo: 'equipo', equipoId: card.dataset.equipoId, ids: card.dataset.miembros.split(',').filter(Boolean) });
    }));

    // ---------- Hoja de comportamientos ----------
    function mostrarTab(tab) {
        $$('[data-tab-conducta]').forEach(b => b.classList.toggle('activo', b.dataset.tabConducta === tab));
        $$('[data-lista-conducta]').forEach(l => l.classList.toggle('d-none', l.dataset.listaConducta !== tab));
    }
    $$('[data-tab-conducta]').forEach(b => b.addEventListener('click', () => mostrarTab(b.dataset.tabConducta)));

    function abrirHoja(obj) {
        objetivo = obj;
        const avatares = $('[data-hoja-avatares]');
        avatares.replaceChildren();
        let titulo;
        let sub;
        if (obj.tipo === 'equipo') {
            const card = equipoDe(obj.equipoId);
            const escudo = document.createElement('span');
            escudo.className = 'grande';
            escudo.textContent = card.querySelector('.e').textContent;
            avatares.appendChild(escudo);
            titulo = card.dataset.nombre;
            sub = `${obj.ids.length} integrantes · ${card.querySelector('[data-equipo-total]').textContent} pts`;
        } else {
            const cards = obj.ids.map(tarjetaDe).filter(Boolean);
            cards.slice(0, 5).forEach(c => {
                const img = document.createElement('img');
                img.src = c.dataset.avatar;
                img.alt = '';
                avatares.appendChild(img);
            });
            titulo = cards.length === 1 ? cards[0].dataset.nombre : (obj.todos ? 'Toda la clase' : `${cards.length} alumnos`);
            sub = cards.length === 1 ? '¿Qué quieres reconocer?'
                : cards.slice(0, 4).map(c => c.dataset.nombre).join(', ') + (cards.length > 4 ? '…' : '');
        }
        $('[data-hoja-titulo]').textContent = titulo;
        $('[data-hoja-sub]').textContent = sub;
        $('[data-solo-equipo]').classList.toggle('d-none', obj.tipo !== 'equipo');
        mostrarTab('pos');
        hoja.show();
    }

    // ---------- Resultados en pantalla ----------
    function flotar(elemento, texto, positivo) {
        if (!elemento) return;
        const f = document.createElement('span');
        f.className = 'mc-flotante' + (positivo ? '' : ' neg');
        f.textContent = texto;
        elemento.appendChild(f);
        elemento.classList.remove('pulso');
        void elemento.offsetWidth;
        elemento.classList.add('pulso');
        setTimeout(() => f.remove(), 1400);
    }

    function contarHoy(id, positivo, delta) {
        const t = tarjetaDe(id);
        if (!t) return;
        const hoy = t.querySelector('.hoy');
        const el = hoy.querySelector(positivo ? '[data-hoy-pos]' : '[data-hoy-neg]');
        const actual = Math.max(0, (parseInt(el.textContent.replace(/\D/g, ''), 10) || 0) + delta);
        el.textContent = actual ? (positivo ? `+${actual}` : ` −${actual}`) : '';
        hoy.classList.toggle('d-none', !hoy.textContent.trim());
    }

    function reordenarEquipos() {
        const contenedor = $('.mc-equipos');
        if (!contenedor) return;
        const cards = $$('.mc-equipo', contenedor);
        cards.sort((a, b) => parseInt(b.querySelector('[data-equipo-total]').textContent, 10)
            - parseInt(a.querySelector('[data-equipo-total]').textContent, 10));
        cards.forEach((card, i) => { card.querySelector('.pos').textContent = `#${i + 1}`; contenedor.appendChild(card); });
    }

    function celebrarMeta(card) {
        Sonido.play('meta');
        if (typeof window.confetti === 'function') {
            window.confetti({ particleCount: 160, spread: 100, origin: { y: 0.6 } });
            setTimeout(() => window.confetti({ particleCount: 90, spread: 120, origin: { y: 0.4 } }), 300);
        }
        toast(`🎉 ¡Meta del grupo cumplida: ${card.querySelector('.t').textContent}!`);
    }

    function aplicarEstado(r) {
        Object.entries(r.alumnos || {}).forEach(([id, d]) => {
            const el = tarjetaDe(id)?.querySelector('[data-monedas]');
            if (el) el.textContent = d.monedas;
        });
        Object.entries(r.equipos || {}).forEach(([id, total]) => {
            const el = equipoDe(id)?.querySelector('[data-equipo-total]');
            if (el) el.textContent = total;
        });
        reordenarEquipos();
        (r.metas || []).forEach(m => {
            const card = $(`.mc-meta[data-meta="${m.id}"]`);
            if (!card) return;
            card.querySelector('[data-meta-valor]').textContent = m.valor;
            card.querySelector('[data-meta-barra]').style.width = m.pct + '%';
            if (m.completada && !card.classList.contains('lograda')) {
                card.classList.add('lograda');
                $$('[data-meta-delta]', card).forEach(b => b.remove());
                celebrarMeta(card);
            }
        });
    }

    // ---------- Aviso con Deshacer ----------
    const aviso = $('#mc-aviso');
    let temporizadorAviso = null;
    function mostrarAviso(texto, accionDeshacer) {
        deshacer = accionDeshacer;
        $('[data-aviso-texto]').textContent = texto;
        $('[data-accion="deshacer"]').classList.toggle('d-none', !accionDeshacer);
        aviso.classList.add('visible');
        clearTimeout(temporizadorAviso);
        temporizadorAviso = setTimeout(() => { aviso.classList.remove('visible'); deshacer = null; }, 10000);
    }

    async function ejecutarDeshacer() {
        const accion = deshacer;
        if (!accion) return;
        deshacer = null;
        aviso.classList.remove('visible');
        try {
            if (accion.tipo === 'conducta') {
                const r = await post(raiz.dataset.urlDeshacer, { clase: claseId, registros: accion.registros });
                aplicarEstado(r);
                accion.alumnos.forEach(id => contarHoy(id, accion.positivo, -1));
            } else {
                const r = await post(raiz.dataset.urlEquipo, { equipo: accion.equipoId, puntos: -accion.puntos, motivo: 'Se deshizo' });
                aplicarEstado(r);
            }
            toast('Listo, se deshizo', 'info');
        } catch (e) { toast('No se pudo deshacer', 'error'); }
    }

    // ---------- Aplicar un comportamiento ----------
    $$('[data-comportamiento]').forEach(btn => btn.addEventListener('click', async () => {
        if (!objetivo || !objetivo.ids.length) { toast('No hay alumnos para premiar', 'warning'); return; }
        const botones = $$('[data-comportamiento]');
        botones.forEach(b => { b.disabled = true; });
        try {
            const r = await post(raiz.dataset.urlConducta, {
                clase: claseId, comportamiento: btn.dataset.comportamiento, alumnos: objetivo.ids,
            });
            hoja.hide();
            const c = r.comportamiento;
            Sonido.play(c.positivo ? 'pos' : 'neg');
            aplicarEstado(r);
            const ids = Object.keys(r.aplicados);
            ids.forEach(id => {
                const v = r.aplicados[id];
                const texto = v.monedas ? `${c.icono} ${v.monedas > 0 ? '+' : ''}${v.monedas}` : `${c.icono} +${v.xp} XP`;
                flotar(tarjetaDe(id), texto, c.positivo);
                contarHoy(id, c.positivo, 1);
            });
            if (objetivo.tipo === 'equipo') flotar(equipoDe(objetivo.equipoId), `${c.icono} ×${ids.length}`, c.positivo);
            const quien = ids.length === 1 ? (tarjetaDe(ids[0])?.dataset.nombre || '1 alumno') : `${ids.length} alumnos`;
            mostrarAviso(`${c.icono} ${c.nombre} · ${quien}`, { tipo: 'conducta', registros: r.registros, alumnos: ids, positivo: c.positivo });
            if (seleccionando) activarSeleccion(false);
        } catch (e) {
            toast('No se pudo guardar. Revisa tu conexión.', 'error');
        } finally {
            botones.forEach(b => { b.disabled = false; });
        }
    }));

    // ---------- Puntos directos al equipo ----------
    $$('[data-puntos]').forEach(btn => btn.addEventListener('click', async () => {
        if (!objetivo || objetivo.tipo !== 'equipo') return;
        const puntos = parseInt(btn.dataset.puntos, 10);
        try {
            const r = await post(raiz.dataset.urlEquipo, { equipo: objetivo.equipoId, puntos, motivo: 'Puntos del profesor' });
            hoja.hide();
            Sonido.play(puntos > 0 ? 'equipo' : 'neg');
            aplicarEstado(r);
            const card = equipoDe(objetivo.equipoId);
            flotar(card, `${puntos > 0 ? '+' : ''}${puntos} pts`, puntos > 0);
            mostrarAviso(`${card.dataset.nombre} · ${puntos > 0 ? '+' : ''}${puntos} pts`, { tipo: 'equipo', equipoId: objetivo.equipoId, puntos });
        } catch (e) { toast('No se pudo guardar', 'error'); }
    }));

    // ---------- Metas con avance manual ----------
    $$('[data-meta-delta]').forEach(btn => btn.addEventListener('click', async () => {
        const card = btn.closest('.mc-meta');
        try {
            const r = await post(raiz.dataset.urlMeta, { meta: card.dataset.meta, delta: btn.dataset.metaDelta });
            aplicarEstado(r);
            if (parseInt(btn.dataset.metaDelta, 10) > 0) Sonido.play('pos');
        } catch (e) { toast('No se pudo actualizar la meta', 'error'); }
    }));

    // ---------- Alumno al azar ----------
    const overlayAzar = $('#mc-azar');
    const claveAzar = `nl-azar-${claseId}`;
    async function elegirAlAzar() {
        overlayAzar.hidden = true;
        mostrarVista('alumnos');
        activarSeleccion(false);
        let usados = [];
        try { usados = JSON.parse(sessionStorage.getItem(claveAzar) || '[]'); } catch (e) { usados = []; }
        let candidatos = visibles().filter(t => !usados.includes(t.dataset.id));
        if (!candidatos.length) { usados = []; candidatos = visibles(); }
        if (!candidatos.length) return;

        let actual = null;
        const pasos = Math.min(22, 10 + candidatos.length);
        for (let i = 0; i < pasos; i++) {
            const siguiente = candidatos[Math.floor(Math.random() * candidatos.length)];
            actual?.classList.remove('destacado');
            siguiente.classList.add('destacado');
            actual = siguiente;
            Sonido.play('tick');
            await espera(55 + i * i * 1.8);
        }
        usados.push(actual.dataset.id);
        try { sessionStorage.setItem(claveAzar, JSON.stringify(usados)); } catch (e) { /* nada */ }
        setTimeout(() => actual.classList.remove('destacado'), 1500);
        elegidoAzar = actual.dataset.id;
        $('[data-azar-avatar]').src = actual.dataset.avatar;
        $('[data-azar-nombre]').textContent = actual.dataset.nombre;
        const restantes = candidatos.length - 1;
        $('[data-azar-restantes]').textContent = restantes ? `Faltan ${restantes} por pasar` : '¡Ya pasaron todos! La siguiente vuelta empieza de nuevo.';
        overlayAzar.hidden = false;
        Sonido.play('azar');
        if (typeof window.confetti === 'function') window.confetti({ particleCount: 60, spread: 70, origin: { y: 0.55 } });
    }
    overlayAzar.addEventListener('click', e => { if (e.target === overlayAzar) overlayAzar.hidden = true; });

    // ---------- Modo enfoque ----------
    let botonSalirEnfoque = null;
    function alternarEnfoque(forzar) {
        const activar = forzar ?? !document.body.classList.contains('modo-enfoque');
        document.body.classList.toggle('modo-enfoque', activar);
        if (activar) {
            if (!botonSalirEnfoque) {
                botonSalirEnfoque = document.createElement('button');
                botonSalirEnfoque.type = 'button';
                botonSalirEnfoque.className = 'p-btn sm';
                botonSalirEnfoque.style.cssText = 'position:fixed;top:.75rem;right:.75rem;z-index:1030';
                botonSalirEnfoque.innerHTML = '<i class="bi bi-fullscreen-exit"></i> Salir';
                botonSalirEnfoque.addEventListener('click', () => alternarEnfoque(false));
                document.body.appendChild(botonSalirEnfoque);
            }
            botonSalirEnfoque.hidden = false;
            document.documentElement.requestFullscreen?.().catch(() => {});
        } else {
            if (botonSalirEnfoque) botonSalirEnfoque.hidden = true;
            if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {});
        }
    }
    document.addEventListener('fullscreenchange', () => {
        if (!document.fullscreenElement && document.body.classList.contains('modo-enfoque')) alternarEnfoque(false);
    });

    // ---------- Botones generales ----------
    document.addEventListener('click', e => {
        const btn = e.target.closest('[data-accion]');
        if (!btn) return;
        const accion = btn.dataset.accion;
        if (accion === 'seleccionar') { mostrarVista('alumnos'); activarSeleccion(!seleccionando); }
        else if (accion === 'todos') {
            const ids = visibles().map(t => t.dataset.id);
            if (!ids.length) { toast('No hay alumnos en esta vista', 'warning'); return; }
            abrirHoja({ tipo: 'alumnos', ids, todos: ids.length === tarjetas().length });
        }
        else if (accion === 'todos-seleccion') visibles().forEach(t => alternarTarjeta(t, true));
        else if (accion === 'cancelar-seleccion') activarSeleccion(false);
        else if (accion === 'premiar-seleccion') abrirHoja({ tipo: 'alumnos', ids: [...seleccion] });
        else if (accion === 'deshacer') ejecutarDeshacer();
        else if (accion === 'azar') elegirAlAzar();
        else if (accion === 'azar-cerrar') overlayAzar.hidden = true;
        else if (accion === 'azar-premiar') { overlayAzar.hidden = true; abrirHoja({ tipo: 'alumnos', ids: [elegidoAzar] }); }
        else if (accion === 'enfoque') alternarEnfoque();
        else if (accion === 'sonido') {
            const activo = Sonido.alternar();
            if (textoSonido) textoSonido.textContent = activo ? 'Silenciar sonidos' : 'Activar sonidos';
            toast(activo ? 'Sonidos activados' : 'Sonidos silenciados', 'info');
        }
    });
})();

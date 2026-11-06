// Radar del grupo (vista de alumno del profe): abre un panel flotante con el avance de una misión.
// Cada botón con data-radar="m123" muestra el contenido de <template id="radar-m123">.
(function () {
    const radar = document.getElementById('radar-grupo');
    if (!radar) return;
    const cuerpo = radar.querySelector('.radar-cuerpo');
    let actual = null;
    let temporizador = null;

    function marcar(origen) {
        document.querySelectorAll('.nodo-caja.seleccionada').forEach((caja) => caja.classList.remove('seleccionada'));
        const caja = origen && origen.closest('.nodo-caja');
        if (caja) caja.classList.add('seleccionada');
    }

    function abrir(id, origen) {
        const plantilla = document.getElementById('radar-' + id);
        if (!plantilla) return;
        clearTimeout(temporizador);
        cuerpo.replaceChildren(plantilla.content.cloneNode(true));
        cuerpo.scrollTop = 0;
        radar.hidden = false;
        requestAnimationFrame(() => radar.classList.add('abierto'));
        marcar(origen);
        actual = id;
    }

    function cerrar() {
        radar.classList.remove('abierto');
        marcar(null);
        actual = null;
        temporizador = setTimeout(() => { radar.hidden = true; }, 200);
    }

    document.addEventListener('click', (evento) => {
        const boton = evento.target.closest('[data-radar]');
        if (boton) {
            evento.preventDefault();
            if (actual === boton.dataset.radar) cerrar();
            else abrir(boton.dataset.radar, boton);
            return;
        }
        if (actual && !radar.contains(evento.target)) cerrar();
    });
    radar.querySelector('.radar-cerrar').addEventListener('click', cerrar);
    document.addEventListener('keydown', (evento) => {
        if (evento.key === 'Escape' && actual) cerrar();
    });
})();

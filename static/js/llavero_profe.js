// Tabla de accesos del llavero de apps (panel del profe):
// pegar una columna (o dos) desde Excel en una casilla la reparte hacia abajo, mostrar u ocultar contraseñas
// y avisar si hay cambios sin guardar.
(function () {
    const form = document.querySelector('[data-accesos]');
    if (!form) return;
    const filas = [...form.querySelectorAll('tr[data-fila]')];
    const celdasDe = fila => [...fila.querySelectorAll('input.celda')];
    const contador = form.querySelector('[data-contador-listos]');
    const estado = form.querySelector('[data-estado-cambios]');
    const aviso = form.querySelector('[data-aviso-pegado]');
    let cambios = false;
    let enviando = false;

    form.querySelectorAll('input').forEach(input => { input.dataset.original = input.value; });

    function actualizar() {
        let listos = 0;
        filas.forEach(fila => {
            const lleno = celdasDe(fila).some(c => c.value.trim());
            if (lleno) listos += 1;
            fila.querySelector('.marca-lista')?.classList.toggle('d-none', !lleno);
        });
        if (contador) contador.textContent = listos;
        cambios = [...form.querySelectorAll('input[data-original]')].some(i => i.value !== i.dataset.original);
        form.querySelectorAll('input.celda').forEach(i => i.classList.toggle('cambiada', i.value !== i.dataset.original));
        if (estado) {
            estado.textContent = cambios ? 'Tienes cambios sin guardar' : 'Sin cambios';
            estado.classList.toggle('hay-cambios', cambios);
        }
    }

    function avisar(texto, advertencia) {
        if (!aviso) return;
        aviso.textContent = texto;
        aviso.classList.toggle('advertencia', !!advertencia);
        aviso.classList.remove('d-none');
    }

    form.addEventListener('input', actualizar);

    // Pegar desde Excel: cada renglón va a un alumno y cada columna (separada por tabulador) a una casilla
    form.addEventListener('paste', e => {
        const celda = e.target.closest('input.celda');
        if (!celda) return;
        const texto = (e.clipboardData || window.clipboardData).getData('text') || '';
        const limpio = texto.replace(/\r/g, '').replace(/\n+$/, '');
        if (!/[\n\t]/.test(limpio)) return;    // un solo dato: se pega normal
        e.preventDefault();
        const renglones = limpio.split('\n').map(r => r.split('\t'));
        const filaInicio = filas.indexOf(celda.closest('tr'));
        const colInicio = celdasDe(filas[filaInicio]).indexOf(celda);
        let usados = 0;
        renglones.forEach((valores, i) => {
            const fila = filas[filaInicio + i];
            if (!fila) return;
            usados += 1;
            const celdas = celdasDe(fila);
            valores.forEach((valor, j) => {
                const destino = celdas[colInicio + j];
                if (destino) destino.value = valor.trim();
            });
        });
        actualizar();
        const sobran = renglones.length - usados;
        if (sobran > 0) {
            avisar(`Se pegaron ${usados} renglones. Sobraron ${sobran}: revisa que tu lista tenga los mismos alumnos y en el mismo orden.`, true);
        } else {
            avisar(`Se pegaron ${usados} renglones. Revisa que cada dato quedó con su alumno y presiona «Guardar».`);
        }
    });

    // Mostrar u ocultar todas las contraseñas (por si la pantalla está proyectada)
    const boton = form.querySelector('[data-mostrar-secretos]');
    if (boton) {
        const texto = boton.querySelector('span');
        const original = texto.textContent;
        boton.addEventListener('click', () => {
            const mostrar = boton.getAttribute('aria-pressed') !== 'true';
            form.querySelectorAll('input.secreto').forEach(i => { i.type = mostrar ? 'text' : 'password'; });
            boton.setAttribute('aria-pressed', mostrar ? 'true' : 'false');
            boton.querySelector('i').className = mostrar ? 'bi bi-eye-slash' : 'bi bi-eye';
            texto.textContent = mostrar ? original.replace('Mostrar', 'Ocultar') : original;
        });
    }

    // Enter en una casilla baja a la de abajo (como en Excel) en lugar de enviar el formulario
    form.addEventListener('keydown', e => {
        const celda = e.target.closest('input.celda');
        if (!celda || e.key !== 'Enter') return;
        e.preventDefault();
        const fila = filas.indexOf(celda.closest('tr'));
        const columna = celdasDe(filas[fila]).indexOf(celda);
        const siguiente = filas[fila + (e.shiftKey ? -1 : 1)];
        if (siguiente) celdasDe(siguiente)[columna]?.focus();
    });

    form.addEventListener('submit', () => { enviando = true; });
    window.addEventListener('beforeunload', e => {
        if (cambios && !enviando) { e.preventDefault(); e.returnValue = ''; }
    });
    actualizar();
})();

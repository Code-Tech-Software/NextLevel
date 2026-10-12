# forms.py
import re
from collections import OrderedDict

from django import forms
from django.db.models import Max

from . import minijuegos
from .models import (
    Alumno, ArticuloTienda, Clase, Comportamiento, Equipo, Juego, Logro, MetaGrupo, Mision, MisionDiaria, Mundo, Nivel,
)


class ArchivoImagen(forms.ClearableFileInput):
    """Subida de imagen sin el texto técnico de Django; la miniatura la muestra el formulario."""
    template_name = 'widgets/archivo.html'

    def __init__(self, attrs=None):
        super().__init__(attrs={'accept': 'image/*', **(attrs or {})})


class EstiloMixin:
    """Aplica las clases de diseño del panel del profesor a todos los campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput,)):
                widget.attrs.setdefault('class', 'nl-switch')
            elif isinstance(widget, (forms.CheckboxSelectMultiple, forms.RadioSelect)):
                widget.attrs.setdefault('class', 'nl-choice-list')
            elif isinstance(widget, forms.ClearableFileInput) or isinstance(widget, forms.FileInput):
                widget.attrs.setdefault('class', 'nl-file')
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault('class', 'nl-select')
            else:
                widget.attrs.setdefault('class', 'nl-input')


def _opciones_mundos():
    grupos = OrderedDict()
    for mundo in Mundo.objects.select_related('clase').order_by('clase__grado', 'clase__grupo', 'clase_id', 'orden'):
        etiqueta = f'{mundo.clase.nombre} · {mundo.clase.grado} {mundo.clase.grupo}'
        grupos.setdefault(etiqueta, []).append((mundo.id, f'{mundo.get_tema_display().split(" ")[0]} {mundo.nombre}'))
    return [('', 'Selecciona un mundo…')] + list(grupos.items())


def _opciones_niveles():
    grupos = OrderedDict()
    niveles = Nivel.objects.select_related('clase', 'mundo').order_by(
        'clase__grado', 'clase__grupo', 'clase_id', 'mundo__orden', 'mundo_id', 'orden'
    )
    for nivel in niveles:
        mundo = nivel.mundo.nombre if nivel.mundo else 'Sin mundo'
        etiqueta = f'{nivel.clase.nombre} ({nivel.clase.grado} {nivel.clase.grupo}) › {mundo}'
        grupos.setdefault(etiqueta, []).append((nivel.id, nivel.nombre))
    return [('', 'Selecciona un nivel…')] + list(grupos.items())


class ClaseForm(EstiloMixin, forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['nombre', 'grado', 'grupo', 'anio', 'icono', 'color', 'descripcion', 'activa']
        labels = {'anio': 'Año escolar', 'icono': 'Ícono (emoji)', 'descripcion': 'Descripción',
                  'activa': 'Visible en el lobby'}
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Robótica'}),
            'grado': forms.TextInput(attrs={'placeholder': 'Ej. 4°'}),
            'grupo': forms.TextInput(attrs={'placeholder': 'Ej. A'}),
            'descripcion': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Opcional: de qué trata la clase'}),
            'icono': forms.TextInput(attrs={'maxlength': 10, 'placeholder': '🚀'}),
            'color': forms.RadioSelect(),
        }

    def clean_grupo(self):
        return (self.cleaned_data.get('grupo') or '').strip().upper()


class AlumnoForm(EstiloMixin, forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'clases', 'avatar', 'pin', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Ana', 'autocomplete': 'off'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ej. López Pérez', 'autocomplete': 'off'}),
            'clases': forms.CheckboxSelectMultiple(),
            'avatar': ArchivoImagen(),
            'pin': forms.TextInput(attrs={'placeholder': '0000', 'maxlength': '4', 'inputmode': 'numeric',
                                          'autocomplete': 'off', 'pattern': '[0-9]{4}'}),
        }
        labels = {
            'clases': 'Clases a las que pertenece',
            'pin': 'PIN de acceso (4 dígitos)',
            'activo': 'Alumno activo',
        }
        help_texts = {'avatar': 'Opcional. Si no subes uno, se le asigna un robot automático.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clases'].error_messages['required'] = 'Elige al menos una clase.'

    def clean_pin(self):
        pin = (self.cleaned_data.get('pin') or '').strip()
        if not (len(pin) == 4 and pin.isdigit()):
            raise forms.ValidationError('El PIN debe tener exactamente 4 números.')
        return pin


def separar_nombre(linea):
    """'Ana López Pérez' → ('Ana', 'López Pérez'); 'López Pérez, Ana Sofía' → ('Ana Sofía', 'López Pérez')."""
    linea = ' '.join(linea.replace('\t', ' ').split())
    if ',' in linea:
        apellido, nombre = (parte.strip() for parte in linea.split(',', 1))
        if nombre:
            return nombre[:100], apellido[:100]
        linea = apellido
    partes = linea.split(' ')
    return partes[0][:100], ' '.join(partes[1:])[:100]


class AltaMasivaForm(EstiloMixin, forms.Form):
    clase = forms.ModelChoiceField(queryset=Clase.objects.order_by('-activa', 'grado', 'grupo'), label='Clase',
                                   error_messages={'required': 'Elige la clase de estos alumnos.'})
    nombres = forms.CharField(
        label='Lista de alumnos',
        widget=forms.Textarea(attrs={'rows': 9, 'spellcheck': 'false',
                                     'placeholder': 'Un alumno por renglón:\nAna López\nCarlos Pérez Ruiz\nGarcía Torres, María José'}),
        error_messages={'required': 'Pega al menos un nombre.'},
    )
    pin_aleatorio = forms.BooleanField(
        label='Generar un PIN aleatorio para cada alumno', required=False, initial=True,
    )

    def clean_nombres(self):
        lineas = [l for l in self.cleaned_data['nombres'].splitlines() if l.strip()]
        if not lineas:
            raise forms.ValidationError('Pega al menos un nombre.')
        return '\n'.join(lineas)


class MundoForm(EstiloMixin, forms.ModelForm):
    class Meta:
        model = Mundo
        fields = ['clase', 'nombre', 'tema', 'descripcion']
        widgets = {
            'tema': forms.RadioSelect(),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Bosque de los Circuitos'}),
            'descripcion': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Una frase épica para presentar el mundo'}),
        }
        labels = {'tema': 'Tema visual'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clase'].queryset = Clase.objects.order_by('-activa', 'grado', 'grupo')
        self.fields['clase'].empty_label = 'Selecciona una clase…'

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.orden = 9999  # La vista lo acomoda en la posición elegida
        return super().save(commit)


class NivelForm(EstiloMixin, forms.ModelForm):
    mundo = forms.TypedChoiceField(label='Mundo', coerce=int)

    class Meta:
        model = Nivel
        fields = ['mundo', 'nombre', 'recompensa_cofre']
        labels = {'recompensa_cofre': 'Monedas del cofre 🎁'}
        widgets = {'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Nivel 1 · Primeros circuitos'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mundo'].choices = _opciones_mundos()

    def clean_mundo(self):
        try:
            return Mundo.objects.get(pk=self.cleaned_data['mundo'])
        except Mundo.DoesNotExist:
            raise forms.ValidationError('Selecciona un mundo válido.')

    def clean_recompensa_cofre(self):
        monedas = self.cleaned_data.get('recompensa_cofre')
        if monedas is None or monedas < 1:
            raise forms.ValidationError('El cofre debe tener al menos 1 moneda.')
        return monedas

    def save(self, commit=True):
        self.instance.clase = self.cleaned_data['mundo'].clase
        if not self.instance.pk:
            self.instance.orden = 9999  # La vista lo acomoda en la posición elegida
        return super().save(commit)


class MisionForm(EstiloMixin, forms.ModelForm):
    nivel = forms.TypedChoiceField(label='Nivel', coerce=int)

    class Meta:
        model = Mision
        fields = ['nivel', 'nombre', 'descripcion', 'tipo', 'juego', 'imagen', 'codigo', 'link', 'xp_recompensa',
                  'monedas_recompensa', 'es_jefe', 'activa', 'fecha_limite']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Explica la misión a tus alumnos...'}),
            'tipo': forms.Select(attrs={'id': 'selector_tipo_mision'}),
            'imagen': ArchivoImagen(),
            'codigo': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Pega aquí el código base de Arduino...',
                                            'class': 'nl-input nl-code', 'spellcheck': 'false'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://...'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        labels = {
            'xp_recompensa': 'XP',
            'monedas_recompensa': 'Monedas',
            'es_jefe': 'Misión jefe (batalla final)',
            'activa': 'Visible para los alumnos',
            'fecha_limite': 'Fecha límite (opcional)',
            'link': 'Enlace o video de YouTube',
            'imagen': 'Imagen de portada',
            'codigo': 'Código base',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nivel'].choices = _opciones_niveles()
        self.fields['juego'].queryset = Juego.objects.filter(activo=True) | Juego.objects.filter(
            pk=getattr(self.instance, 'juego_id', None))
        self.fields['juego'].empty_label = 'Elige un juego…'
        self.fields['juego'].label = 'Minijuego'

    def clean_nivel(self):
        try:
            return Nivel.objects.select_related('clase').get(pk=self.cleaned_data['nivel'])
        except Nivel.DoesNotExist:
            raise forms.ValidationError('Selecciona un nivel válido.')

    def clean(self):
        datos = super().clean()
        if datos.get('tipo') == 'juego' and not datos.get('juego'):
            self.add_error('juego', 'Elige el minijuego que van a jugar.')
        if datos.get('tipo') != 'juego':
            datos['juego'] = None
        if datos.get('tipo') == 'video' and not datos.get('link'):
            self.add_error('link', 'Pega el enlace del video de YouTube.')
        if datos.get('tipo') == 'link' and not datos.get('link'):
            self.add_error('link', 'Pega el enlace de la página que deben visitar.')
        return datos

    def save(self, commit=True):
        self.instance.clase = self.cleaned_data['nivel'].clase
        return super().save(commit)


class ArticuloTiendaForm(EstiloMixin, forms.ModelForm):
    class Meta:
        model = ArticuloTienda
        fields = ['nombre', 'tipo', 'descripcion', 'costo_monedas', 'imagen', 'stock', 'limite_por_alumno',
                  'nivel_requerido', 'requiere_validacion', 'destacado', 'activo']
        widgets = {
            'tipo': forms.RadioSelect(),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'imagen': ArchivoImagen(),
            'costo_monedas': forms.NumberInput(attrs={'min': 1}),
            'stock': forms.NumberInput(attrs={'min': 0}),
            'limite_por_alumno': forms.NumberInput(attrs={'min': 1}),
            'nivel_requerido': forms.NumberInput(attrs={'min': 1}),
        }
        labels = {
            'tipo': '¿Qué tipo de premio es?',
            'costo_monedas': 'Precio',
            'limite_por_alumno': 'Máximo por alumno',
            'nivel_requerido': 'Nivel mínimo',
            'requiere_validacion': 'Lo entrego yo',
            'destacado': 'Destacar en la vitrina',
            'activo': 'Visible en la tienda',
        }

    def clean(self):
        datos = super().clean()
        imagen = datos.get('imagen')
        if datos.get('tipo') == 'avatar' and not imagen and not (self.instance.pk and self.instance.imagen and imagen is not False):
            self.add_error('imagen', 'Los avatares necesitan una imagen: es lo que verá el alumno en su perfil.')
        if datos.get('costo_monedas') is not None and datos['costo_monedas'] < 1:
            self.add_error('costo_monedas', 'El precio debe ser de al menos 1 moneda.')
        if datos.get('tipo') == 'avatar':
            datos['requiere_validacion'] = False  # los avatares se equipan solos al comprarlos
        return datos


class MisionDiariaForm(EstiloMixin, forms.ModelForm):
    # Objetivos que se cumplen con una sola acción y no necesitan cantidad
    OBJETIVOS_SIN_META = ('login', 'tienda')

    class Meta:
        model = MisionDiaria
        fields = ['titulo', 'descripcion', 'icono', 'objetivo', 'meta', 'recompensa_monedas', 'recompensa_xp',
                  'clase', 'activa']
        widgets = {
            'objetivo': forms.RadioSelect(),
            'meta': forms.NumberInput(attrs={'min': 1}),
            'icono': forms.TextInput(attrs={'maxlength': 10}),
            'recompensa_monedas': forms.NumberInput(attrs={'min': 0}),
            'recompensa_xp': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {
            'titulo': 'Nombre',
            'icono': 'Ícono',
            'objetivo': '¿Qué deben hacer hoy?',
            'meta': 'Meta',
            'recompensa_monedas': 'Monedas',
            'recompensa_xp': 'XP',
            'clase': '¿Para quién?',
            'activa': 'Activa (puede salir en el sorteo de cada día)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meta'].required = False
        self.fields['clase'].empty_label = 'Todas las clases'

    def clean(self):
        datos = super().clean()
        if datos.get('objetivo') in self.OBJETIVOS_SIN_META or not datos.get('meta'):
            datos['meta'] = 1
        return datos


class LogroForm(EstiloMixin, forms.ModelForm):
    class Meta:
        model = Logro
        fields = ['nombre', 'descripcion', 'icono', 'condicion', 'valor', 'rareza', 'recompensa_monedas',
                  'recompensa_xp', 'orden', 'activo']
        widgets = {
            'condicion': forms.RadioSelect(),
            'rareza': forms.RadioSelect(),
            'valor': forms.NumberInput(attrs={'min': 1}),
            'icono': forms.TextInput(attrs={'maxlength': 10}),
            'recompensa_monedas': forms.NumberInput(attrs={'min': 0}),
            'recompensa_xp': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {
            'icono': 'Ícono',
            'condicion': '¿Cómo se gana?',
            'valor': 'Meta',
            'recompensa_monedas': 'Monedas',
            'recompensa_xp': 'XP',
            'activo': 'Activo (los alumnos pueden ganarlo)',
            'orden': 'Orden en la vitrina',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor'].required = False
        self.fields['orden'].required = False

    def clean_valor(self):
        return self.cleaned_data.get('valor') or 1

    def clean_orden(self):
        orden = self.cleaned_data.get('orden')
        if orden:
            return orden
        return self.instance.orden if self.instance.pk else (Logro.objects.aggregate(m=Max('orden'))['m'] or 0) + 1


class OtorgarLogroForm(EstiloMixin, forms.Form):
    logro = forms.ModelChoiceField(queryset=Logro.objects.filter(activo=True), label='Logro')
    alumnos = forms.ModelMultipleChoiceField(
        queryset=Alumno.objects.filter(activo=True).order_by('apellido', 'nombre'),
        widget=forms.CheckboxSelectMultiple(), label='Alumnos',
    )


class EquipoForm(EstiloMixin, forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['clase', 'nombre', 'emoji', 'color']
        labels = {'emoji': 'Escudo (emoji)'}
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Dragones'}),
            'emoji': forms.TextInput(attrs={'maxlength': 10, 'placeholder': '🐉'}),
            'color': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clase'].queryset = Clase.objects.order_by('-activa', 'grado', 'grupo')
        self.fields['clase'].empty_label = 'Selecciona una clase…'

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.orden = Equipo.objects.filter(clase=self.cleaned_data['clase']).count() + 1
        return super().save(commit)


class MetaGrupoForm(EstiloMixin, forms.ModelForm):
    class Meta:
        model = MetaGrupo
        fields = ['clase', 'titulo', 'icono', 'tipo', 'objetivo', 'recompensa', 'monedas_recompensa', 'fecha_limite',
                  'descripcion', 'activa']
        labels = {
            'titulo': 'Nombre de la meta',
            'icono': 'Ícono (emoji)',
            'tipo': '¿Qué cuenta para la meta?',
            'recompensa': 'Premio para el grupo',
            'monedas_recompensa': 'Monedas para cada alumno',
            'fecha_limite': 'Fecha límite (opcional)',
            'descripcion': 'Descripción (opcional)',
            'activa': 'Visible para los alumnos',
        }
        widgets = {
            'tipo': forms.RadioSelect(),
            'titulo': forms.TextInput(attrs={'placeholder': 'Ej. ¡Viernes de película!'}),
            'recompensa': forms.TextInput(attrs={'placeholder': 'Ej. 🍿 Película el viernes'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ej. Si entre todos completan 30 misiones esta semana…'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clase'].queryset = Clase.objects.order_by('-activa', 'grado', 'grupo')
        self.fields['clase'].empty_label = 'Selecciona una clase…'

    def clean_objetivo(self):
        objetivo = self.cleaned_data.get('objetivo')
        if not objetivo:
            raise forms.ValidationError('El objetivo debe ser mayor que cero.')
        return objetivo


class ComportamientoForm(EstiloMixin, forms.ModelForm):
    """Las monedas se escriben siempre en positivo; el signo lo da «suma» o «resta»."""
    polaridad = forms.ChoiceField(choices=[('positivo', 'Suma'), ('negativo', 'Resta')], initial='positivo',
                                  widget=forms.RadioSelect())

    class Meta:
        model = Comportamiento
        fields = ['nombre', 'icono', 'monedas', 'xp', 'activo']
        labels = {'icono': 'Ícono (emoji)', 'xp': 'XP', 'activo': 'Mostrar en el modo clase'}
        widgets = {'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Participación'}),
                   'monedas': forms.NumberInput(attrs={'min': 1}), 'xp': forms.NumberInput(attrs={'min': 0})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and not self.is_bound:
            self.initial['polaridad'] = 'positivo' if self.instance.monedas >= 0 else 'negativo'
            self.initial['monedas'] = abs(self.instance.monedas)

    def clean(self):
        datos = super().clean()
        monedas = datos.get('monedas')
        if monedas is not None:
            if monedas == 0:
                self.add_error('monedas', 'Escribe cuántas monedas da o quita.')
            elif datos.get('polaridad') == 'negativo':
                datos['monedas'] = -abs(monedas)
                datos['xp'] = 0  # Los negativos nunca quitan XP
            else:
                datos['monedas'] = abs(monedas)
        return datos

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.orden = 9999  # La vista lo acomoda en la posición elegida
        return super().save(commit)


def campos_clasifica(cfg):
    """Los grupos del Detective digital como campos del formulario (cat1_nombre, cat1_tarjetas…)."""
    campos = {'tema_clasifica': cfg.get('tema', 'personalizado')}
    for n, categoria in enumerate(cfg['categorias'][:3], start=1):
        campos.update({f'cat{n}_emoji': categoria['emoji'], f'cat{n}_nombre': categoria['nombre'],
                       f'cat{n}_tarjetas': '\n'.join(categoria['tarjetas'])})
    return campos


class JuegoForm(EstiloMixin, forms.ModelForm):
    """El juego guarda su configuración en un JSON; aquí cada ajuste es un campo normal."""
    # Mecanografía de meteoros
    palabras = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'rows': 5, 'spellcheck': 'false', 'placeholder': 'Una palabra por renglón o separadas por comas'}))
    duracion = forms.TypedChoiceField(choices=[(60, '1 minuto'), (90, '1½ minutos'), (120, '2 minutos')],
                                      coerce=int, initial=60, required=False)
    velocidad = forms.ChoiceField(choices=[('lenta', 'Lenta'), ('normal', 'Normal'), ('rapida', 'Rápida')],
                                  initial='normal', required=False)
    vidas = forms.TypedChoiceField(choices=[(3, '3'), (5, '5')], coerce=int, initial=3, required=False)
    meta = forms.IntegerField(min_value=1, max_value=300, required=False)
    acentos_exactos = forms.BooleanField(required=False, label='Exigir acentos y ñ exactos')
    # Teclado misterioso
    conjunto = forms.ChoiceField(choices=[(c, c) for c in minijuegos.CONJUNTOS_TECLAS] + [('personalizado', 'personalizado')],
                                 initial='central', required=False)
    teclas = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={
        'placeholder': 'Ej. ASDF', 'autocomplete': 'off', 'style': 'text-transform:uppercase'}))
    rondas = forms.TypedChoiceField(choices=[(15, '15'), (20, '20'), (30, '30')], coerce=int, initial=20, required=False)
    modo = forms.ChoiceField(choices=[('guiado', 'Guiado'), ('reto', 'Reto')], initial='guiado', required=False)
    # Detective digital: hasta 3 grupos con sus tarjetas
    tema_clasifica = forms.CharField(required=False, widget=forms.HiddenInput())
    cat1_emoji = forms.CharField(required=False, max_length=10)
    cat1_nombre = forms.CharField(required=False, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Ej. Seguro'}))
    cat1_tarjetas = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'spellcheck': 'false', 'placeholder': 'Una tarjeta por renglón'}))
    cat2_emoji = forms.CharField(required=False, max_length=10)
    cat2_nombre = forms.CharField(required=False, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Ej. Peligroso'}))
    cat2_tarjetas = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'spellcheck': 'false', 'placeholder': 'Una tarjeta por renglón'}))
    cat3_emoji = forms.CharField(required=False, max_length=10)
    cat3_nombre = forms.CharField(required=False, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Opcional'}))
    cat3_tarjetas = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'spellcheck': 'false', 'placeholder': 'Una tarjeta por renglón'}))
    rondas_tarjetas = forms.TypedChoiceField(choices=[(10, '10'), (15, '15'), (20, '20')], coerce=int, initial=10, required=False)
    tiempo_tarjeta = forms.TypedChoiceField(choices=[(0, 'Sin límite'), (8, '8 s'), (5, '5 s')], coerce=int, initial=8,
                                            required=False, empty_value=8)
    # Robot programador
    dificultad = forms.ChoiceField(choices=[(d, d) for d in minijuegos.DIFICULTADES_ROBOT], initial='facil', required=False)
    niveles = forms.TypedChoiceField(choices=[(3, '3'), (5, '5'), (8, '8')], coerce=int, initial=5, required=False)
    modo_robot = forms.ChoiceField(choices=[('flechas', 'Flechas'), ('giros', 'Giros')], initial='flechas', required=False)
    bucles = forms.BooleanField(required=False, label='Bloques de repetir 🔁')
    # Atajos ninja
    atajos = forms.MultipleChoiceField(choices=[(k, v[1]) for k, v in minijuegos.ATAJOS.items()], required=False,
                                       widget=forms.CheckboxSelectMultiple())
    rondas_atajos = forms.TypedChoiceField(choices=[(10, '10'), (15, '15'), (20, '20')], coerce=int, initial=10, required=False)
    modo_atajos = forms.ChoiceField(choices=[('aprende', 'Aprende'), ('ninja', 'Ninja')], initial='aprende', required=False)
    # Mensaje secreto
    cifrado = forms.ChoiceField(choices=[(k, v[1]) for k, v in minijuegos.CIFRADOS.items()], initial='simbolos', required=False)
    palabras_mensaje = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'rows': 4, 'spellcheck': 'false', 'placeholder': 'Una palabra por renglón (2 a 12 letras)'}))
    rondas_mensaje = forms.TypedChoiceField(choices=[(5, '5'), (8, '8'), (10, '10')], coerce=int, initial=5, required=False)
    desplazamiento = forms.TypedChoiceField(choices=[(1, '1'), (3, '3'), (5, '5')], coerce=int, initial=3, required=False)
    # Explorador de rutas
    modo_rutas = forms.ChoiceField(choices=[('ruta', 'Sigue la ruta'), ('buscar', 'Búscalo')], initial='ruta', required=False)
    dificultad_rutas = forms.ChoiceField(choices=[(d, d) for d in minijuegos.DIFICULTADES_RUTAS], initial='facil', required=False)
    rondas_rutas = forms.TypedChoiceField(choices=[(5, '5'), (8, '8'), (10, '10')], coerce=int, initial=5, required=False)
    # Copia el formato
    dificultad_formato = forms.ChoiceField(choices=[(d, d) for d in minijuegos.DIFICULTADES_FORMATO], initial='facil',
                                           required=False)
    rondas_formato = forms.TypedChoiceField(choices=[(5, '5'), (8, '8'), (10, '10')], coerce=int, initial=5, required=False)
    frases = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'rows': 4, 'placeholder': 'Opcional: una frase por renglón. Si lo dejas vacío usamos frases de TIC.'}))
    # Ponerlo también en el mapa como misión
    agregar_mapa = forms.BooleanField(required=False)
    nivel_mapa = forms.TypedChoiceField(coerce=int, required=False, empty_value=None, label='Nivel')
    xp_mapa = forms.IntegerField(min_value=0, max_value=1000, initial=50, required=False)
    monedas_mapa = forms.IntegerField(min_value=0, max_value=1000, initial=15, required=False)

    class Meta:
        model = Juego
        fields = ['plantilla', 'nombre', 'descripcion', 'icono', 'en_arcade', 'clase', 'desbloqueo',
                  'monedas_arcade', 'activo']
        widgets = {
            'plantilla': forms.RadioSelect(),
            'desbloqueo': forms.RadioSelect(),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Lluvia de meteoros'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ej. Practica escribiendo las partes de la computadora'}),
            'icono': forms.TextInput(attrs={'maxlength': 10}),
            'monedas_arcade': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {'en_arcade': 'Disponible en el Arcade', 'activo': 'Juego activo',
                  'monedas_arcade': 'Monedas por partida en el Arcade'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clase'].queryset = Clase.objects.order_by('-activa', 'grado', 'grupo')
        self.fields['clase'].empty_label = 'Todas las clases'
        self.fields['clase'].label = 'Arcade de'
        self.fields['nivel_mapa'].choices = _opciones_niveles()
        if self.instance.pk and not self.is_bound:
            cfg = minijuegos.configuracion(self.instance)
            if self.instance.plantilla == 'atajos':
                self.initial.update({'atajos': cfg['atajos'], 'rondas_atajos': cfg['rondas'], 'modo_atajos': cfg['modo']})
            elif self.instance.plantilla == 'mensaje':
                self.initial.update({'cifrado': cfg['cifrado'], 'palabras_mensaje': '\n'.join(cfg['palabras']),
                                     'rondas_mensaje': cfg['rondas'], 'desplazamiento': cfg['desplazamiento']})
            elif self.instance.plantilla == 'rutas':
                self.initial.update({'modo_rutas': cfg['modo'], 'dificultad_rutas': cfg['dificultad'], 'rondas_rutas': cfg['rondas']})
            elif self.instance.plantilla == 'formato':
                propias = (self.instance.configuracion or {}).get('frases') or []
                self.initial.update({'dificultad_formato': cfg['dificultad'], 'rondas_formato': cfg['rondas'],
                                     'frases': '\n'.join(propias)})
            elif self.instance.plantilla == 'clasifica':
                self.initial.update(campos_clasifica(cfg))
                self.initial.update({'rondas_tarjetas': cfg['rondas'], 'tiempo_tarjeta': cfg['tiempo']})
            elif self.instance.plantilla == 'robot':
                self.initial.update({'dificultad': cfg['dificultad'], 'niveles': cfg['niveles'], 'modo_robot': cfg['modo'],
                                     'bucles': cfg['bucles']})
            elif self.instance.plantilla == 'teclado':
                self.initial.update({k: cfg[k] for k in ('conjunto', 'rondas', 'modo')})
                self.initial['teclas'] = cfg['teclas'] if cfg['conjunto'] == 'personalizado' else ''
            else:
                self.initial.update({k: cfg[k] for k in ('duracion', 'velocidad', 'vidas', 'meta')})
                self.initial['palabras'] = '\n'.join(cfg['palabras'])
                self.initial['acentos_exactos'] = cfg['acentos'] == 'exactos'

    def clean(self):
        datos = super().clean()
        if datos.get('plantilla') == 'atajos':
            if len(datos.get('atajos') or []) < 2:
                self.add_error('atajos', 'Elige al menos 2 atajos.')
            self.configuracion = {'atajos': datos.get('atajos') or [], 'rondas': datos.get('rondas_atajos') or 10,
                                  'modo': datos.get('modo_atajos') or 'aprende'}
        elif datos.get('plantilla') == 'mensaje':
            crudas = [p for p in re.split(r'[\n,;]+', datos.get('palabras_mensaje') or '') if p.strip()]
            palabras = list(dict.fromkeys(minijuegos.normalizar_secreto(p) for p in crudas))
            largas = [p for p in palabras if len(p) > 12]
            if largas:
                self.add_error('palabras_mensaje', f'Máximo 12 letras por palabra: {", ".join(largas[:3])}.')
            validas = [p for p in palabras if 2 <= len(p) <= 12]
            if len(validas) < 3:
                self.add_error('palabras_mensaje', 'Escribe al menos 3 palabras (de 2 a 12 letras).')
            self.configuracion = {'cifrado': datos.get('cifrado') or 'simbolos', 'palabras': validas,
                                  'rondas': datos.get('rondas_mensaje') or 5, 'desplazamiento': datos.get('desplazamiento') or 3}
        elif datos.get('plantilla') == 'rutas':
            self.configuracion = {'modo': datos.get('modo_rutas') or 'ruta', 'dificultad': datos.get('dificultad_rutas') or 'facil',
                                  'rondas': datos.get('rondas_rutas') or 5}
        elif datos.get('plantilla') == 'formato':
            frases = [' '.join(f.split()) for f in (datos.get('frases') or '').splitlines() if f.strip()]
            if frases and len([f for f in frases if len(f.split()) >= 2]) < 3:
                self.add_error('frases', 'Escribe al menos 3 frases de dos o más palabras (o deja el campo vacío).')
            if any(len(f) > 60 for f in frases):
                self.add_error('frases', 'Cada frase puede tener máximo 60 letras.')
            self.configuracion = {'dificultad': datos.get('dificultad_formato') or 'facil',
                                  'rondas': datos.get('rondas_formato') or 5, 'frases': frases}
        elif datos.get('plantilla') == 'clasifica':
            categorias = []
            for n in (1, 2, 3):
                nombre = ' '.join((datos.get(f'cat{n}_nombre') or '').split())
                tarjetas = [' '.join(t.split()) for t in (datos.get(f'cat{n}_tarjetas') or '').splitlines() if t.strip()]
                if not nombre and not tarjetas:
                    continue
                if not nombre:
                    self.add_error(f'cat{n}_nombre', 'Ponle nombre a este grupo.')
                elif not tarjetas:
                    self.add_error(f'cat{n}_tarjetas', 'Escribe al menos una tarjeta para este grupo.')
                largas = [t for t in tarjetas if len(t) > 70]
                if largas:
                    self.add_error(f'cat{n}_tarjetas', f'Hay tarjetas muy largas (máximo 70 letras): «{largas[0][:30]}…».')
                categorias.append({'nombre': nombre, 'emoji': (datos.get(f'cat{n}_emoji') or '📁').strip(), 'tarjetas': tarjetas})
            if len([c for c in categorias if c['nombre'] and c['tarjetas']]) < 2:
                self.add_error('cat2_nombre', 'Necesitas al menos 2 grupos, cada uno con sus tarjetas.')
            tiempo = datos.get('tiempo_tarjeta')
            self.configuracion = {'tema': datos.get('tema_clasifica') or 'personalizado', 'categorias': categorias,
                                  'rondas': datos.get('rondas_tarjetas') or 10, 'tiempo': 8 if tiempo is None else tiempo}
        elif datos.get('plantilla') == 'robot':
            self.configuracion = {'dificultad': datos.get('dificultad') or 'facil', 'niveles': datos.get('niveles') or 5,
                                  'modo': datos.get('modo_robot') or 'flechas', 'bucles': bool(datos.get('bucles'))}
        elif datos.get('plantilla') == 'teclado':
            conjunto = datos.get('conjunto') or 'central'
            teclas = ''.join(dict.fromkeys(c for c in (datos.get('teclas') or '').upper() if c in minijuegos.TECLAS_VALIDAS))
            if conjunto == 'personalizado' and len(teclas) < 2:
                self.add_error('teclas', 'Escribe al menos 2 letras o números distintos.')
            self.configuracion = {'conjunto': conjunto, 'teclas': teclas if conjunto == 'personalizado' else '',
                                  'rondas': datos.get('rondas') or 20, 'modo': datos.get('modo') or 'guiado'}
        elif datos.get('plantilla') == 'meteoros':
            palabras = []
            for palabra in re.split(r'[\n,;]+', datos.get('palabras') or ''):
                palabra = ' '.join(palabra.split())
                if palabra and palabra.lower() not in (p.lower() for p in palabras):
                    palabras.append(palabra)
            if len(palabras) < 5:
                self.add_error('palabras', 'Escribe al menos 5 palabras distintas.')
            largas = [p for p in palabras if len(p) > 20]
            if largas:
                self.add_error('palabras', f'Estas palabras son muy largas (máximo 20 letras): {", ".join(largas[:3])}.')
            duracion = datos.get('duracion') or 60
            velocidad = datos.get('velocidad') or 'normal'
            self.configuracion = {
                'palabras': palabras, 'duracion': duracion, 'velocidad': velocidad, 'vidas': datos.get('vidas') or 3,
                'meta': datos.get('meta') or minijuegos.meta_sugerida(duracion, velocidad),
                'acentos': 'exactos' if datos.get('acentos_exactos') else 'opcionales',
            }
        if datos.get('agregar_mapa'):
            if not datos.get('nivel_mapa'):
                self.add_error('nivel_mapa', 'Elige en qué nivel del mapa va la misión.')
            elif not Nivel.objects.filter(pk=datos['nivel_mapa']).exists():
                self.add_error('nivel_mapa', 'Selecciona un nivel válido.')
        return datos

    def save(self, commit=True):
        self.instance.configuracion = getattr(self, 'configuracion', self.instance.configuracion)
        return super().save(commit)

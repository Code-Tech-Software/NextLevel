# forms.py
from collections import OrderedDict

from django import forms
from django.db.models import Max

from .models import (
    Alumno, ArticuloTienda, Clase, Comportamiento, Equipo, Logro, MetaGrupo, Mision, MisionDiaria, Mundo, Nivel,
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
        labels = {'anio': 'Año escolar', 'icono': 'Ícono (emoji)', 'descripcion': 'Descripción'}
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Opcional: de qué trata la clase'}),
            'icono': forms.TextInput(attrs={'maxlength': 10, 'placeholder': '🚀'}),
        }


class AlumnoForm(EstiloMixin, forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'clases', 'avatar', 'pin', 'activo']
        widgets = {
            'clases': forms.CheckboxSelectMultiple(),
            'avatar': ArchivoImagen(),
            'pin': forms.TextInput(attrs={'placeholder': '0000', 'maxlength': '4', 'inputmode': 'numeric'}),
        }
        labels = {
            'clases': 'Clases a las que pertenece',
            'pin': 'PIN de acceso (4 dígitos)',
            'activo': 'Alumno activo',
        }
        help_texts = {'avatar': 'Opcional. Si no subes uno, se le asigna un robot automático.'}

    def clean_pin(self):
        pin = (self.cleaned_data.get('pin') or '').strip()
        if not (len(pin) == 4 and pin.isdigit()):
            raise forms.ValidationError('El PIN debe tener exactamente 4 números.')
        return pin


class AltaMasivaForm(EstiloMixin, forms.Form):
    clase = forms.ModelChoiceField(queryset=Clase.objects.all(), label='Clase')
    nombres = forms.CharField(
        label='Lista de alumnos',
        widget=forms.Textarea(attrs={'rows': 10, 'placeholder': 'Un alumno por renglón:\nNombre Apellido\nAna López\nCarlos Pérez Ruiz'}),
        help_text='Escribe un alumno por renglón. La primera palabra es el nombre y el resto el apellido.',
    )
    pin_aleatorio = forms.BooleanField(
        label='Generar un PIN aleatorio para cada alumno', required=False, initial=True,
    )


class MundoForm(EstiloMixin, forms.ModelForm):
    class Meta:
        model = Mundo
        fields = ['clase', 'nombre', 'tema', 'descripcion', 'orden']
        widgets = {
            'tema': forms.RadioSelect(),
            'descripcion': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Una frase épica para presentar el mundo'}),
        }
        labels = {'orden': 'Orden en el mapa', 'tema': 'Tema visual'}


class NivelForm(EstiloMixin, forms.ModelForm):
    mundo = forms.TypedChoiceField(label='Mundo', coerce=int)

    class Meta:
        model = Nivel
        fields = ['mundo', 'nombre', 'orden', 'recompensa_cofre']
        labels = {'recompensa_cofre': 'Monedas del cofre 🎁', 'orden': 'Orden dentro del mundo'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mundo'].choices = _opciones_mundos()

    def clean_mundo(self):
        try:
            return Mundo.objects.get(pk=self.cleaned_data['mundo'])
        except Mundo.DoesNotExist:
            raise forms.ValidationError('Selecciona un mundo válido.')

    def save(self, commit=True):
        self.instance.clase = self.cleaned_data['mundo'].clase
        return super().save(commit)


class MisionForm(EstiloMixin, forms.ModelForm):
    nivel = forms.TypedChoiceField(label='Nivel', coerce=int)

    class Meta:
        model = Mision
        fields = ['nivel', 'nombre', 'descripcion', 'tipo', 'imagen', 'codigo', 'link', 'xp_recompensa',
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

    def clean_nivel(self):
        try:
            return Nivel.objects.select_related('clase').get(pk=self.cleaned_data['nivel'])
        except Nivel.DoesNotExist:
            raise forms.ValidationError('Selecciona un nivel válido.')

    def clean(self):
        datos = super().clean()
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
        fields = ['clase', 'nombre', 'emoji', 'color', 'orden']
        labels = {'emoji': 'Escudo (emoji)', 'orden': 'Orden'}
        widgets = {'emoji': forms.TextInput(attrs={'maxlength': 10, 'placeholder': '🐉'})}


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
        widgets = {'fecha_limite': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}
        help_texts = {'objetivo': 'Solo cuenta lo que pase a partir de que crees la meta.'}


class ComportamientoForm(EstiloMixin, forms.ModelForm):
    class Meta:
        model = Comportamiento
        fields = ['nombre', 'icono', 'monedas', 'xp', 'orden', 'activo']
        labels = {'icono': 'Ícono (emoji)', 'xp': 'XP', 'activo': 'Mostrar en el modo clase'}

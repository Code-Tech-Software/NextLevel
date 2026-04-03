# forms.py
from django import forms
from .models import Alumno, Clase, ArticuloTienda, Mision, Nivel


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'clases', 'avatar', 'pin']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'clases': forms.SelectMultiple(attrs={'class': 'form-select form-select-lg'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'pin': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'placeholder': '0000', 'maxlength': '4'}),
        }
        labels = {
            'clases': 'Asignar a clases (Mantén presionado Ctrl o Cmd para elegir varias)',
            'pin': 'PIN de acceso (4 dígitos)'
        }


class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['nombre', 'grado', 'grupo', 'anio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'grado': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
        }


class ArticuloTiendaForm(forms.ModelForm):
    class Meta:
        model = ArticuloTienda
        fields = ['nombre', 'descripcion', 'costo_monedas', 'imagen', 'requiere_validacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 3}),
            'costo_monedas': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'requiere_validacion': forms.CheckboxInput(attrs={'style': 'width: 1.5em; height: 1.5em; '}),
        }


class MisionForm(forms.ModelForm):
    class Meta:
        model = Mision
        fields = ['clase', 'nivel', 'nombre', 'descripcion', 'tipo', 'imagen', 'codigo', 'link', 'xp_recompensa',
                  'monedas_recompensa', 'orden']
        widgets = {
            'clase': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'nivel': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Explica la misión a tus alumnos...'}),
            'tipo': forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'selector_tipo_mision'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'codigo': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Pega aquí el código base de Arduino...'}),
            'link': forms.URLInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'https://...'}),
            'xp_recompensa': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'monedas_recompensa': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
        }


class NivelForm(forms.ModelForm):
    class Meta:
        model = Nivel
        fields = ['clase', 'nombre', 'orden']
        widgets = {
            'clase': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
        }

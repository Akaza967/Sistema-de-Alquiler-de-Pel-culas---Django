from __future__ import annotations

from datetime import date
from django import forms
from .models import Alquiler, Categoria, Cliente, Pelicula
from django.core.exceptions import ValidationError

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "email", "telefono"]


class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ["titulo", "anio", "categoria", "precio_alquiler"]


class AlquilerCreateForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ["cliente", "pelicula"]


class MarcarPagadoForm(forms.Form):
    fecha_devolucion = forms.DateField(
        required=False,
        label="Fecha de devolución (opcional)",
        widget=forms.DateInput(attrs={"type": "date"}),
    )


class SimularVentasForm(forms.Form):
    numero_ventas = forms.IntegerField(
        min_value=1,
        label="Número de ventas"
    )

    desde = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    hasta = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def clean(self):
        cleaned_data = super().clean()

        desde = cleaned_data.get("desde")
        hasta = cleaned_data.get("hasta")
        numero = cleaned_data.get("numero_ventas")

        # 🔴 Validación 1: fechas correctas
        if desde and hasta:
            if hasta < desde:
                raise ValidationError(
                    "La fecha 'hasta' no puede ser menor que 'desde'."
                )

        # 🔴 Validación 2: límite razonable
        if numero and numero > 1000:
            raise ValidationError(
                "No puedes generar más de 1000 ventas."
            )

        # 🔴 Validación 3: no fechas futuras
        if desde and desde > date.today():
            raise ValidationError(
                "La fecha 'desde' no puede estar en el futuro."
            )

        return cleaned_data


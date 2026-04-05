from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True, unique=True)
    telefono = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre


class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)

    anio = models.PositiveIntegerField(
        validators=[MinValueValidator(1900)],
        verbose_name="Año"
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="peliculas"
    )

    precio_alquiler = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]  # 🔥 mejor que 0
    )

    # ✅ Reto Django #1
    stock = models.IntegerField(default=0)

    class Meta:
        ordering = ["titulo", "anio"]
        unique_together = [("titulo", "anio")]

    def disponible(self):
        return self.stock > 0

    # ✅ Reto Django #23 / #79 (validaciones correctas)
    def clean(self):
        super().clean()

        # 🔴 Stock no puede ser negativo
        if self.stock < 0:
            raise ValidationError({
                'stock': "El stock no puede ser negativo"
            })

        # 🔴 Precio debe ser mayor a 0
        if self.precio_alquiler <= 0:
            raise ValidationError({
                'precio_alquiler': "El precio debe ser mayor a 0"
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # 🔥 ejecuta validaciones siempre
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titulo} ({self.anio})"


class Alquiler(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.PROTECT)

    fecha_alquiler = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)

    pagado = models.BooleanField(default=False)

    def clean(self):
        super().clean()

        # 🔴 Validación 1: no alquilar sin stock
        if self.pelicula and self.pelicula.stock <= 0:
            raise ValidationError("No hay stock disponible para esta película.")

        # 🔴 Validación 2: fechas coherentes
        if self.fecha_devolucion and self.fecha_devolucion < self.fecha_alquiler:
            raise ValidationError(
                "La fecha de devolución no puede ser menor a la de alquiler."
            )

    def save(self, *args, **kwargs):
        # 🔥 Ejecuta validaciones
        self.full_clean()

        # 🔥 Control de stock (solo si es nuevo)
        #if not self.pk:
         #   self.pelicula.stock -= 1
          #  self.pelicula.save()
          #Ya no va en el modelo, ahora lo hace el signal

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente} - {self.pelicula}"

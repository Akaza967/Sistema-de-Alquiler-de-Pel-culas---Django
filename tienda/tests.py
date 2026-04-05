from django.test import TestCase
from .models import Pelicula, Categoria
from decimal import Decimal
from django.core.exceptions import ValidationError
# Create your tests here.
class PeliculaTest(TestCase):

    def test_crear_pelicula(self):
        categoria = Categoria.objects.create(nombre="Acción")

        pelicula = Pelicula.objects.create(
            titulo="Test",
            anio=2020,
            categoria=categoria,
            precio_alquiler=Decimal("10.00"),
            stock=5
        )

        self.assertEqual(pelicula.titulo, "Test")
        self.assertTrue(pelicula.disponible())

class PeliculaValidacionTest(TestCase):

    def test_stock_negativo(self):
        categoria = Categoria.objects.create(nombre="Drama")

        pelicula = Pelicula(
            titulo="Error",
            anio=2020,
            categoria=categoria,
            precio_alquiler=Decimal("10.00"),
            stock=-1
        )

        with self.assertRaises(ValidationError):
            pelicula.full_clean()
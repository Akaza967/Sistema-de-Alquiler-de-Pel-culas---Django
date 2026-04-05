from django.contrib import admin

from .models import Alquiler, Categoria, Cliente, Pelicula


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "descripcion"]
    search_fields = ["nombre"]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "email", "telefono"]
    search_fields = ["nombre", "email"]


@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "anio", "categoria", "precio_alquiler"]
    list_filter = ["categoria", "anio"]
    search_fields = ["titulo"]


@admin.register(Alquiler)
class AlquilerAdmin(admin.ModelAdmin):
    list_display = ("cliente", "pelicula", "fecha_alquiler", "pagado", "precio_pelicula")

    def precio_pelicula(self, obj):
        return obj.pelicula.precio_alquiler

    precio_pelicula.short_description = "Precio"

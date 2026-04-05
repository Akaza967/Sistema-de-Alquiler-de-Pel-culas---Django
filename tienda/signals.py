from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Alquiler

# 🔥 Cuando se crea un alquiler → descuenta stock
@receiver(post_save, sender=Alquiler)
def actualizar_stock(sender, instance, created, **kwargs):
    if created:
        pelicula = instance.pelicula
        pelicula.stock -= 1
        pelicula.save()
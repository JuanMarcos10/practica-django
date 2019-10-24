import datetime
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    nombre = models.CharField(max_length=150);
    slug = models.SlugField(unique=True);

    def __str__(self):
        return self.nombre

class Article(models.Model):
    BORRADOR = 'DRF'
    PUBLICADO = 'PUB'

    ESTADO = [
        [BORRADOR, 'Borrador'],
        [PUBLICADO, 'Publicado']
    ]

    titulo = models.CharField(max_length=150);
    texto_introduccion = models.TextField(null=True, blank=True)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_publicacion = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now())
    estado =  models.CharField(max_length=3, choices=ESTADO, default=BORRADOR)
    usuario = models.ForeignKey(User, related_name='articulos', on_delete=models.CASCADE)
    categoria = models.ForeignKey(Category, related_name='articulos', on_delete=models.CASCADE)
    imagen = models.URLField(default='http://ella.practicalaction.org/wp-content/themes/ella/images/no-photo.png')
    video = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.titulo
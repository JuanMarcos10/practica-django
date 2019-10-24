from rest_framework.serializers import ModelSerializer

from . import models

class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = models.Category
        fields = ['id','nombre','slug']

class ArticleListSerializer(ModelSerializer):

    class Meta:
        model = models.Article
        fields = ['id','titulo','texto_introduccion']

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = models.Article
        fields = ['id',
                  'titulo',
                  'texto_introduccion',
                  'contenido',
                  'fecha_creacion',
                  'fecha_modificacion',
                  'estado',
                  'usuario',
                  'imagen',
                  'video'
                  ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion', 'usuario']
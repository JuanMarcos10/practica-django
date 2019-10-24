from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from articles.models import Article, Category
from articles.permissions import ArticlePermission
from articles.serializers import ArticleListSerializer, ArticleSerializer, CategoryListSerializer


class ArticleFilter(filters.FilterSet):

    class Meta:
        model = Article
        fields = {
            'titulo' : ['contains'],
            'usuario' : ['exact'],
            'fecha_creacion' : ['gte', 'lt', 'contains'],
            'estado' : ['exact']
        }

class ArticleList(object):
    def get_queryset(self):
        queryset = Article.objects.select_related('usuario').order_by('-fecha_modificacion')
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(estado=Article.PUBLICADO)
        elif not self.request.user.is_superuser:
            queryset = queryset.filter(Q(estado=Article.PUBLICADO) | Q(usuario=self.request.user))
        return queryset

class CategoryListView(ListAPIView):

    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    filter_backends = [OrderingFilter]
    ordering_filters = ['nombre']

    def get_serializer_class(self):
        return CategoryListSerializer

class ArticleViewSet(ArticleList, ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Article.objects.all()
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filter_class = ArticleFilter
    ordering_filters = ['id','titulo']

    def get_serializer_class(self):
        return ArticleListSerializer if self.request.method == 'GET' else ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class ArticleDetail(ArticleList, RetrieveUpdateDestroyAPIView):

    permission_classes = [ArticlePermission]

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_update(self, serializer):
        serializer.save(usuario=self.request.user)
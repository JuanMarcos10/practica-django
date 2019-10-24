from django.urls import include, path
from django.contrib import admin

from articles.api_views import ArticleViewSet, ArticleDetail, CategoryListView
from .api import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('articulos/', ArticleViewSet.as_view()),
    path('categorias/', CategoryListView.as_view()),
    path('articulos/<int:pk>', ArticleDetail.as_view()),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken'))
]

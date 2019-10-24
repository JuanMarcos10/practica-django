from rest_framework.permissions import BasePermission

from articles.models import Article


class ArticlePermission(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'GET' or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return obj.estado == Article.PUBLICADO or obj.usuario == request.user or request.user.is_superuser

        return obj.usuario == request.user or request.user.is_superuser
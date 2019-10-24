from django.contrib import admin

# Custom models registration
from articles.models import Article, Category

admin.site.register(Article)
admin.site.register(Category)


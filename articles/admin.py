from django.contrib import admin
from .models import Article, ReadPost

admin.site.register(Article)
admin.site.register(ReadPost)
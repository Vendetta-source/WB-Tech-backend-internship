from django.urls import path, include
from .views import ArticleAPIList, ArticleRead

urlpatterns = [
    path('articles/', ArticleAPIList.as_view()),
    path('articles/<int:pk>/read_mark/', ArticleRead.as_view()),
]
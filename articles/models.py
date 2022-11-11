from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    """
    Model for articles.
    """
    title = models.CharField(max_length=100, verbose_name='Заголовок статьи')
    content = models.TextField(max_length=10000, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class ReadPost(models.Model):
    """
    Model for marking a article as read.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_readed = models.BooleanField(default=False)


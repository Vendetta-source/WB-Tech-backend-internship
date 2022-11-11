from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Article, ReadPost
from users.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True).data

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['author']

    def create(self, validated_data):
        author = self.context.get('request').user
        title = self.initial_data.get('title')
        content = self.initial_data.get('content')
        article = Article.objects.create(author=author, title=title, content=content)
        return article

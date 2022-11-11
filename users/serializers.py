from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FollowUser


class UserSerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'article_count')

    def get_article_count(self, author):
        return author.articles.count()


class FollowUserSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(source='author.id')
    user = serializers.IntegerField(source='user.id')

    class Meta:
        model = FollowUser
        fields = ('user', 'author')

    def validate(self, data):
        user = data['user']['id']
        author = data['author']['id']
        follow_exist = FollowUser.objects.filter(user__id=user, author__id=author).exists()
        if user == author:
            raise serializers.ValidationError(
                {"error": 'You cannot subscribe to yourself.'}
            )
        elif follow_exist:
            raise serializers.ValidationError({"error": 'You are already subscribed'})
        return data

    def create(self, validated_data):
        author = validated_data.get('author')
        author = get_object_or_404(User, pk=author.get('id'))
        user = User.objects.get(id=validated_data["user"]["id"])
        return FollowUser.objects.create(user=user, author=author)


from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FollowUser
from .permissions import ReadOnly
from .serializers import UserSerializer, FollowUserSerializer
from articles.models import Article
from articles.serializers import ArticleSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    @action(detail=False, permission_classes=[ReadOnly])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ordering = self.request.query_params.get('ordering', None)
        queryset = queryset.annotate(cnt=Count('articles'))
        response = super(UserViewSet, self).list(queryset, args, kwargs)
        if response.data['results']:
            if ordering == 'up':
                response.data['results'] = sorted(response.data['results'], key=lambda x: x['article_count'])
            elif ordering == 'down':
                response.data['results'] = sorted(response.data['results'], key=lambda x: x['article_count'], reverse=True)
            else:
                response.data['results'] = sorted(response.data['results'], key=lambda x: x['id'])
            return Response(response.data, status=status.HTTP_200_OK)
        return Response(response.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[ReadOnly])
    def retrieve(self, request, pk=None):
        queryset = Article.objects.filter(author=pk)
        if queryset:
            serializer = ArticleSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'This user has not created any articles or user does not exist.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        queryset = User.objects.filter(pk=pk)
        if queryset:
            serializer = FollowUserSerializer(data=dict(author=pk, user=request.user.id), context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'This pk is not valid!'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def unsubscribe(self, request, pk=None):
        queryset = User.objects.filter(pk=pk)
        if queryset:
            author = get_object_or_404(User, pk=pk)
            sub_pair = FollowUser.objects.filter(user=request.user, author=author)
            if sub_pair:
                sub_pair.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Attempt to delete a non-existent subscription'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'This pk is not valid!'}, status=status.HTTP_400_BAD_REQUEST)


class ShowSubArticlesViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FollowUser.objects.filter(user_id=self.request.user)
        queryset_articles = Article.objects.none()
        for item in queryset:
            article = Article.objects.filter(author_id=item.author, created_at__gt=item.time_sub)
            if article:
                queryset_articles = article | queryset_articles
        return queryset_articles

    @action(detail=False, permission_classes=[IsAuthenticated])
    def show_sub_articles(self, request):
        queryset_articles = self.get_queryset()
        response = super(ShowSubArticlesViewSet, self).list(queryset_articles, request)
        if queryset_articles:
            return Response(response.data, status=status.HTTP_200_OK)
        return Response(response.data, status=status.HTTP_204_NO_CONTENT)

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import Article, ReadPost
from .serializers import ArticleSerializer


class ArticleAPIList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ArticleRead(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'No pk.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Article.objects.get(pk=pk)
            if len(ReadPost.objects.filter(user=self.request.user.id, article=instance.id)) >= 1:
                return Response({'error': 'Article already read.'}, status=status.HTTP_409_CONFLICT)
        except:
            return Response({'error': 'Object does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        article = instance
        is_readed = True
        ReadPost.objects.create(article=article, user=user, is_readed=is_readed)
        return Response({'message': 'You read this article now.'}, status=status.HTTP_201_CREATED)



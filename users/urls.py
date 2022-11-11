from django.urls import path, include, re_path
from .views import UserViewSet, ShowSubArticlesViewSet

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('users/<int:pk>/subscribe/', UserViewSet.as_view({'post': 'subscribe'})),
    path('users/<int:pk>/unsubscribe/', UserViewSet.as_view({'post': 'unsubscribe'})),
    path('users/subscribed_authors_articles/', ShowSubArticlesViewSet.as_view({'get': 'show_sub_articles'}))
]
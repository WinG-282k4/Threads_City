from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'threads', views.ThreadViewSet, basename='thread')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'follows', views.FollowViewSet, basename='follow')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

# Nested router for comments
thread_router = DefaultRouter()
thread_router.register(r'comments', views.CommentViewSet, basename='thread-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('threads/<int:thread_pk>/', include(thread_router.urls)),
]

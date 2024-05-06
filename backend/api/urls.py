from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, WikiViewSet, MyWikiViewSet

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('wiki', WikiViewSet)
router.register('mywiki', MyWikiViewSet, basename='mywiki')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, WikiViewSet, MyWikiViewSet, PortalViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('wiki', WikiViewSet)
router.register('mywiki', MyWikiViewSet, basename='mywiki')
router.register('portal', PortalViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

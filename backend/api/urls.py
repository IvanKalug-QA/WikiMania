from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, WikiViewSet

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('wiki', WikiViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied
from djoser.views import UserViewSet

from wiki.models import Wiki
from .serializers import WikiSerializer


class UserViewSet(UserViewSet):
    http_method_names = ['get', 'post', 'delete',]


class WikiViewSet(ModelViewSet):
    queryset = Wiki.objects.all()
    serializer_class = WikiSerializer
    http_method_names = (
        'get', 'post', 'delete', 'patch'
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied('Редактировать может только автор!')
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Удалить может только автор!')
        return super().perform_destroy(instance)

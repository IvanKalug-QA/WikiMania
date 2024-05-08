from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from wiki.models import Wiki, Subscribe, CustomUser
from .serializers import WikiSerializer, GetUserSerializer


class UserViewSet(UserViewSet):
    http_method_names = ['get', 'post', 'delete',]
    lookup_field = 'pk'

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

    @action(methods=['DELETE', 'POST'], detail=True)
    def subscribe(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        if request.method == 'POST':
            serializer = GetUserSerializer(
                user, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(
                user=request.user,
                subscribe=user
            )
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            try:
                Subscribe.objects.get(
                    user=request.user,
                    subscribe=user).delete()
                return Response(
                    data={'Ты отписан!'},
                    status=status.HTTP_200_OK
                )
            except ObjectDoesNotExist:
                return Response(
                    data={'Такой подписки нет!'},
                    status=status.HTTP_400_BAD_REQUEST
                )


class WikiViewSet(ModelViewSet):
    queryset = Wiki.objects.all()
    serializer_class = WikiSerializer
    http_method_names = (
        'get', 'post', 'delete', 'patch'
    )
    lookup_field = 'pk'

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


class MyWikiViewSet(ModelViewSet):
    serializer_class = WikiSerializer
    http_method_names = ['get', ]

    def get_queryset(self):
        subscribed_users = Subscribe.objects.filter(
            user=self.request.user).values_list('subscribe', flat=True)
        return Wiki.objects.filter(author__in=subscribed_users)

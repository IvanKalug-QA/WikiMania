import base64

from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from wiki.models import Wiki

User = get_user_model()


class CreateUserSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password')
        read_only_fields = ('id',)


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
        read_only_fields = fields


class Base64ImageSerializer(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format_img, img_str = data.split(';base64,')
            ext = format_img.split('/')[-1]
            data = ContentFile(base64.b64decode(img_str), 'temp.' + ext)
        return super().to_internal_value(data)


class WikiSerializer(serializers.ModelSerializer):
    image = Base64ImageSerializer()
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Wiki
        fields = (
            'id', 'title', 'image', 'text', 'author'
        )
        read_only_fields = ('author',)

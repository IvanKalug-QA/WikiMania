import base64

from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from wiki.models import Wiki, Subscribe, Like, Dislike

User = get_user_model()


class CreateUserSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password')
        read_only_fields = ('id',)


class GetUserSerializer(serializers.ModelSerializer):
    count_wiki = serializers.SerializerMethodField()

    def get_count_wiki(self, obj):
        return obj.wiki_all.count()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'count_wiki')
        read_only_fields = fields

    def validate(self, data):
        author = self.instance
        user = self.context['request'].user
        if Subscribe.objects.filter(
             user=user,
             subscribe=author.id).exists():
            raise serializers.ValidationError('Ты уже подписан!')
        if author == user:
            raise serializers.ValidationError('На себя подписываться нельзя!')
        return data


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
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return obj.wiki_likes.count()

    def get_dislikes(self, obj):
        return obj.wiki_dislikes.count()

    class Meta:
        model = Wiki
        fields = (
            'id', 'title', 'image', 'text', 'author', 'likes', 'dislikes'
        )
        read_only_fields = ('author', 'likes', 'dislikes')


class GetWikiSerializer(WikiSerializer):
    image = Base64ImageSerializer(read_only=True)

    def validate(self, data):
        request = self.context['request']
        if 'like' in request.path:
            if Like.objects.filter(user=request.user,
                                   wiki_like=self.instance).exists():
                raise serializers.ValidationError(
                    'Ты уже подписан!'
                )
            return data
        elif 'dislike' in request.path:
            if Dislike.objects.filter(user_diser=request.user,
                                      wiki_dislike=self.instance).exists():
                raise serializers.ValidationError(
                    'Ты уже дисанул!'
                )
            return data
        return data

    class Meta(WikiSerializer.Meta):
        read_only_fields = WikiSerializer.Meta.fields

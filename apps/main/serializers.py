from rest_framework import serializers
from apps.main.models import (
    Post,
    Like, Analytic
)
from apps.users.serializers import UserBasicSerializer


class PostListSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'created_at', 'likes_count', 'is_liked')

    @staticmethod
    def get_likes_count(obj):
        count = obj.like_set.count()
        return count

    def get_is_liked(self, obj):
        user = self.context.get('user')
        exists = obj.like_set.filter(user=user).exists()
        return exists


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True, required=False)
    likes_count = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body', 'created_at', 'likes_count', 'is_liked')

    @staticmethod
    def get_likes_count(obj):
        count = obj.like_set.count()
        return count

    def get_is_liked(self, obj):
        user = self.context.get('user')
        exists = obj.like_set.filter(user=user).exists()
        return exists

    def save(self, **kwargs):
        user = self.context.get('user')
        self.validated_data['user'] = user
        return super(PostDetailSerializer, self).save(**kwargs)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body')

    def save(self, **kwargs):
        user = self.context.get('user')
        self.validated_data['user'] = user
        return super(PostCreateSerializer, self).save(**kwargs)

    def to_representation(self, instance):
        serializer = PostDetailSerializer(instance)
        return serializer.data


class AnalyticSerializer(serializers.ModelSerializer):
    post = PostDetailSerializer()

    class Meta:
        model = Analytic
        fields = ('id', 'post', 'date', 'likes_count')


class PostAnalyticsSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()
    analytics = AnalyticSerializer(source='analytic_set', many=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'created_at', 'analytics')




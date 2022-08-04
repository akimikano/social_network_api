from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from apps.main.filters import AnalyticFilter
from apps.main.models import Post, Like, Analytic
from rest_framework import (
    viewsets,
    views,
    mixins,
    permissions,
    status
)
from apps.main.serializers import (
    PostListSerializer,
    PostDetailSerializer,
    AnalyticSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('user').prefetch_related('like_set').filter(is_archived=False)
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update',]:
            return PostDetailSerializer
        else:
            return PostListSerializer

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({
            'user': self.request.user
        })
        return context

    @swagger_auto_schema(method='get',
                         responses={'200': PostDetailSerializer})
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def like_unlike(self, request, pk):
        obj = get_object_or_404(Post, pk=pk)
        likes = obj.like_set.filter(user=self.request.user)
        if likes:
            likes.delete()
        else:
            Like.objects.create(user=self.request.user, post=obj)
        context = self.get_serializer_context()
        serializer = PostDetailSerializer(obj, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnalyticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Analytic.objects.select_related('post__user').all()
    serializer_class = AnalyticSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnalyticFilter
    permission_classes = [IsAdminUser]

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter


from .serializers import CategorySerializer,PostSerialiser
from .models import Category, Post

class PermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminUser]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

class CategoryViewSet(PermissionMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(PermissionMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerialiser
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title','created_at']
    ordering_fields = ['created_at', 'title']



    # @action(methods=['POST'], detail=True)
    # def like(self, request, pk=None):
    #     post = self.get_object()
    #     user = request.user
    #     try:
    #         like = Like.objects.get(post=post,author=user)
    #         like.delete()
    #         message = 'disliked'
    #     except Like.DoesNotExist:
    #         like = Like.objects.create(post=post,author=user,is_liked =True)
    #         like.save()
    #         message='liked'
    #     return Response(message, status=201)
    

    # @action(methods=['POST'],detail=True)
    # def like(self, request, pk=None):
    #     product = self.get_object()
    #     author = request.user
    #     serializer = LikeSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         try:
    #             like = Like.objects.get(product=product,author=author)
    #             like.delete()
    #             message= 'disliked'
    #         except Like.DoesNotExist:
    #             Like.objects.create(product=product,author=author)
    #             message = 'liked'
    #         return Response(message,status=200)

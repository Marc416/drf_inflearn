# # ViewSets define the view behavior.
# from django.contrib.auth.models import User
# from rest_framework import viewsets
# from rest_framework.generics import ListAPIView
#
# from api2.serializers import UserSerializer
# from api2.serializers import PostSerializer
# from api2.serializers import CommentSerializer
# from blog.models import Post, Comment
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
# --------------------------------------------------

# GenericApiView 로 만들어보기
# api2/post[GET], api2/post/pk[GET], api2/comment[POST] 를 변경해보기
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from api2.serializers import PostSerializer, CommentSerializer
from blog.models import Post, Comment


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

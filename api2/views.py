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
from collections import OrderedDict

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api2.serializers import PostListSerializer, CommentSerializer, PostRetrieveSerializer, PostLikeSerializer, CateTagSerializer, PostSerializerDetail
from blog.models import Post, Comment, Category, Tag


class PostPageNumberPagination(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    # Viewset에서는 get 메서드를 사용하지 않으므로 다른 메서드로 바구고 url 매핑해주기
    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()

        return Response(instance.like)


# class PostListAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#
#     def get_serializer_context(self):
#         """
#         Extra context provided to the serializer class.
#         """
#         return {
#             # 상속에 속성에 따라 request를 None 처리하면 Url이 상대 url로 나오게됨
#             'request': None,
#             'format': self.format_kwarg,
#             'view': self
#         }
#

# class PostRetrieveAPIView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializerDetail
#
#     def get_serializer_context(self):
#         """
#         Extra context provided to the serializer class.
#         """
#         return {
#             # 상속에 속성에 따라 request를 None 처리하면 Url이 상대 url로 나오게됨
#             'request': None,
#             'format': self.format_kwarg,
#             'view': self
#         }
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         # 장고에서 기본으로 제공해주는 인스턴 : 해당인스턴스 앞뒤를 부름
#         prevInstance, nextInstance = get_prev_next(instance=instance)
#         commentList = instance.comment_set.all()
#         data = {
#             'post': instance,
#             'prevPost': prevInstance,
#             'nextPost': nextInstance,
#             'commentList': commentList,
#
#         }
#         serializer = self.get_serializer(instance=data)
#         # 직렬화는 serializer.data 할때 직렬화 진행됨
#         return Response(serializer.data)
#
#
# class PostLikeAPIView(GenericAPIView):
#     queryset = Post.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.like += 1
#         instance.save()
#
#         return Response(instance.like)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# class CommentCreateAPIView(CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


class CateTagListAPIView(APIView):
    """
    GenericAPIView 는 하나의 테이블을 처리하는 APIView,
    DB를 처리하기 위한 클래스임.
    DB처리를하기위한 메서드를 오버라이드해서 사용할것이 아니라면 APIView를 상속하는게 낫다(새로처음부터뭔가 만들것이라면)
    """

    def get(self, request, *args, **kwargs):
        category_list = Category.objects.all()
        tag_list = Tag.objects.all()
        data = {
            'cateList': category_list,
            'tagList': tag_list
        }
        # 인스턴스 인자는 시리얼라이저와 같아야 한다
        serializer = CateTagSerializer(instance=data)
        return Response(serializer.data)

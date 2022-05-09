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
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from api2.serializers import PostListSerializer, CommentSerializer, PostRetrieveSerializer
from blog.models import Post, Comment


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer


class PostLikeAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    # Put 과 Patch의 차이점:
    # Blank true가 아닌 필드는 필수 필드이고 필수 필드는 Put 메서드실행시 필요.
    # Patch에서는 필수필드가 필요없다.
    # 장고쉘에서 시리얼 라이저 필드중 필수 필드를 확인할 수 있음
    # PATCH
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # 변경하고자 하는 필드만 변경
        data = {'like': instance.like + 1}
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

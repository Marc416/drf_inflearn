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
from rest_framework.views import APIView

from api2.serializers import PostListSerializer, CommentSerializer, PostRetrieveSerializer, PostLikeSerializer, CateTagSerializer
from blog.models import Post, Comment, Category, Tag


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer


class PostLikeAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer

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

        return Response(data['like'])


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


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

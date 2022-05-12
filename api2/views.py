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
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api2.serializers import PostListSerializer, CommentSerializer, PostRetrieveSerializer, PostLikeSerializer, CateTagSerializer, PostSerializerDetail
from blog.models import Post, Comment, Category, Tag


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }


# class PostRetrieveAPIView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostRetrieveSerializer

def get_prev_next(instance):
    try:
        prev = instance.get_previous_by_update_dt()
    except instance.DoesNotExist:
        # exception은 인스턴스나 모델에 붙여서 사용
        prev = None

    try:
        next_ = instance.get_next_by_update_dt()
    except instance.DoesNotExist:
        next_ = None
    return prev, next_


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerDetail

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 장고에서 기본으로 제공해주는 인스턴 : 해당인스턴스 앞뒤를 부름
        prevInstance, nextInstance = get_prev_next(instance=instance)
        commentList = instance.comment_set.all()
        data = {
            'post': instance,
            'prevPost': prevInstance,
            'nextPost': nextInstance,
            'commentList': commentList,

        }
        serializer = self.get_serializer(instance=data)
        # 직렬화는 serializer.data 할때 직렬화 진행됨
        return Response(serializer.data)


# class PostLikeAPIView(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostLikeSerializer
#
#     # Put 과 Patch의 차이점:
#     # Blank true가 아닌 필드는 필수 필드이고 필수 필드는 Put 메서드실행시 필요.
#     # Patch에서는 필수필드가 필요없다.
#     # 장고쉘에서 시리얼 라이저 필드중 필수 필드를 확인할 수 있음
#     # PATCH
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         # 변경하고자 하는 필드만 변경
#         data = {'like': instance.like + 1}
#         serializer = self.get_serializer(instance, data=data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#
#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}
#
#         return Response(data['like'])

# PATCH vs GET
# like 는 사용자의 데이터 입력 부분없이 이벤트에 의해 작동되므로 GET 으로 동작해도 됨
class PostLikeAPIView(GenericAPIView):
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()

        return Response(instance.like)


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

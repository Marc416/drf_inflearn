# Serializers define the API representation.
from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Post, Comment, Category, Tag


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class PostListSerializer(serializers.ModelSerializer):
    """
       {
           "postList": [
               {
                 "id": 1,
                 "title": "Django 4.x Technical Board Election Results",
                 "image": "/media/blog/2021/06/05-full.jpg",
                 "like": 0,
                 "category": "IT"
               },
           ],
           "pageCnt": 2,
           "curPage": 1
       }
       이번에 필요한 것 : postList, pagination
       """

    # 카테고리 테이블의 네임 컬럼을 보여주겠다
    category = serializers.CharField(source='category.name')
    """
        category = PrimaryKeyRelatedField(allow_null=True, queryset=Category.objects.all(), required=False)
        카테고리가 자동으로 프라이머리 키로 잡혀있어서 프라이머리 키로 나오고 있었음
    """

    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'like', 'category']


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['like']


class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['create_dt']


class PostSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title']


class CommentSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'update_dt']


class PostSerializerDetail(serializers.Serializer):
    post = PostRetrieveSerializer()
    prevPost = PostSerializerSub()
    nextPost = PostSerializerSub()
    commentList = CommentSerializerSub(many=True)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class CateTagSerializer(serializers.Serializer):
    """
    [두가지 모델을 이용하는 법 - 두가지 시리얼라이저를 섞어쓴다]
    Category, Tag 를 모델 시리얼 라이저로 만들어서
    새로운 시리얼 라이저로 만든다.
    이렇게하면 여러개의 카테고리 , 태그 의 속성들을 리스트로 응답할 수 있다.
    """
    # cateList = CategorySerializer(many=True)
    # tagList = TagSerializer(many=True)

    # Nested Serializer with List Field ; 리스트로 요소들을 보여줄 수 있게 된다.
    cateList = serializers.ListField(child=serializers.CharField())
    tagList = serializers.ListField(child=serializers.CharField())

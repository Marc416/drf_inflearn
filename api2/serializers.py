# Serializers define the API representation.
from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Post, Comment, Category, Tag


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class PostListSerializer(serializers.ModelSerializer):
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

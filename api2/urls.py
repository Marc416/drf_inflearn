# Routers provide an easy way of automatically determining the URL conf.
# from django.urls import path, include
# from rest_framework import routers

# from api2.views import UserViewSet
# from api2.views import PostViewSet
# from api2.views import CommentViewSet

# # ViewSet을 사용할때만 라우터를 사용한다
# router = routers.DefaultRouter()
# router.register(r'user', UserViewSet)
# router.register(r'post', PostViewSet)
# router.register(r'comment', CommentViewSet)
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]

# GenericAPIView 활용하기
from django.urls import path

from api2 import views

urlpatterns = [
    # name을 drf명명법을 따라 표기
    # defaultrouter를 사용시 root url인 'api2/' 가 만들어짐. 하지만 GenericView를 이용했기 때문에
    # 루트라 라우터는 만들어지지 않음
    # path('post/', views.PostListAPIView.as_view(), name='post-list'),
    # path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-detail'),
    # path('post/<int:pk>/like/', views.PostLikeAPIView.as_view(), name='post-like'),
    # path('comment/', views.CommentCreateAPIView.as_view(), name='comment-list'),
    # path('catetag/', views.CateTagListAPIView.as_view(), name='catetag_list'),

    path('post/', views.PostViewSet.as_view(actions={
        # get 요청이오면 list 메서드로 바인딩 ; list는 ViewSet 기본 메서드
        'get': 'list'
    }), name='post-list'),
    path('post/<int:pk>/', views.PostViewSet.as_view(actions={
        # get 요청이오면 retrieve 메서드로 바인딩 ; retrieve ViewSet 기본 메서드
        'get': 'retrieve'
    }), name='post-detail'),
    path('post/<int:pk>/like/', views.PostViewSet.as_view(actions={
        'get': 'like'
    }), name='post-like'),

    path('comment/', views.CommentViewSet.as_view(actions={
        'post': 'create'
    }), name='comment-list'),

    path('catetag/', views.CateTagListAPIView.as_view(), name='catetag_list'),
]

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
from django.urls import path, include

from api2 import views

urlpatterns = [
    # name을 drf명명법을 따라 표기
    path('post', include(views.PostListAPIView.as_view(), names='post-list')),
    path('post/<int:pk>', include(views.PostRetrieveAPIView.as_view(), names='post-detail')),
    path('comment', include(views.CommentCreateAPIView.as_view(), names='comment-list')),
]

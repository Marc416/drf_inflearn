# Routers provide an easy way of automatically determining the URL conf.
from django.urls import path, include
from rest_framework import routers

from api2.views import UserViewSet
from api2.views import PostViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'post', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

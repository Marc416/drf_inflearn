from django.urls import path
from django.urls import include
from django.contrib import admin

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api2/', include('api2.urls')),

    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

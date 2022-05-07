from django.conf.urls.static import static
from django.urls import path
from django.urls import include
from django.contrib import admin

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
from mysite import settings
from mysite.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('blog/', include('blog.urls')),

    # Class View API
    path('api/', include('api.urls')),

    # api/ 를 drf로 api2/ 에서 만들기
    # DRF API
    path('api2/', include('api2.urls')),

    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

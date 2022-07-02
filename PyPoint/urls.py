"""PyPoint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from main_app.views import PickPointViewSet
from rest_framework import permissions, routers
from rest_framework.authtoken import views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="PyPoint API",
      default_version='v1',
      description="e-commerce API",
      # terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="sasha55555k@yandex.rus"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

router = routers.SimpleRouter()
router.register(r'pick-points', PickPointViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('rest_framework.urls')),
    path('api/token-auth/', views.obtain_auth_token),
    path('api/', include(router.urls)),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

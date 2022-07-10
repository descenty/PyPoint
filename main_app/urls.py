from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from main_app.views import RegisterCustomerView


urlpatterns = [
    path('api/', include('main_app.api_urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/register/', RegisterCustomerView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]

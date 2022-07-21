from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from main_app.views import RegisterCustomerView, HomeView, SellersView, CartView
from main_app.views_functions import update_cart_good, update_cart_promo_code
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('api/', include('main_app.api_urls')),
    path('', HomeView.as_view(), name='home'),
    path('orders/', HomeView.as_view(), name='orders'),
    path('sellers/', SellersView.as_view(), name='sellers'),
    path('cart/', CartView.as_view(), name='cart'),
    path('update_cart_good/<str:action>', update_cart_good, name='update_cart_good'),
    path('update_cart_promo_code/', update_cart_promo_code, name='update_cart_promo_code'),
    path('admin/', admin.site.urls),
    path('accounts/register/', RegisterCustomerView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path, include, re_path
from main_app.api_views import GoodViewSet, PickPointViewSet, CreateCustomerView, CartGoodViewSet, post_vehicle_coords, AddToCart, \
    get_cart
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
router.register(r'pick-points', PickPointViewSet, basename='pick-points')
router.register(r'cart-goods', CartGoodViewSet, basename='cart-goods')
router.register(r'goods', GoodViewSet, basename='goods')

urlpatterns = [
    path('accounts/register/', CreateCustomerView.as_view()),
    path('accounts/', include('rest_framework.urls')),
    path('accounts/token-auth/', views.obtain_auth_token, name='token-auth'),
    path('add-to-cart/', AddToCart.as_view(), name='add-to-cart'),
    path('get-cart/', get_cart, name='get-cart'),
    path('post_vehicle-coords/', post_vehicle_coords, name='vehicle-coords'),
    path('', include(router.urls)),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
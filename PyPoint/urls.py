from django.urls import path, include

urlpatterns = [
    path('', include('main_app.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

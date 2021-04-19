from django.urls import path, include
from . import views


urlpatterns = [
    path('not-allowed', views.not_allowed),
    path('auth/', include('src.apps.users.urls')),
    path('', views.index),
    path('', include('src.apps.web.urls')),
]

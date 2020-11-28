from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('not-allowed', views.not_allowed),
    path('auth/', include('src.apps.users.urls')),
]

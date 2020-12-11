from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('', include('src.apps.web.urls')),
    path('not-allowed', views.not_allowed),
    path('auth/', include('src.apps.users.urls')),
]

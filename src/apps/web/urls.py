from django.urls import path, include
from . import views


urlpatterns = [
    path('users/', include('src.apps.web.users.urls')),
    path('organizations/', include('src.apps.web.orgs.urls')),
]

from django.urls import path, include
from . import views


urlpatterns = [
    path('users/', include('src.apps.web.users.urls')),
    path('organizations/', include('src.apps.web.orgs.urls')),
    path('classes/', include('src.apps.web.classes.urls')),
    path('teacher/', include('src.apps.web.teacher.urls')),
    path('pupil/', include('src.apps.web.pupil.urls')),
]

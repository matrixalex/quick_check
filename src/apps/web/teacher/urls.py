from django.urls import path, include
from . import views


urlpatterns = [
    path('homework/create-or-change', views.CreateOrChangeHomeworkView.as_view())
]

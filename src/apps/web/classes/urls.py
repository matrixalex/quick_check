from django.urls import path, include
from . import views


urlpatterns = [
    path('all', views.ListView.as_view()),
    path('create-or-change', views.CreateOrChangeView.as_view()),
    path('delete', views.DeleteView.as_view())
]

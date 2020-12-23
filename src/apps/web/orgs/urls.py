from django.urls import path, include
from . import views


urlpatterns = [
    path('all', views.AllOrgsView.as_view()),
    path('create', views.CreateOrgView.as_view()),
    path('change/<int:org_id>', views.ChangeOrgView.as_view()),
    path('delete', views.DeleteOrgView.as_view())
]

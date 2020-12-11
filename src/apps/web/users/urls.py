from django.urls import path, include
from . import views


urlpatterns = [
    path('system-admins', views.SystemAdminsView.as_view()),
    path('admins', views.AdminsView.as_view()),
    path('delete/<int:user_id>', views.UserDeleteView.as_view()),
    path('create', views.UserCreateView.as_view()),
    path('change/<int:user_id>', views.UserChangeView.as_view()),
    path('block/<int:user_id>', views.BlockUserView.as_view()),
    path('accept/<int:user_id>', views.AcceptRegistrationView.as_view()),
]

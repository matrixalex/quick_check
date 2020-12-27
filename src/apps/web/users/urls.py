from django.urls import path, include
from . import views


urlpatterns = [
    path('all', views.UsersView.as_view()),
    path('create-or-change', views.UserCreateOrChangeView.as_view()),
    path('delete', views.UserDeleteView.as_view()),
    path('block/<int:user_id>', views.BlockUserView.as_view()),
    path('accept/<int:user_id>', views.AcceptRegistrationView.as_view()),
]

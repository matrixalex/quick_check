from django.urls import path
from . import views


urlpatterns = [
    path('', views.AuthView.as_view()),
    path('login', views.LoginView.as_view()),
    path('registration', views.RegistrationView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('reset-password', views.ResetPasswordPageView.as_view()),
    path('reset-password/<uuid:str>', views.ResetPassword.as_view()),
]

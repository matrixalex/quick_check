from django.urls import path, include
from . import views


urlpatterns = [
    path('homework/create-or-change', views.CreateOrChangeHomeworkView.as_view()),
    path('homework/delete', views.HomeWorkDeleteView.as_view()),
    path('homework/<int:homework_id>', views.HomeworkShowView.as_view())
]

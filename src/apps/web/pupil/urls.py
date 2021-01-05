from django.urls import path, include
from . import views


urlpatterns = [
    path('appeal/<int:appeal_result_id>', views.AppealResultView.as_view()),
    path('homework/upload', views.UploadHomeworkView.as_view()),
    path('homework/appeal', views.AppealHomeworkView.as_view()),
    path('homework/<int:homework_id>', views.PupilHomeworkShowView.as_view())
]

"""
Api endpoint urls
"""

from django.urls import path
from . import views

urlpatterns = [
    path("resources", views.GetResourceView.as_view(), name="get-resources"),
    path(
        "resources/create", views.CreateResourceView.as_view(), name="create-resources"
    ),
    path("students", views.GetStudentView.as_view(), name="get-students"),
    path("students/create", views.CreateStudentView.as_view(), name="create-students"),
    path(
        "students/stats",
        views.GetStudentStatisticsView.as_view(),
        name="get-student-statistics",
    ),
    path(
        "students/delete/<str:student_id>",
        views.DeleteStudentView.as_view(),
        name="delete-student",
    ),
]

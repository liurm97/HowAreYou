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
    # path("students", views.GetStudentView.as_view(), name="get-students"),
    # path("students/create", views.CreateStudentView.as_view(), name="create-students"),
    # path(
    #     "students/response/evaluate",
    #     views.CreateStudentResponseView.as_view(),
    #     name="create-student-responses",
    # ),
    # path(
    #     "students/response/delete",
    #     views.DeleteStudentView.as_view(),
    #     name="delete-student",
    # ),
]

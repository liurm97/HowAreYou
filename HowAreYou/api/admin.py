from django.contrib import admin
from .models import Student, StudentResponse, Resource


class StudentResponseInline(admin.StackedInline):
    """
    Define StackedInline page for Student Response
    """

    model = StudentResponse
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    """
    Define admin page for Students
    """

    inlines = [
        StudentResponseInline,
    ]
    ordering = ["age"]
    list_display = ["age", "gender"]


class ResourceAdmin(admin.ModelAdmin):
    """
    Define admin page for Resources
    """

    ordering = ["id"]
    list_display = ["type", "url"]


admin.site.register(Student, StudentAdmin)
admin.site.register(Resource, ResourceAdmin)

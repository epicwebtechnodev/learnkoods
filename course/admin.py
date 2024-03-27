from django.contrib import admin
from course.models import Courses, CourseApplicant
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model



class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title'),
    search_fields = ("course_title"),

admin.site.register(Courses,CourseAdmin)
admin.site.register(CourseApplicant)
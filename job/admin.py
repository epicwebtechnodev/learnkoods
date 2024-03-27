from django.contrib import admin
from job.models import Job, JobApplicant,Category,City,SubCategory

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class JobAdmin(admin.ModelAdmin):
    search_fields = ['job_title']

class CatAdmin(admin.ModelAdmin):
    search_fields = ['name']

class SubCatAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Job,JobAdmin)
admin.site.register(JobApplicant)
admin.site.register(Category,CatAdmin)
admin.site.register(SubCategory,SubCatAdmin)
admin.site.register(City)
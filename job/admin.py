from django.contrib import admin
from job.models import *

class JobAdmin(admin.ModelAdmin):
    list_display = ('company','job_title')

admin.site.register(Job,JobAdmin)
admin.site.register(Applicant)
admin.site.register(Category)
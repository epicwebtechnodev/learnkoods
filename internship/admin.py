from django.contrib import admin
from internship.models import Internship, InternApplicant,Task

# Register your models here.

admin.site.register(Internship)
admin.site.register(Task)
admin.site.register(InternApplicant)
from django.contrib import admin
from companys.models import Company,CompanyEmployee,Role

# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyEmployee)

admin.site.register(Role)
from django.contrib import admin

from scrape_data.models import ScrapeJobResult,SearchQuery,RelatedQuestion, Indeed, Salary, Indeed_job,Courses

Model = [ScrapeJobResult,SearchQuery,RelatedQuestion]

admin.site.register(Model)

class AdminIndeed(admin.ModelAdmin):
    search_fields = (
        "title",
        "company",
    )

admin.site.register(Indeed,AdminIndeed)
# Register your models here.


class AdminSalary(admin.ModelAdmin):
    search_fields = (
        "title",
    )

admin.site.register(Salary,AdminSalary)


class AdminIndeedJob(admin.ModelAdmin):
    search_fields = (
        "title",
    )
admin.site.register(Indeed_job,AdminIndeedJob)

class AdminCourse(admin.ModelAdmin):
    search_fields = (
        "title",
        "skills",
    )
admin.site.register(Courses,AdminCourse)
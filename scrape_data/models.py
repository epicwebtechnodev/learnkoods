from django.db import models
from django.utils import timezone
from uploads.models import skil

# Create your models here.

class ScrapeJobResult(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True, default=None)
    link = models.URLField(max_length=400, null=True, blank=True, default=None)
    displayedLink = models.URLField(max_length=400, null=True, blank=True, default=None)
    source = models.CharField(max_length=100, null=True, blank=True, default=None)
    snippet = models.CharField(max_length=400, null=True, blank=True, default=None)
    snippetHighlitedWords = models.CharField(max_length=100, null=True, blank=True, default=None) 

    def __str__(self):
        return self.title


class SearchQuery(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.CharField(max_length=100, null=True, blank=True, default=None)  
    link = models.URLField(max_length=200, null=True, blank=True, default=None) 

    def __str__(self):
        return self.query

class RelatedQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=500, null=True, blank=True, default=None) 
    snippet = models.CharField(max_length=500, null=True, blank=True, default=None) 
    link = models.URLField(max_length=500, null=True, blank=True, default=None) 
    title = models.CharField(max_length=500, null=True, blank=True, default=None) 
    displayedLink = models.URLField(max_length=500, null=True, blank=True, default=None) 

    def __str__(self):
        return f"{self.question} - {self.title}"
    

class Indeed(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000, null=True, blank=True, default=None)
    company = models.CharField(max_length=1000, null=True, blank=True, default=None)
    locations = models.CharField(max_length=1000, null=True, blank=True, default=None)
    salary = models.CharField(max_length=1000, null=True, blank=True, default=None)
    posted_at = models.CharField(max_length=1000, null=True, blank=True, default=None)
    links = models.CharField(max_length=1000, null=True, blank=True, default=None)
    about_text = models.CharField(max_length =10000, null=True, blank= True, default=None)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.title} - {self.company}"
    
class Indeed_job(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000, null=True, blank=True, default=None)
    company = models.CharField(max_length=1000, null=True, blank=True, default=None)
    locations = models.CharField(max_length=1000, null=True, blank=True, default=None)
    salary = models.CharField(max_length=1000, null=True, blank=True, default=None)
    posted_at = models.CharField(max_length=1000, null=True, blank=True, default=None)
    links = models.CharField(max_length=1000, null=True, blank=True, default=None)
    skill = models.ManyToManyField(skil, null=True,blank=True, default=None)
    about_text = models.CharField(max_length =10000, null=True, blank= True, default=None)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.title} - {self.company}"
    
class Salary(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True, default=None)
    salary = models.PositiveIntegerField(null=True, blank=True, default=None)
    top_comp_sal = models.JSONField(null=True, blank=True, default=None)
    top_city_sal = models.JSONField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(default=timezone.now())


    def __str__(self):
        return self.title
    
class Courses(models.Model):
    id  = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True, default=None)
    skills = models.CharField(max_length=5000, null=True, blank=True, default=None)
    review = models.CharField(max_length=100, null=True, blank=True, default=None)
    course_for = models.CharField(max_length=100, null=True, blank=True, default=None)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title
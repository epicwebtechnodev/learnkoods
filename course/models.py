from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from uploads.models import skil
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# from company.models import Company
from job.models import City
from accounts.models import CustomUser
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True,default=None)
    course_title = models.CharField(max_length=100)
    course_price = models.DecimalField(max_digits=6, decimal_places=2,null=True)
    course_des = HTMLField(null=True, blank=True, default=None)
    skills = models.CharField(max_length=300, null=True, blank=True, default = None)
    skills_req =  models.ManyToManyField(skil)
    review = models.CharField(max_length=500, null=True, blank=True, default = None)
    company = models.ForeignKey(to="companys.Company",on_delete=models.CASCADE,null=False,default=None)
    course_level = models.CharField(choices=(('Beginner', ("Beginner")),
                                        ('Intermediate', ("Intermediate")),
                                        ('Advance', ("Advance"))),
                                default='Beginner',max_length=50)
    course_duration = models.CharField(max_length=100, null=True, blank=True,default=None)
    course_image = models.ImageField(upload_to="corse/",null=True,default="course/courses-1.jpg")
    course_slug = AutoSlugField(populate_from = 'course_title',unique=True,null=True,default=None)

    def __str__(self):
        return self.course_title

class CourseApplicant(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='course_applicant')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE,related_name='course_applicant')
    cover_letter = models.TextField(help_text=_("Enter your cover letter here."))
    available = models.BooleanField(default=False, help_text=_("Check if you are available for this internship."))
    resume = models.FileField(upload_to='documents/', blank=True, help_text=_("Upload your resume."))
    is_accepted = models.BooleanField(default=False, help_text=_("Check if your application is accepted."))
    is_rejected = models.BooleanField(default=False, help_text=_("Check if your application is rejected."))

    class Meta:
        verbose_name = _("Course Applicant")
        verbose_name_plural = _("Course Applicant")
        unique_together = ['student', 'course']  # Ensures each student can apply to an internship only once

    def __str__(self):
        return f"{self.student.get_full_name()} | {self.course.course_title}"
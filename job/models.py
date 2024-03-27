from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from uploads.models import skil
# from kood_api.manager import CustomUserManager
from tinymce.models import HTMLField
# from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# from companys.models import Company
from django.contrib.auth import get_user_model

User = get_user_model()



# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(_('email address'), unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     groups = models.ManyToManyField(Group, related_name='%(app_label)s_%(class)s_groups')
#     user_permissions = models.ManyToManyField(Permission, related_name='%(app_label)s_%(class)s_user_permissions')

#     objects = CustomUserManager()

class City(models.Model):
    name = models.CharField(max_length = 100, default=None, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name


class Job(models.Model):

    JOB_TYPE = [
        ("Full Time","Full Time"),
        ("Part Time","Part Time"),
        ("Internship","Internship"),
    ]

    TimeLine = [
        ("1 to 3 days","1 to 3 days"),
        ("3 to 7 days","3 to 7 days"),
        ("1 to 2 weeks","1 to 2 weeks"),
        ("2 to 4 weeks","2 to 4 weeks"),
        ("More than 4 weeks","More than 4 weeks"),
        ]


    job_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,default=None)
    # category = models.ForeignKey(Category,on_delete=models.CASCADE, default=None)
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE, default=None)
    job_title = models.CharField(max_length=100)
    job_type = models.CharField(choices=JOB_TYPE,default=None, null = True,max_length=50)
    exp_required = models.CharField(max_length=100)
    skills_req =  models.ManyToManyField(skil)
    job_des = HTMLField(blank=True, null=True)
    min_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Minimum Salary",
        help_text="Enter the minimum salary for this job (e.g., 50000.00)",
    )
    max_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Maximum Salary",
        help_text="Enter the maximum salary for this job (e.g., 80000.00)",
    )
    company = models.ForeignKey(to="companys.Company", on_delete=models.CASCADE,null=False,default=None)
    location = models.CharField(max_length=250)
    city = models.ForeignKey(City, default=None, on_delete=models.CASCADE)
    area = models.CharField(max_length=250, default=None,null=True, blank=True)
    pincode = models.PositiveIntegerField(validators=[RegexValidator(r'^\d{1,6}$')],null=True, blank=True)
    recruitment_timeline = models.CharField(choices=TimeLine, default=None, max_length=250)
    company_desc = HTMLField(blank=True, null=True)
    url = models.URLField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    job_image = models.ImageField(upload_to='job/', default = "job/jobs-1.jpg")
    job_slug = AutoSlugField(populate_from = 'get_full_slug',unique=True,null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    def get_full_slug(self):
        return f"{self.job_title} at {self.company}"


    def __str__(self):
        return self.job_title
    
    def save(self, *args, **kwargs):
        if self.recruitment_timeline not in dict(self.TimeLine).keys():
                raise ValidationError({'recruitment_timeline': 'Invalid choice selected.'})
        if self.job_type:
            if self.job_type not in dict(self.JOB_TYPE).keys():
                raise ValidationError({'job_type': 'Invalid choice selected.'})
        
        super().save(*args, **kwargs)

class JobApplicant(models.Model):
    user = models.ForeignKey(User, null=True,blank=True, default=None,on_delete=models.CASCADE, related_name="job_applicants")
    job = models.ForeignKey(Job, null=True,blank=True, default=None, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("Job Applicant")
        verbose_name_plural = _("Job Applicant")
        unique_together = ['user', 'job']

    def __str__(self):
        return self.job.job_title
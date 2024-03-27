from django.db import models
from django.contrib.auth.models import User, Group, Permission
from uploads.models import Industry
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
# from job.models import City
from django.apps import apps
from django.core.validators import RegexValidator, EmailValidator,URLValidator
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from job.models import Job
from course.models import Courses


from django.contrib.auth import get_user_model
import json


User = get_user_model()

# Create your models here.
class Company(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    email = models.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])
    website = models.URLField(validators=[URLValidator(message="Enter a valid website URL")], blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, default=None, null=True)
    city = models.ForeignKey("job.City", on_delete=models.CASCADE, default=None, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True,default = "company_logos/comp_logo.jpg")
    phone_regex = RegexValidator(regex=r'^\+44\s\d{10}$', message="Phone number must start with '+44' followed by 10 digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_job = models.BooleanField(default=False)
    is_course = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):


        if not self.pk:
            highest_id = Company.objects.order_by("-id").first()
            if highest_id:
                self.pk = highest_id.id+1
            else:   
                self.pk = 1
        super().save(*args, **kwargs)
    
    def assign_permissions_to_user(self, company_emp, permissions:list):
        """
        Assign permissions to a specific CompanyUser associated with this company.
        :param company_user: The CompanyUser instance to assign permissions to.
        :param permissions: List of permission codenames to assign.
        """

        if self.user == company_emp.user.username:
            raise ValueError("Permission can only be assigned by the company owner.")
        
        user = company_emp.user
        user.user_permissions.clear()  # Clear existing permissions
        
        try:
            permission = Permission.objects.filter(codename__in=permissions)
            user.user_permissions.add(*permission)
        except Permission.DoesNotExist:
            raise ValidationError("Permission does not Exists!")
        
class Role(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False,unique=True, default=None)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    permission = models.JSONField(default=list)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            high_id = Role.objects.order_by("-id").first()
            if high_id:
                self.pk= high_id.id+1
            else:
                self.pk=1
        super().save(*args,**kwargs)

    def assign_permissions_to_role(self, company, permissions):
        
        if not self.company.user.is_company:
            raise ValueError("Permission can only be assigned by the company owner.")
        
        user = company.user
        user.user_permissions.clear()  # Clear existing permissions
        
        try:
            permission = Permission.objects.filter(codename__in=permissions)
            user.user_permissions.add(*permission)
        except Permission.DoesNotExist:
            raise ValidationError("Permission does not Exists!")

class CompanyEmployee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.ForeignKey(Role,default=None, null=True, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'company')  # Ensure each user is associated with a company only once

    def __str__(self):
        return self.user.username
    
# @receiver(post_save, sender=CompanyEmployee)
# def create_user_permissions(sender, instance, created, **kwargs):
#     if created:
#         # Create user permissions after creating a CompanyUser instance
#         instance.save()
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, Group,Permission
from django.utils.translation import gettext_lazy as _
# from uploads.manager import CustomUserManager
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()


class Industry(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class skil(models.Model):
    data = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.data

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile/",null=True,default = "profile/profile-default.jpg")
    profile_desc = models.TextField(max_length=250,blank=True)
    institution = models.CharField(max_length=50,blank=True)
    resume = models.FileField(upload_to="resume/",null=True,default="resume/resume.pdf")
    resume_data = models.TextField(max_length=3000,null=True,default="RESUME")
    skills = models.ManyToManyField(skil)
    phone = PhoneNumberField(region="IN",null=True, blank=True,unique=True)
    gender = models.CharField(max_length=100)
    work_at = models.CharField(max_length=100, default=None, null=True, blank=True)
    position = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return self.user.username
    

    def save(self, *args, **kwargs):
        if not self.pk:
            # Get the highest existing ID in the Profile table
            highest_id = Profile.objects.order_by('-profile_id').first()
            if highest_id:
                self.pk = highest_id.profile_id + 1  # Increment by 1
            else:
                self.pk = 1  # If no records exist, start from 1
        super().save(*args, **kwargs)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# @receiver(post_delete, sender=Profile)
# def delete_related_user(sender, instance, **kwargs):
#     try:
#         instance.user.delete()
#     except CustomUser.DoesNotExist:
#         raise ValueError("User Does not Exists.")
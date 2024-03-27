from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from django.db import models, transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,username,first_name=None, last_name=None,email=None,password=None, **extra_fields):

        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError("The Password field must be set")
        email = self.normalize_email(email)
        with transaction.atomic():
            user = self.model(username=username, **extra_fields)
            if first_name is not None:
                user.first_name = first_name
            else:
                first_name = None
            if last_name is not None:
                user.last_name = last_name
            else:
                last_name = None
            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
    
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=200, null=False, blank=False, unique=True, verbose_name='Username', help_text='Enter your Username')
    email = models.EmailField(null=True, blank=True, unique=True, verbose_name='Email', help_text='Enter your Email')
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='First Name', help_text='Enter your First Name')
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Last Name', help_text='Enter your Last Name')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # Get the highest existing ID in the Profile table
            highest_id = CustomUser.objects.order_by('-id').first()
            if highest_id:
                self.pk = highest_id.id + 1  # Increment by 1
            else:
                self.pk = 1  # If no records exist, start from 1
        super().save(*args, **kwargs)
        
# @receiver(post_save, sender=CustomUser)
# def assign_group_and_permissions(sender, instance, created, **kwargs):
#     if created and instance.is_company:
#         job_group, created = Group.objects.get_or_create(name='Add_Jobs')
#         course_group, _ = Group.objects.get_or_create(name='Add_Course')
#         intern_group, _ = Group.objects.get_or_create(name='Add_Internship')
#         instance.groups.add(job_group, course_group, intern_group)
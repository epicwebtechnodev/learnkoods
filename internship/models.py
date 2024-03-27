from django.db import models
from job.models import City
from companys.models import Company
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from uploads.models import Profile
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Internship(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=None, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, null=True) 
    stipend = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    requirements = models.TextField(null=True, blank=True) 
    responsibilities = models.TextField(null=True, blank=True)
    eligibility_criteria = models.TextField(null=True, blank=True)
    duration_months = models.PositiveIntegerField()
    application_deadline = models.DateField()
    skills_required = models.CharField(max_length=200, null=True, blank=True)
    contact_email = models.EmailField()
    is_paid = models.BooleanField(default=False)
    min_experience = models.PositiveIntegerField()
    max_applicants = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=False, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    # assigned_to = models.ForeignKey(CustomUser,null=False, blank=False,on_delete=models.CASCADE)
    priority = models.CharField(max_length=20)
    # video = models.FileField(upload_to='videos_uploaded',null=True,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    estimated_hours = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Add created_at field
    updated_at = models.DateTimeField(auto_now=True)  # Add updated_at field
    category = models.CharField(max_length=50)  # Add category field
    assigned_to = models.ManyToManyField(CustomUser,null=True, blank=True)

    def __str__(self):
        return self.title

class InternApplicant(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='intern_applicant')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='intern_applicant')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(help_text=_("Enter your cover letter here."))
    available = models.BooleanField(default=False, help_text=_("Check if you are available for this internship."))
    resume = models.FileField(upload_to='documents/', blank=True, help_text=_("Upload your Resume."))
    is_accepted = models.BooleanField(default=False, help_text=_("Check if your application is accepted."))
    is_rejected = models.BooleanField(default=False, help_text=_("Check if your application is rejected."))

    class Meta:
        verbose_name = _("Intership Applicant")
        verbose_name_plural = _("Intership Applicant")
        unique_together = ['student', 'internship']  # Ensures each student can apply to an internship only once

    def __str__(self):
        return f"{self.student.get_username()} | {self.internship.title}"

    def save(self, *args, **kwargs):

        if not self.pk:
            highest_id = Internship.objects.order_by("-id").first()
            if highest_id:
                self.pk = highest_id.id+1
            else:
                self.pk = 1

        current_applicants_count = self.internship.intern_applications.count()
            
        if current_applicants_count >= int(self.internship.max_applicants):
            raise ValidationError("Maximum number of applicants reached for this internship.")
        
        super().save(*args, **kwargs)

# Generated by Django 4.2.4 on 2024-03-27 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companys', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('stipend', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('requirements', models.TextField(blank=True, null=True)),
                ('responsibilities', models.TextField(blank=True, null=True)),
                ('eligibility_criteria', models.TextField(blank=True, null=True)),
                ('duration_months', models.PositiveIntegerField()),
                ('application_deadline', models.DateField()),
                ('skills_required', models.CharField(blank=True, max_length=200, null=True)),
                ('contact_email', models.EmailField(max_length=254)),
                ('is_paid', models.BooleanField(default=False)),
                ('min_experience', models.PositiveIntegerField()),
                ('max_applicants', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='job.city')),
                ('company', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='companys.company')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True, unique=True)),
                ('description', models.TextField()),
                ('deadline', models.DateField()),
                ('is_completed', models.BooleanField(default=False)),
                ('priority', models.CharField(max_length=20)),
                ('estimated_hours', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=50)),
                ('assigned_to', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('internship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='internship.internship')),
            ],
        ),
        migrations.CreateModel(
            name='InternApplicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.TextField(help_text='Enter your cover letter here.')),
                ('available', models.BooleanField(default=False, help_text='Check if you are available for this internship.')),
                ('resume', models.FileField(blank=True, help_text='Upload your Resume.', upload_to='documents/')),
                ('is_accepted', models.BooleanField(default=False, help_text='Check if your application is accepted.')),
                ('is_rejected', models.BooleanField(default=False, help_text='Check if your application is rejected.')),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intern_applicant', to='internship.internship')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intern_applicant', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='internship.task')),
            ],
            options={
                'verbose_name': 'Intership Applicant',
                'verbose_name_plural': 'Intership Applicant',
                'unique_together': {('student', 'internship')},
            },
        ),
    ]

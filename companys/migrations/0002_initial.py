# Generated by Django 4.2.4 on 2024-03-27 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uploads', '0001_initial'),
        ('companys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='job.city'),
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='uploads.industry'),
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='companyemployee',
            unique_together={('user', 'company')},
        ),
    ]
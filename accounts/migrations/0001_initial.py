# Generated by Django 4.2.4 on 2024-03-27 10:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(help_text='Enter your Username', max_length=200, unique=True, verbose_name='Username')),
                ('email', models.EmailField(blank=True, help_text='Enter your Email', max_length=254, null=True, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, help_text='Enter your First Name', max_length=50, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, help_text='Enter your Last Name', max_length=50, null=True, verbose_name='Last Name')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_company', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
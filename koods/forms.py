from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Permission,Group
from accounts.models import CustomUser
from uploads.models import Profile
from job.models import Job
from course.models import Courses
from django.contrib.auth import get_user_model
User = get_user_model()
from tinymce.widgets import TinyMCE

# class ADDJOB(forms.ModelForm):
#     class Meta:
#         model = Job
#         fields = ['category','job_title','job_type','exp_required','skills_req','job_des','min_salary','max_salary','location','company','company_desc','url','job_image','is_published','is_closed']
#         widgets = {'content':TinyMCE(attrs={'cols':80, 'rows':30})}

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(ADDJOB, self).__init__(*args, **kwargs)
#         self.fields['skills_req'].widget.attrs = {'class':'js-select2','required':'required'}
        
#         if user:
#             self.user = user 

class ADDJOB_DESC(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_des', 'company_desc']
        widgets = {'content':TinyMCE(attrs={'cols':80, 'rows':30})}


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ADDJOB_DESC, self).__init__(*args, **kwargs)
        # self.fields['skills_req'].widget.attrs = {'class':'js-select2','required':'required'}
        self.fields['job_des'].label = "Job Description"
        self.fields['company_desc'].label = "Course Description"
        
        if user:
            self.user = user 
        
class ADDCOURSE_DESC(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['course_des']
        widgets = {'content':TinyMCE(attrs={'cols':80, 'rows':30})}


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ADDCOURSE_DESC, self).__init__(*args, **kwargs)
        # self.fields['skills_req'].widget.attrs = {'class':'js-select2','required':'required'}
        self.fields['course_des'].label = "Course Description"
        
        if user:
            self.user = user 
    
    
class EDITJOB(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_title','job_type','exp_required','skills_req','job_des','min_salary','max_salary','location','company','company_desc','url','job_image','is_published','is_closed']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EDITJOB, self).__init__(*args, **kwargs)
        self.fields['skills_req'].widget.attrs = {'class':'js-select2'}
        if user:
            self.user = user 



class EDIT_DESC(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_des', 'company_desc']
        widgets = {'content':TinyMCE(attrs={'cols':80, 'rows':30})}


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EDIT_DESC, self).__init__(*args, **kwargs)
        self.fields['job_des'].label = "Job Description"
        self.fields['company_desc'].label = "Course Description"
        
        if user:
            self.user = user 


# class ADDCOURSE(forms.ModelForm):
#     class Meta:
#         model = Courses
#         fields = ['course_title','course_price','course_des','course_level','course_duration','course_image']

class CreateUserForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','email','password1','password2']

    def create(self,validated_data):
        username = validated_data.pop("username",None)
        groups_data = validated_data.pop("groups", [])
        # perms_data = validated_data.pop("user_permissions", []) 
        user = CustomUser.objects.create(username=username,**validated_data)
        user.is_company = True
        user.is_active = True
        user.save()
        user.groups.set(groups_data)
        permission_data = ['add_job','change_job','create_job','delete_job','view_job','add_courses','change_courses','delete_courses','view_courses','add_internship','change_internship','delete_internship','view_internship','add_customuser',"add_companyemployee","change_companyemployee","delete_companyemployee","view_companyemployee"]
        permissions = Permission.objects.filter(codename__in=permission_data)
        user.user_permissions.set(*permissions)
        return user
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = [
#             'username', 
#             'first_name', 
#             'last_name', 
#             'email', 
#         ]

# GENDER_CHOICES = [
#     ('Male','Male'),('Female','Female'),('Other','Other'),('Prefer not to say','Prefer not to say')
# ]
# SKILL_CHOICES = [
#     ('Python','Python'),('Django','Django'),('HTML','HTML'),('CSS','CSS'),('Bootstrap','Bootstrap'),('Wordpress','Wordpress'),('Java','Java'),('Shopify','Shopify')
# ]

# class ProfileForm(forms.ModelForm):
#     gender = forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect)
#     skills = forms.MultipleChoiceField(choices=SKILL_CHOICES,widget=forms.CheckboxSelectMultiple)
#     class Meta:
#         model = Profile
#         fields = [
#             'profile_image',
#             'profile_desc',
#             'resume',
#             'resume_data',
#             'skills',
#             'gender',
#             'phone',
#             'institution',
#         ]
#         labels = {'institution':'Institution/Organization','profile_desc':'About','profile_image':'Profile Image','resume':'Resume'}
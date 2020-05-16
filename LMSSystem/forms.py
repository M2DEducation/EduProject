from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import ClassList, Assignments, AssignmentWeight

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Supervisor', 'Supervisor'),
    )
    email = forms.EmailField(max_length=150,widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter email'}))
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':''}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':''}))
    Register_As = forms.ChoiceField(choices=ROLE_CHOICES,widget=forms.Select(attrs={'class': 'form-control roleInput','placeholder':''}))
    Teacher_Registration_Code = forms.CharField(min_length=32,max_length=32,widget=forms.TextInput(attrs={'class': 'form-control regCode','placeholder':''}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    Profile_Image = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2','Register_As','Teacher_Registration_Code','Profile_Image')

class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=150,widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # class Meta:
    #     model = User
    #     fields = ('username', 'password',)

class CreateNewClass(ModelForm):
    class_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Intro To English'}))
    class_subject = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'English'}))
    class_photo = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    class_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    syllabus = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = ClassList
        fields = ['class_name','class_subject','class_photo','class_description', 'syllabus']

class CreateNewAssignment(ModelForm):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Published', 'Published'),
        ('Late', 'Late'),
    )
    TYPE_CHOICES =(
        ('File Upload','File Upload'),
        ('Homework','Homework'),
        ('Discussion','Discussion'),
        ('Quiz','Quiz'),
        ('Test','Test'),
    )
    assignment_name = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Assignment Name...'}))
    assignment_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    assignment_type = forms.ChoiceField(choices=TYPE_CHOICES,widget=forms.Select(attrs={'class': 'form-control','placeholder':''}))
    due_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    point_value = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter Point Value...'}))
    assignment_files = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    assignment_status = forms.ChoiceField(choices=STATUS_CHOICES,widget=forms.Select(attrs={'class': 'form-control','placeholder':''}))

    class Meta:
        model = Assignments
        fields = ['assignment_name','assignment_description','due_date','point_value', 'assignment_files', 'assignment_status']

class CreateAssignmentWeight(ModelForm):
    TYPE_CHOICES =(
        ('File Upload','File Upload'),
        ('Homework','Homework'),
        ('Discussion','Discussion'),
        ('Quiz','Quiz'),
        ('Test','Test'),
    )
    assignment_type = forms.ChoiceField(choices=TYPE_CHOICES,widget=forms.Select(attrs={'class': 'form-control','placeholder':''}))
    assignment_weight = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter Weight Value...'}))

    class Meta:
        model = AssignmentWeight
        fields = ['assignment_type','assignment_weight']
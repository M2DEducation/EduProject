from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import ClassList

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Supervisor', 'Supervisor'),
    )
    email = forms.EmailField(max_length=150,widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter email'}))
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':''}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':''}))
    Register_As = forms.ChoiceField(choices=ROLE_CHOICES,widget=forms.Select(attrs={'class': 'form-control','placeholder':''}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    Profile_Image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2','Register_As','Profile_Image')

class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=150,widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # class Meta:
    #     model = User
    #     fields = ('username', 'password',)

class CreateNewClass(ModelForm):
    class_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'English 101'}))
    class_photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = ClassList
        fields = ['class_name','class_photo']
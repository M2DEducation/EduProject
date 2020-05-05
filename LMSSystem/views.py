from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from .models import Profile, ClassList
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.auth.models import Group
from .forms import SignUpForm, LoginForm, CreateNewClass
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def handle_404(request, *args, **kwargs):
    return redirect('home')

# Create your views here.
def activation_sent_view(request):
    return render(request, 'activate-email/activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set Account_Confirmed true
        user.profile.Account_Confirmed = True
        user.save()
        # login(request, user)
        return redirect('loginuser')
    else:
        return render(request, 'activate-email/activation_invalid.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'register/register.html', {'form':SignUpForm()})
    else:
        form = SignUpForm(request.POST, request.FILES)
        if request.method == "POST" and form.is_valid():
            #Create New User
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(username=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password1'])
                    if form.cleaned_data.get('Register_As') == "Student":
                        my_group = Group.objects.get(name='Student')
                        my_group.user_set.add(user)
                    if form.cleaned_data.get('Register_As') == "Teacher":
                        my_group = Group.objects.get(name='Teacher')
                        my_group.user_set.add(user)
                    if form.cleaned_data.get('Register_As') == "Supervisor":
                        my_group = Group.objects.get(name='SchoolAdmin')
                        my_group.user_set.add(user)
                    if form.cleaned_data.get('Profile_Image'):
                        user.profile.Profile_Image = form.cleaned_data.get('Profile_Image')
                    user.profile.email = form.cleaned_data.get('email')
                    user.profile.first_name = form.cleaned_data.get('first_name')
                    user.profile.last_name = form.cleaned_data.get('last_name')
                    user.profile.role = form.cleaned_data.get('Register_As')
                    user.save()
                    current_site = get_current_site(request)
                    subject = 'Please Activate Your Account'
                    # load a template like get_template() 
                    # and calls its render() method immediately.
                    message = render_to_string('activate-email/activation_request.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        # method will generate a hash value with user related data
                        'token': account_activation_token.make_token(user),
                    })
                    user.email_user(subject, message)
                    # login(request, user)
                    return redirect('activation_sent')
                    # return redirect('register')
                except IntegrityError:
                    return render(request, 'register/register.html', {'form':SignUpForm(), 'error':'That username has already been taken. Please choose a different one.'})
            else:
                #Password didnt match
                return render(request, 'register/register.html', {'form':SignUpForm(), 'error':'Passwords did not match'})

def confirmRegistration(request):
    return render(request, 'login-user/login-user.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login-user/loginuser.html', {'form':LoginForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'login-user/loginuser.html', {'form':LoginForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('dashboard')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def home(request):
    # if request.user.is_authenticated:
    #     role = request.user.profile.role
    #     # Supervisor View
    #     if role == "Supervisor":
    #         return redirect('dashboard')
    #     # Teacher View
    #     if role == "Teacher":
    #         return redirect('dashboard')
    #     # Student View
    #     if role == "Student":
    #         return redirect('dashboard')
    # else:
        return render(request, 'home/home.html')

def dashboard(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'teacher-view/index.html')
        # Teacher View
        if role == "Teacher":
            return render(request, 'teacher-view/index.html')
        # Student View
        if role == "Student":
            return render(request, 'student-view/index.html')
    else:
        return redirect('home')

def useradmin(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'useradmin/index.html')
        # Supervisor View
        if role == "Teacher":
            return render(request, 'useradmin/index.html')
        # If Student dont allow useradmin view
        if role == "Student":
            return redirect('dashboard')

def grades(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'grades/index.html')
        # Supervisor View
        if role == "Teacher":
            return render(request, 'grades/index.html')
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'grades/index.html')

def courses(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'courses/index.html')
        # Supervisor View
        if role == "Teacher":
            return render(request, 'courses/index.html')
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'courses/index.html')

def viewcourse(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'courses/course-info/index.html')
        # Supervisor View
        if role == "Teacher":
            return render(request, 'courses/course-info/index.html')
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'courses/course-info/index.html')

def viewlesson(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'courses/course-info/lesson/index.html')
        # Supervisor View
        if role == "Teacher":
            return render(request, 'courses/course-info/lesson/index.html')
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'courses/course-info/lesson/index.html')

def students(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'students/index.html')
        # Supervisor View
        if role == "Teacher":
            return render(request, 'students/index.html')
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'students/index.html')

def profile(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'profile/index.html')
        # Supervisor View
        if role == "Teacher":
            return render(request, 'profile/index.html')
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'profile/index.html')

def notifications(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'messages/index.html')
        # Supervisor View
        if role == "Teacher":
            return render(request, 'messages/index.html')
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'messages/index.html')

def attendance(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'attendance/index.html')
        # Supervisor View
        if role == "Teacher":
            return render(request, 'attendance/index.html')
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'attendance/index.html')



def createclass(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            listclasses = ClassList.objects.filter(user=request.user)
            return render(request, 'createclass/index.html', {'listclasses':listclasses,'newclassform':CreateNewClass()})
        else:
            try:
                form = CreateNewClass(request.POST, request.FILES)
                newclass = form.save(commit=False)
                newclass.user = request.user
                newclass.save()
                return redirect('createclass') 
            except ValueError:
                return render(request, 'createclass/index.html', {'listclasses':listclasses,'form':CreateNewClass(), 'error':'Data is bad please retry'})

def recordmanagement(request):
    if request.user.is_authenticated:
        return render(request, 'useradmin/record-management/index.html')

def administrationannouncements(request):
    if request.user.is_authenticated:
        return render(request, 'useradmin/announcements/index.html')

def administrationinvoices(request):
    if request.user.is_authenticated:
        return render(request, 'useradmin/invoices/index.html')

def calendar(request):
    if request.user.is_authenticated:
        return render(request, 'calendar/index.html')

def assignments(request):
    if request.user.is_authenticated:
        return render(request, 'assignments/index.html')

def messages(request):
    if request.user.is_authenticated:
        return render(request, 'messages/index.html')

def forum(request):
    if request.user.is_authenticated:
        return render(request, 'forum/index.html')
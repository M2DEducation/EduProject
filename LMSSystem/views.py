from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from .models import m2dAnnouncements, Profile, ClassList, ClassListGroupCode, ClassListGroup, Assignments, AssignmentWeight, StudentAssignments, classannouncements
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.auth.models import Group
from .forms import SignUpForm, LoginForm, CreateNewClass, CreateNewAssignment, CreateAssignmentWeight
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
                        checkCode = ClassListGroupCode.objects.filter(class_group_code=request.POST['Teacher_Registration_Code']).first()
                        if not checkCode:
                            return render(request, 'register/register.html', {'form':SignUpForm(), 'regError':'Invalid teacher registration code.'})
                        else:
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
                            student_class = ClassListGroup.objects.get_or_create(code_id=checkCode,class_id=checkCode.class_id,user=user)
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
                        return render(request, 'register/register.html', {'form':SignUpForm(), 'regError':'That username has already been taken. Please choose a different one.'})
            else:
                #Password didnt match
                return render(request, 'register/register.html', {'form':SignUpForm(), 'regError':'Passwords did not match'})

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
        getSysAnnouncements = m2dAnnouncements.objects.filter()
        listclasses = ClassList.objects.filter(user=request.user)
        liststudents = ClassListGroup.objects.filter(class_id__in=listclasses)
        getClassAnnouncements = classannouncements.objects.filter(class_id__in=(listclasses))
        # listassignments = Assignments.objects.filter(class_id=course)
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'dashboard/index.html', {'pagename':'Dashboard', 'systemannouncements':getSysAnnouncements, 'classannouncements':getClassAnnouncements, 'listclasses':listclasses, 'liststudents':liststudents})
        # Teacher View
        if role == "Teacher":
            return render(request, 'dashboard/index.html', {'pagename':'Dashboard', 'systemannouncements':getSysAnnouncements, 'classannouncements':getClassAnnouncements, 'listclasses':listclasses, 'liststudents':liststudents})
        # Student View
        if role == "Student":
            return render(request, 'dashboard/index.html', {'pagename':'Dashboard', 'systemannouncements':getSysAnnouncements, 'classannouncements':getClassAnnouncements, 'listclasses':listclasses, 'liststudents':liststudents})
    else:
        return redirect('home')
        
def announcements(request):
    if request.user.is_authenticated:
        return render(request, 'announcements/index.html', {'pagename':'Announcements'})

def useradmin(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'useradmin/index.html', {'pagename':'Administration'})
        # Supervisor View
        if role == "Teacher":
            return render(request, 'useradmin/index.html', {'pagename':'Administration'})
        # If Student dont allow useradmin view
        if role == "Student":
            return redirect('dashboard')

def grades(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        getMyCourses = ClassList.objects.filter(user=request.user)
        listassignments = StudentAssignments.objects.filter(class_id__in=(getMyCourses))
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'grades/index.html', {'pagename':'Grades', 'listassignments':listassignments})
        # Supervisor View
        if role == "Teacher":
            return render(request, 'grades/index.html', {'pagename':'Grades', 'listassignments':listassignments})
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'grades/index.html', {'pagename':'Grades', 'listassignments':listassignments})

def courses(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'courses/index.html', {'pagename':'Courses'})
        # Supervisor View
        if role == "Teacher":
            return render(request, 'courses/index.html', {'pagename':'Courses'})
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'courses/index.html', {'pagename':'Courses'})

def viewcourse(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'courses/course-info/index.html', {'pagename':'Course'})
        # Supervisor View
        if role == "Teacher":
            return render(request, 'courses/course-info/index.html', {'pagename':'Course'})
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'courses/course-info/index.html', {'pagename':'Course'})

def viewlesson(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'courses/course-info/lesson/index.html', {'pagename':'Lesson'})
        # Supervisor View
        if role == "Teacher":
            return render(request, 'courses/course-info/lesson/index.html', {'pagename':'Lesson'})
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'courses/course-info/lesson/index.html', {'pagename':'Lesson'})

def students(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'students/index.html', {'pagename':'Students'})
        # Supervisor View
        if role == "Teacher":
            return render(request, 'students/index.html', {'pagename':'Students'})
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'students/index.html', {'pagename':'Students'})

def profile(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'profile/index.html', {'pagename':'Profile'})
        # Supervisor View
        if role == "Teacher":
            return render(request, 'profile/index.html', {'pagename':'Profile'})
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'profile/index.html', {'pagename':'Profile'})

def notifications(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'messages/index.html', {'pagename':'Notifications'})
        # Supervisor View
        if role == "Teacher":
            return render(request, 'messages/index.html', {'pagename':'Notifications'})
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'messages/index.html', {'pagename':'Notifications'})

def attendance(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        # Supervisor View
        if role == "Supervisor":
            return render(request, 'attendance/index.html', {'pagename':'Attendance'})
        # Supervisor View
        if role == "Teacher":
            return render(request, 'attendance/index.html', {'pagename':'Attendance'})
        # If Student dont allow useradmin view
        if role == "Student":
            return render(request, 'attendance/index.html', {'pagename':'Attendance'})



def coursemanagement(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            course = request.GET.get('c')
            listclasses = ClassList.objects.filter(user=request.user)
            liststudents = ClassListGroup.objects.filter(class_id=course)
            listassignments = Assignments.objects.filter(class_id=course)
            assignmentweights = AssignmentWeight.objects.filter(class_id=course)
            if listclasses and course:
                showcourse = ClassList.objects.filter(user=request.user,class_id=course)
                return render(request, 'coursemanagement/index.html', {'pagename':'Course Management','courseexist':"classandcourse",'listclasses':listclasses,'liststudents':liststudents,'listassignments':listassignments,'assignmentweights':assignmentweights,'showcourse':showcourse,'newclassform':CreateNewClass(),'newAssignment':CreateNewAssignment(),'createweight':CreateAssignmentWeight()})
            elif listclasses:
                return render(request, 'coursemanagement/index.html', {'pagename':'Course Management','courseexist':"course",'listclasses':listclasses,'listassignments':listassignments,'newclassform':CreateNewClass(),'newAssignment':CreateNewAssignment()})
            else:
                return render(request, 'coursemanagement/index.html', {'pagename':'Course Management','courseexist':"none",'newclassform':CreateNewClass()})                
        else:
            course = request.GET.get('c')
            listclasses = ClassList.objects.filter(user=request.user)
            listassignments = Assignments.objects.filter(class_id=course)
            getcourse_id = ClassList.objects.get(class_id=course)
            assignmentweights = AssignmentWeight.objects.filter(class_id=course)
            if request.method == "POST" and 'newclass' in request.POST:
                # find new code
                # getNewCode = ""
                # while True:
                #     getNewCode = get_random_string(length=32)
                #     checkCodeExist = ClassListGroupCode.objects.filter(class_group_code=getNewCode)
                #     if checkCodeExist is None:
                #         break;
                # start form
                form = CreateNewClass(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        newclass = form.save(commit=False)
                        newclass.user = request.user
                        newclass.save()
                        getNewCourse = ClassList.objects.get(class_id=newclass.pk).pk
                        setreturn = '/course-management/?c='+str(getNewCourse)
                        return redirect(setreturn)                            
                    except ValueError:
                        return render(request, 'coursemanagement/index.html', {'pagename':'Course Management','listclasses':listclasses,'listassignments':listassignments,'form':CreateNewClass(), 'error':'Data is bad please retry','newAssignment':CreateNewAssignment()})
            elif request.method == "POST" and 'createassignment' in request.POST:
                form = CreateNewAssignment(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        newassignment = form.save(commit=False)
                        newassignment.class_id = getcourse_id
                        newassignment.save()
                        getMyStudents = ClassListGroup.objects.filter(class_id=getcourse_id)
                        for row in getMyStudents:
                            makeStudentAssignments = StudentAssignments.objects.get_or_create(class_id=getcourse_id,user=row.user,code_id=row.code_id,assignment_id=newassignment)
                        if listclasses and course:
                            return redirect('/course-management/?c='+course)
                    except ValueError:
                        return render(request, 'coursemanagement/index.html', {'pagename':'Course Management','listclasses':listclasses,'listassignments':listassignments,'form':CreateNewClass(), 'error':'Data is bad please retry','newAssignment':CreateNewAssignment()})       
            elif request.method == "POST" and 'createweight' in request.POST:
                form = CreateAssignmentWeight(request.POST)
                if form.is_valid():
                    try:
                        newweight = form.save(commit=False)
                        newweight.class_id = getcourse_id
                        newweight.save()
                        return redirect('/course-management/?c='+course)
                    except ValueError:
                        return render(request, 'coursemanagement/index.html', {'pagename':'Course Management','listclasses':listclasses,'listassignments':listassignments,'form':CreateNewClass(), 'error':'Data is bad please retry','newAssignment':CreateNewAssignment(), 'createweight':CreateAssignmentWeight()})       
            else:
                return render(request, 'coursemanagement/index.html', {'pagename':'Course Management','listclasses':listclasses,'listassignments':listassignments,'newclassform':CreateNewClass(),'newAssignment':CreateNewAssignment()})



def recordmanagement(request):
    if request.user.is_authenticated:
        return render(request, 'useradmin/record-management/index.html', {'pagename':'Record Management'})

def administrationannouncements(request):
    if request.user.is_authenticated:
        return render(request, 'useradmin/announcements/index.html', {'pagename':'Administrative Announcements'})

def administrationinvoices(request):
    if request.user.is_authenticated:
        return render(request, 'useradmin/invoices/index.html', {'pagename':'Administrative Invoices'})

def calendar(request):
    if request.user.is_authenticated:
        return render(request, 'calendar/index.html', {'pagename':'Calendar'})

def assignments(request):
    if request.user.is_authenticated:
        return render(request, 'assignments/index.html', {'pagename':'Assignments'})

def messages(request):
    if request.user.is_authenticated:
        return render(request, 'messages/index.html', {'pagename':'Messages'})

def forum(request):
    if request.user.is_authenticated:
        return render(request, 'forum/index.html', {'pagename':'Forum'})
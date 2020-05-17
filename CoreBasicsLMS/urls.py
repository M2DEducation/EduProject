"""CoreBasicsLMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from LMSSystem import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.loginuser, name='loginuser'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # SchoolAdmin Views
    path('administration/', views.useradmin, name='useradmin'),
    path('administration/record-management/', views.recordmanagement, name='recordmanagement'),
    path('administration/announcements/', views.administrationannouncements, name='administrationannouncements'),
    path('administration/invoices/', views.administrationinvoices, name='administrationinvoices'),

    # User views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('announcements/', views.announcements, name='announcements'),
    path('course-management/', views.coursemanagement, name='coursemanagement'),
    path('course-management/?c<courseID>', views.coursemanagement, name='coursemanagement'),
    path('course-management/?c<courseID>&q=<quizId>', views.coursemanagement, name='coursemanagement'),
    path('notifications/', views.notifications, name='notifications'),
    path('grades/', views.grades, name='grades'),
    path('courses/', views.courses, name='courses'),
    path('courses/1', views.viewcourse, name='viewcourse'),
    path('courses/1/lesson-1', views.viewlesson, name='viewlesson'),
    path('students/', views.students, name='students'),
    path('attendance/', views.attendance, name='attendance'),
    path('profile/', views.profile, name='profile'),
    path('calendar/', views.calendar, name='calendar'),
    path('assignments/', views.assignments, name='assignments'),
    path('messages/', views.messages, name='messages'),
    path('forum/', views.forum, name='forum'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'LMSSystem.views.handle_404'
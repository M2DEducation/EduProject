from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

# Admin Models
class m2dAnnouncements(models.Model):
    IMPORTANCE_CHOICES = (
        ('General','General'),
        ('Important','Important'),
        ('Critical','Critical'),
    )
    m2dannouncement_id = models.AutoField(primary_key=True)
    message_importance = models.CharField(max_length=9,choices=IMPORTANCE_CHOICES, blank=False, default="General")
    message_content = models.TextField(blank=False,default="Announcement Coming Soon")
    message_attachments = models.FileField(upload_to ='system/',blank=True)
    message_expiration_date = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateField(auto_now=True)

# School Models
class Profile(models.Model):
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Supervisor', 'Supervisor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES, null=True, blank=False)
    Account_Confirmed = models.BooleanField(default=False)
    Profile_Image = models.ImageField(upload_to ='uploads/',blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class ClassList(models.Model):
    class_id = models.AutoField(primary_key=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classlist")
    class_name = models.CharField(max_length=100, blank=False, default="Pending")
    class_subject = models.CharField(max_length=100, blank=False, default="Pending")
    class_description = models.TextField(blank=False,default="Pending")
    class_photo = models.ImageField(upload_to ='classphotos/',blank=True, null=True)
    syllabus_file = models.FileField(upload_to ='syllabus/',blank=True)

    def __iter__(self):
        return [ self.class_id, 
                 self.user, 
                 self.class_name,
                 self.class_subject,
                 self.class_description, 
                 self.class_photo,
                 self.syllabus_file ]

class ClassListGroupCode(models.Model):
    code_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    class_group_name = models.CharField(max_length=100, blank=False, default="Class 1")
    class_group_code = models.CharField(max_length=32, blank=False, default="00000000000000000000000000000000")

class ClassListGroup(models.Model):
    class_group_id = models.AutoField(primary_key=True)
    code_id = models.ForeignKey(ClassListGroupCode, on_delete=models.CASCADE)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="codeassignment")

class Assignments(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Published', 'Published'),
        ('Late', 'Late'),
    )
    TYPE_CHOICES =(
        ('Pending','Pending'),
        ('File Upload','File Upload'),
        ('Homework','Homework'),
        ('Discussion','Discussion'),
        ('Quiz','Quiz'),
        ('Test','Test'),
    )
    assignment_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    assignment_name = models.CharField(max_length=255, blank=False, null=False, default="None")
    assignment_description = models.TextField(blank=False,default="Pending")
    assignment_type = models.CharField(max_length=11,choices=TYPE_CHOICES, null=False, blank=False, default="Pending")
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    point_value = models.IntegerField(blank=False,null=False,default=0)
    assignment_files = models.FileField(upload_to ='assignments/',blank=True)
    assignment_status = models.CharField(max_length=10,choices=STATUS_CHOICES, null=False, blank=False, default="Pending")

class AssignmentWeight(models.Model):
    TYPE_CHOICES =(
        ('File Upload','File Upload'),
        ('Homework','Homework'),
        ('Discussion','Discussion'),
        ('Quiz','Quiz'),
        ('Test','Test'),
    )
    assignment_weight_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    assignment_type = models.CharField(max_length=11,choices=TYPE_CHOICES, null=False, blank=False, default="Pending")
    assignment_weight = models.IntegerField(blank=False,null=False,default=0)

class Question(models.Model):
    TYPE_CHOICES =(
        ('Multiple Choice','Multiple Choice'),
        ('Fill In The Blank','Fill In The Blank'),
        ('Short Response','Short Response'),
        ('Essay','Essay'),
        ('Pending','Pending'),
    )
    question_id = models.AutoField(primary_key=True)
    assignment_type = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=17,choices=TYPE_CHOICES, null=False, blank=False, default="Pending")
    question = models.TextField(blank=False,default="Pending")
    is_active = models.BooleanField(blank=False,default=True)

class Question_choices(models.Model):
    choice_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_right_choice = models.BooleanField(blank=False,default=False)
    answer = models.TextField(blank=False,default="Pending")

class User_question_answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Question_choices, on_delete=models.CASCADE, related_name="questionchoice")
    is_right_choice = models.ForeignKey(Question_choices, on_delete=models.CASCADE)
    answer_time = models.DateTimeField()

class StudentAssignments(models.Model):
    STATUS_CHOICES =(
        ('Not Submitted','Not Submitted'),
        ('Submitted - Not Graded','Submitted - Not Graded'),
        ('Graded','Graded'),
        ('Late','Late'),
        ('Resubmitted','Resubmitted'),
    )
    student_assignment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    code_id = models.ForeignKey(ClassListGroupCode, on_delete=models.CASCADE)
    assignment_id = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    assignment_grade = models.IntegerField(blank=True,null=True)
    assignment_status = models.CharField(max_length=22,choices=STATUS_CHOICES, null=False, blank=False, default="Not Submitted")

class classannouncements(models.Model):
    PIN_CHOICES =(
        ('Yes','Yes'),
        ('No','No'),
    )
    IMPORTANCE_CHOICES = (
        ('General','General'),
        ('Important','Important'),
        ('Critical','Critical'),
    )
    MESSAGE_TYPE = (
        ('Assignment Posted','Assignment Posted'),
        ('General Announcement','General Announcement'),
        ('Class Cancelled','Class Cancelled'),
    )
    class_announcement_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    message_content = models.TextField(blank=False,default="Pending")
    message_type = models.CharField(max_length=30,choices=MESSAGE_TYPE, blank=False, default="General Announcement")
    message_importance = models.CharField(max_length=9,choices=IMPORTANCE_CHOICES, blank=False, default="General")
    pinned_message = models.CharField(max_length=3,choices=PIN_CHOICES, blank=False, default="No")
    message_expiration_date = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateField(auto_now=True)

class GroupMessageChat(models.Model):
    group_chat_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    class_group_id = models.ForeignKey(ClassListGroup, on_delete=models.CASCADE)
    assignment_id = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=True)

class GroupChatMembers(models.Model):
    group_chat_id = models.ForeignKey(GroupMessageChat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class GroupChatMessages(models.Model):
    PIN_CHOICES =(
        ('Yes','Yes'),
        ('No','No'),
    )
    group_msg_id = models.AutoField(primary_key=True)
    group_chat_id = models.ForeignKey(GroupMessageChat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_content = models.TextField(blank=False,default="Pending")
    pinned_message = models.CharField(max_length=3,choices=PIN_CHOICES, null=False, blank=False, default="No")
    msg_dts = models.DateTimeField(auto_now_add=True)

class UserMessageGroupActions(models.Model):
    group_msg_id = models.ForeignKey(GroupChatMessages, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_read = models.BooleanField(blank=False,default=False)
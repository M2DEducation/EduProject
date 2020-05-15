from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

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
    class_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    class_group_code = models.CharField(max_length=32, blank=False, default=get_random_string(length=32))

class ClassListGroup(models.Model):
    class_group_id = models.AutoField(primary_key=True)
    code_id = models.ForeignKey(ClassListGroupCode, on_delete=models.CASCADE)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="codeassignment")

class AssignmentType(models.Model):
    assignment_type_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    assignment_type = models.CharField(max_length=100, blank=False, null=False, default="None")

class Assignments(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Published', 'Published'),
        ('Late', 'Late'),
    )
    TYPE_CHOICES =(
        ('File Upload','File Upload'),
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
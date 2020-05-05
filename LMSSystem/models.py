from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    class_name = models.CharField(max_length=100, blank=False)
    class_description = models.TextField(blank=False,default="N/a")
    class_photo = models.ImageField(upload_to ='classphotos/',blank=True)

    def __iter__(self):
        return [ self.class_id, 
                 self.user, 
                 self.class_name, 
                 self.class_description, 
                 self.class_photo ]
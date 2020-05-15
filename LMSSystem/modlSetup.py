# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# User Account Creation additional info
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

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# School Information (for school system integration)

class ClassList(models.Model):
    class_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100, blank=False)
    class_photo = models.ImageField(upload_to ='classphotos/',blank=True)

    def __iter__(self):
        return [ self.class_id, 
                 self.user, 
                 self.class_name, 
                 self.class_photo ]

class ClassSyllabus(models.Model):
    syllabus_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    syllabus_file = models.FileField(upload_to ='syllabus/',blank=True)
    class_description = models.TextField(blank=False,default="N/a")
    class_learning_outcomes = models.TextField(blank=False,default="N/a")
    required_materials = models.TextField(blank=False,default="N/a")
    class_goals = models.TextField(blank=False,default="N/a")
    class_grading_scale = models.TextField(blank=False,default="N/a")
    class_prerequisites = models.TextField(blank=False,default="N/a")
    class_policies = models.TextField(blank=False,default="N/a")

# Below will populate in the syllabus section if no file url used
class ClassLessons(models.Model):
    class_lesson_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    chapter_num
    lesson_num
    date_due
    lesson_attachments

class SchoolInfo(models.Model):
    school_id = models.AutoField(primary_key=True)
    district
    county
    zoning
    school_name
    email
    address_1
    address_2
    city
    state
    zip
    country

class StaffType(models.Model):
    staff_type_id = models.AutoField(primary_key=True)
    school_id
    staff_type

class SchoolStaffInfo(models.Model):
    staff_list_id = models.AutoField(primary_key=True)
    school_id
    staff_type_id
    user

class SchoolTeacherList(models.Model):
    school_teacher_list_id = models.AutoField(primary_key=True)
    school_id ForeignKey
    teacher_id ForeignKey
    teacher_state_id #can be null
    teacher_private_school_id #can be null

class SchoolStudentList(models.Model):
    school_student_list_id = models.AutoField(primary_key=True)
    school_id ForeignKey
    student_id ForeignKey
    student_state_id #can be null
    student_private_school_id #can be null

class SchoolPeriodList(models.Model):
    period_id = models.AutoField(primary_key=True)
    school_id
    period_name
    start_time
    end_time

class SchoolRoomTypes(models.Model):
    room_type_id = models.AutoField(primary_key=True)
    room_type_name

class SchoolRoomList(models.Model):
    room_id = models.AutoField(primary_key=True)
    school_id
    room_type_id
    room_name
    gps_coords

class SchoolEquipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    school_id
    room_id
    equipment_name

class SchoolSubject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    school_id
    subject_name

class SchoolClass(models.Model):
    school_class_id = models.AutoField(primary_key=True)
    class_id
    school_id
    period_id
    room_id
    subject_id

class ClassStudents(models.Model):
    class_students_id = models.AutoField(primary_key=True)
    school_id #can be null
    period_id #can be null
    class_id
    user

class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    school_id
    period_id
    room_id
    subject_id
    class_id
    gps_id
    user

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    school_id
    class_id
    user
    attendance_date
    attendance_status

class Assignments(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_type_id = models.ForeignKey()
    class_id = models.ForeignKey(ClassList)

class Grades(models.Model):
    grade_id = models.AutoField(primary_key=True)

class SystemMessages(models.Model):
    sys_message_id = models.AutoField(primary_key=True)
    sender_id
    recipient_id
    message_importance
    message_content
    message_attachments
    message_reaction
    message_read

class AnnouncementMessages(models.Model):
    announcement_message_id = models.AutoField(primary_key=True)
    sender_id
    recipient_id
    message_importance
    message_content
    message_attachments
    message_reaction
    message_read

class CourseMessages(models.Model):
    course_message_id = models.AutoField(primary_key=True)
    sender_id
    recipient_id
    message_importance
    message_content
    message_attachments
    message_reaction
    message_read

class PrivateMessages(models.Model):
    private_message_id = models.AutoField(primary_key=True)
    sender_id
    recipient_id
    message_importance
    message_content
    message_attachments
    message_reaction
    message_read

class Invoices(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    school_id
    period_id
    class_id
    recipient_id
    invoice_name
    amount_due
    remainder
    is_paid
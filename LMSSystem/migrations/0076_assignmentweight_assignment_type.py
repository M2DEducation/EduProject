# Generated by Django 3.0.3 on 2020-05-18 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMSSystem', '0075_remove_assignmentweight_assignment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentweight',
            name='assignment_type',
            field=models.CharField(choices=[('File Upload', 'File Upload'), ('Homework', 'Homework'), ('Discussion', 'Discussion'), ('Quiz', 'Quiz'), ('Test', 'Test')], default='Pending', max_length=11),
        ),
    ]
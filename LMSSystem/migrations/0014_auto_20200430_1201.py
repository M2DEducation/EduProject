# Generated by Django 3.0.3 on 2020-04-30 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMSSystem', '0013_auto_20200430_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Supervisor', 'Supervisor')], max_length=10, null=True),
        ),
    ]
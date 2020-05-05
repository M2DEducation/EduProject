# Generated by Django 3.0.3 on 2020-04-28 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMSSystem', '0003_remove_profile_signup_confirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Student'), (2, 'Teacher'), (3, 'Supervisor')], null=True),
        ),
    ]
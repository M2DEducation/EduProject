# Generated by Django 3.0.3 on 2020-04-28 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMSSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Account_Confirmed',
            field=models.BooleanField(default=False),
        ),
    ]

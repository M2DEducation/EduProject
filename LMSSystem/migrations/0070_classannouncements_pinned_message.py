# Generated by Django 3.0.3 on 2020-05-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMSSystem', '0069_auto_20200517_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='classannouncements',
            name='pinned_message',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=3),
        ),
    ]

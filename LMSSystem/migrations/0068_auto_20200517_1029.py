# Generated by Django 3.0.3 on 2020-05-17 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMSSystem', '0067_auto_20200517_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlistgroupcode',
            name='class_group_code',
            field=models.CharField(default='00000000000000000000000000000000', max_length=32),
        ),
    ]

# Generated by Django 3.0.3 on 2020-05-14 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LMSSystem', '0036_auto_20200514_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classlistgroup',
            name='class_group_code',
        ),
        migrations.RemoveField(
            model_name='classlistgroup',
            name='class_group_name',
        ),
        migrations.CreateModel(
            name='ClassListGroupCode',
            fields=[
                ('ClassListGroupCode_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_group_name', models.CharField(default='Class 1', max_length=100)),
                ('class_group_code', models.CharField(default='RAmEWFl9SAu5r4RD8GcZc6hZzrZsdFMt', max_length=32)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMSSystem.ClassList')),
            ],
        ),
    ]

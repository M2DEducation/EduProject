# Generated by Django 3.0.3 on 2020-05-14 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMSSystem', '0037_auto_20200514_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classlistgroupcode',
            old_name='ClassListGroupCode_id',
            new_name='code_id',
        ),
        migrations.AlterField(
            model_name='classlistgroupcode',
            name='class_group_code',
            field=models.CharField(default='j9sqozRczfHmy9BB0XG0PNLcB7UH8gZh', max_length=32),
        ),
    ]

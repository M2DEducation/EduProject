# Generated by Django 3.0.3 on 2020-05-14 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMSSystem', '0040_auto_20200514_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlistgroupcode',
            name='class_group_code',
            field=models.CharField(default='6SQ7hSFAcAE9PB0KCeLD7DG8HCIXL3NL', max_length=32),
        ),
        migrations.DeleteModel(
            name='ClassListGroup',
        ),
    ]
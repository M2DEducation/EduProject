# Generated by Django 3.0.3 on 2020-05-16 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LMSSystem', '0058_auto_20200516_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='classlistgroupcode',
            name='class_group_code',
            field=models.CharField(default='Xm4RzPDtR4Cid4sblxpsSjmI4RvzkIYZ', max_length=32),
        ),
    ]

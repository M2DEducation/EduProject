# Generated by Django 3.0.3 on 2020-05-15 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LMSSystem', '0044_auto_20200515_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlistgroup',
            name='class_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMSSystem.ClassList'),
        ),
        migrations.AlterField(
            model_name='classlistgroup',
            name='code_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMSSystem.ClassListGroupCode'),
        ),
        migrations.AlterField(
            model_name='classlistgroup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='classlistgroupcode',
            name='class_group_code',
            field=models.CharField(default='mbuhEHB98FKGFKQGjbKhB6IfcAgJ5yW9', max_length=32),
        ),
    ]

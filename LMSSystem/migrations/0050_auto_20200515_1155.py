# Generated by Django 3.0.3 on 2020-05-15 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LMSSystem', '0049_auto_20200515_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlistgroupcode',
            name='class_group_code',
            field=models.CharField(default='JdNBeBaQObdr9iZylUReShM1OvNO7iGh', max_length=32),
        ),
        migrations.CreateModel(
            name='ClassListGroup',
            fields=[
                ('class_group_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMSSystem.ClassList')),
                ('code_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMSSystem.ClassListGroupCode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='codeassignment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
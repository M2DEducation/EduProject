# Generated by Django 3.0.3 on 2020-05-14 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMSSystem', '0026_auto_20200514_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='assignment_type',
            field=models.CharField(choices=[('File Upload', 'File Upload'), ('Discussion', 'Discussion'), ('Quiz', 'Quiz'), ('Test', 'Test')], default='Pending', max_length=11),
        ),
    ]

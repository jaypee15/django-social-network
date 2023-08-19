# Generated by Django 4.2.4 on 2023-08-19 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0005_alter_profile_job_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='job_type',
            field=models.CharField(choices=[('Full Time', 'full time'), ('Contract', 'contract'), ('Freelance', 'freelance')], default='Full Time', max_length=20),
        ),
    ]

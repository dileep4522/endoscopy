# Generated by Django 5.1.3 on 2024-12-03 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dev_pro', '0002_alter_userdetails_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientsdetails',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='patientsdetails',
            name='mobile',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='mobile_no',
            field=models.CharField(max_length=15),
        ),
    ]
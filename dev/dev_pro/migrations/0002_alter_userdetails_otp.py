# Generated by Django 5.1.3 on 2024-12-03 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dev_pro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

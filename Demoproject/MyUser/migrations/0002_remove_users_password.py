# Generated by Django 5.1.1 on 2024-09-10 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyUser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='password',
        ),
    ]

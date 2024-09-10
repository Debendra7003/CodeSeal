# Generated by Django 5.1.1 on 2024-09-10 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyUser', '0002_remove_users_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(max_length=128)),
                ('phone_number', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('resume_link', models.URLField(blank=True, null=True)),
                ('deleted_time', models.DateTimeField(blank=True, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Users(models.Model):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    image_url = models.URLField(null=True, blank=True)
    resume_link = models.URLField(null=True, blank=True)
    deleted_time = models.DateTimeField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Hash the password and save it."""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Check if the raw password matches the hashed password."""
        return check_password(raw_password, self.password)

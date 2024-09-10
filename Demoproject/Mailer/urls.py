# mailer/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.email_upload_view, name='upload'),
    path('send/', views.send_emails, name='send_emails'),
]

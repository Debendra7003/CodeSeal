from django.db import models


class EmailUpload(models.Model):
    email_file = models.FileField(upload_to='emails/')
    template_file = models.FileField(upload_to='templates/')

    def __str__(self):
        return self.email_file.name

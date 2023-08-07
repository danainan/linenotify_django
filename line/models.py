from django.db import models

# Create your models here.
class Lines(models.Model):
    message = models.CharField(max_length=250)
    imageDisplay = models.FileField()

from django.db import models

# Create your models here.

class User(models.Model):
    username_text = models.CharField(max_length=50, unique=True)
    password_text = models.CharField(max_length=50)
    def __str__(self):
        return self.username_text
from django.db import models

# Create your models here.
class Project(models.Model):
    projectNumber_text = models.CharField(max_length=50)
    projectName_text = models.CharField(max_length=200)
    startDate = models.DateField(auto_now=False, auto_now_add=False)
    projectManager_text = models.CharField(max_length=50)
    projectDes_text = models.TextField(max_length=500)

    def __str__(self):
        return self.projectName_text

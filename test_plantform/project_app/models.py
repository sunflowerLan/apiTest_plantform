from django.db import models

# Create your models here.
class Project(models.Model):
    """
    项目表
    """
    name = models.CharField("项目名称", max_length=100, blank=False, default="")
    describe = models.TextField("项目描述", default="")
    status = models.BooleanField("项目状态", default=True)
    create_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.name

class Module(models.Model):
    """
    模块表
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("模块名称", max_length=100, blank=False, default="")
    describe = models.TextField("模块描述", default="")
    create_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.name


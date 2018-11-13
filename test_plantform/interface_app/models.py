from django.db import models
from project_app.models import Module

# Create your models here.
class TestCase(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name="模块名称")
    name = models.CharField("接口名称", max_length=200, blank=False, default="")
    url = models.TextField("URL地址", default="")
    req_method = models.CharField("请求方法", max_length=50, default="")
    req_type = models.CharField("请求参数类型", max_length=50, default="")
    req_header = models.TextField("请求头", default="")
    req_parameter = models.TextField("请求参数", default="")
    response_assert = models.TextField("预期结果", default="")
    create_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.name
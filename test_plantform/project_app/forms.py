from django.forms import ModelForm
from .models import Project

# 方法一：直接继承Form
# class ProjectForm(forms.Form):
#     name = forms.CharField(label="项目名称", max_length=100)
#     status = forms.BooleanField(label="项目状态", required=False)
#     # create_time = forms.DateTimeField(label="创建时间")
#     describe = forms.CharField(label="项目描述", widget=forms.Textarea)

# 方法二：结合Model，继承django.forms.ModelForm

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # 只显示model中指定的字段
        # field = ('name', 'describe', 'status')

        # 屏蔽的字段
        exclude = ['create_time']
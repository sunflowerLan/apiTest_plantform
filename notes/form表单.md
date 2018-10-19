


# form 表单字段详解
from django import forms
class RegForm(forms.Form):
    u = forms.CharField(max_length=10
    ,error_messages={"max_length":"最长10字符"，"required":"字段不能为空"})
    p = forms.CharField(mix_length=8,
    widget=widgets.PasswordInput(attrs={"placeholder":"password"})
    gender = forms.CharField(initial=2,
    widget=widgets.Select(choices=((1,'上海'),(2,'北京'),)))
    email = forms.EmailField()
    is_married = forms.BooleanField(required=False)
)

# 表单定义
## 方法一：直接继承Form
class ProjectForm(forms.Form):
    name = forms.CharField(label="项目名称", max_length=100)
    status = forms.BooleanField(label="项目状态", required=False)
    describe = forms.CharField(label="项目描述", widget=forms.Textarea)

## 方法二：结合Model，继承django.forms.ModelForm
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # 只显示model中指定的字段
        # field = ('name', 'describe', 'status')

        # 屏蔽的字段
        exclude = ['create_time']
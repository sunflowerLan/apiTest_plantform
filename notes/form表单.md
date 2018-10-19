


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
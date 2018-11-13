from django.forms import ModelForm
from .models import TestCase

class TestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        exclude = ["create_time"]
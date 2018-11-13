from django.contrib import admin
from .models import TestCase
# Register your models here.

class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['module', 'name', 'url', 'req_method',
                    'req_type', 'req_header', 'req_parameter', 'response_assert']

admin.site.register(TestCase, TestCaseAdmin)
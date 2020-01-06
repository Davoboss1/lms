from django.contrib import admin
from .models import Lecturer,Dean,Head_of_Department,Welfare,leave_request
# Register your models here.
admin.site.register(Lecturer)
admin.site.register(Dean)
admin.site.register(Head_of_Department)
admin.site.register(Welfare)
admin.site.register(leave_request)
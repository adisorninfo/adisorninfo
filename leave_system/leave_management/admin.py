from django.contrib import admin
from .models import Department, Employee, LeaveType, LeaveRequest, AttendanceRecord

# Register your models here.
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(LeaveType)
admin.site.register(LeaveRequest)
admin.site.register(AttendanceRecord)

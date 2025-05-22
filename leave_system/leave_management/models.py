from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class LeaveType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=100)
    remaining_leave_days_sick = models.IntegerField(default=0)
    remaining_leave_days_personal = models.IntegerField(default=0)
    remaining_leave_days_vacation = models.IntegerField(default=0)
    is_supervisor = models.BooleanField(default=False)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')

    def __str__(self):
        return self.user.username if self.user else self.employee_id

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    supporting_document = models.FileField(upload_to='supporting_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leave_requests')

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"

class AttendanceRecord(models.Model):
    ATTENDANCE_TYPES = [
        ('Late', 'Late'),
        ('Absent', 'Absent'),
        ('Early Leave', 'Early Leave'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    type = models.CharField(max_length=20, choices=ATTENDANCE_TYPES)
    reason = models.TextField(null=True, blank=True)
    actual_check_in = models.TimeField(null=True, blank=True)
    actual_check_out = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.type} on {self.date}"

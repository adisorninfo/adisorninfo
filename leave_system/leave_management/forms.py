from django import forms
from django.contrib.auth.models import User # Ensure User is imported
from .models import Employee, Department # Department was used in the original EmployeeForm widgets

class EmployeeForm(forms.ModelForm):
    # User fields
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    # Consider adding a password confirmation field here for better UX in a real application.

    class Meta:
        model = Employee
        # Order fields for logical grouping in the form
        fields = ['username', 'email', 'password', # User fields
                  'employee_id', 'department', 'position', 'is_supervisor', 'supervisor',
                  'remaining_leave_days_sick', 'remaining_leave_days_personal', 'remaining_leave_days_vacation']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'is_supervisor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'supervisor': forms.Select(attrs={'class': 'form-control'}),
            'remaining_leave_days_sick': forms.NumberInput(attrs={'class': 'form-control'}),
            'remaining_leave_days_personal': forms.NumberInput(attrs={'class': 'form-control'}),
            'remaining_leave_days_vacation': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        # Exclude user creation fields (username, email, password)
        # User details (username, email) should ideally be updated via a separate profile/admin page for that user.
        # Password changes have their own dedicated flows in Django.
        fields = ['employee_id', 'department', 'position', 'is_supervisor', 'supervisor',
                  'remaining_leave_days_sick', 'remaining_leave_days_personal', 'remaining_leave_days_vacation']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'is_supervisor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'supervisor': forms.Select(attrs={'class': 'form-control'}),
            'remaining_leave_days_sick': forms.NumberInput(attrs={'class': 'form-control'}),
            'remaining_leave_days_personal': forms.NumberInput(attrs={'class': 'form-control'}),
            'remaining_leave_days_vacation': forms.NumberInput(attrs={'class': 'form-control'}),
        }

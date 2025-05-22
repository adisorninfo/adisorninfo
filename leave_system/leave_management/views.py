from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Import messages
from django.contrib.auth.models import User # Import User
# from django.contrib.auth.hashers import make_password # Not needed if using create_user
from .models import Employee
from .forms import EmployeeForm, EmployeeUpdateForm # Import EmployeeUpdateForm

@login_required
def home(request):
    return render(request, 'leave_management/index.html')

@login_required # Later, restrict to HR
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'leave_management/employee_list.html', {'employees': employees})

@login_required # Later, restrict to HR
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                # Create User
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                # Optionally, add user to a group here if needed

                # Create Employee instance
                employee = form.save(commit=False)
                employee.user = user  # Link the created User
                employee.save() # Save the employee object (which now includes the user link)
                # form.save_m2m() # If you had any m2m fields on the form being saved directly

                messages.success(request, f"Employee {employee.user.username} created successfully.")
                return redirect('leave_management:employee_list')
            except Exception as e: # Catch potential errors like username already exists
                messages.error(request, f"Error creating employee: {e}")
                # If user was created but employee saving failed, consider deleting the user:
                # if 'user' in locals() and user.pk:
                # user.delete()
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm()
    return render(request, 'leave_management/employee_form.html', {'form': form, 'action': 'Create'})

@login_required # Later, restrict to HR
def employee_update(request, pk): # pk is the primary key of the Employee
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=employee) # Use EmployeeUpdateForm
        if form.is_valid():
            form.save()
            messages.success(request, f"Employee {employee.user.username} updated successfully.")
            return redirect('leave_management:employee_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeUpdateForm(instance=employee) # Use EmployeeUpdateForm
            
    return render(request, 'leave_management/employee_form.html', {'form': form, 'action': 'Update', 'employee': employee})

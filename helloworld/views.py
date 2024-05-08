# In helloworld/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, EmployeeForm
from .models import CustomUser, Employee

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_employees')
    else:
        form = RegistrationForm()
    return render(request, 'helloworld/register.html', {'form': form})

# Views for CRUD operations
@login_required
def list_employees(request):
    employees = Employee.objects.all()
    return render(request, 'helloworld/list_employees.html', {'employees': employees})

@login_required
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_employees')
    else:
        form = EmployeeForm()
    return render(request, 'helloworld/create_employee.html', {'form': form})

@login_required
def update_employee(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('list_employees')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'helloworld/update_employee.html', {'form': form})

@login_required
def delete_employee(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    employee.delete()
    return redirect('list_employees')

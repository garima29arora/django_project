from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm
from django.shortcuts import redirect, get_object_or_404
from .models import User
def user_list(request):
    users = User.objects.all()
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    return render(request, 'enroll/user_list.html', {'form': form, 'users': users})

def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    return render(request, 'enroll/edit_user.html', {'form': form})

def delete_user(request, user_id):
    # Retrieve the user instance to be deleted
    user = get_object_or_404(User, pk=user_id)
    
    # Check if the request method is POST (i.e., user confirmed deletion)
    if request.method == 'POST':
        # Perform the deletion
        user.delete()
        
        # Redirect to the user list page after deletion
        return redirect('user_list')
    
    # If the request method is not POST, render a confirmation page (template)
    return render(request, 'enroll/confirm_delete.html', {'user': user})
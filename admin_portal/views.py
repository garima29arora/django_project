from django.shortcuts import render

def home(request):
    return render(request, 'admin_portal/home.html')

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str  # Use force_str instead of force_text
from django.urls import reverse
from django.contrib import messages
from admin_portal.forms import UserRegistrationForm
from django.contrib.auth import views as auth_views

CustomUser = get_user_model()

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until it is verified
            user.save()
            
            # Send email verification
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            verification_url = request.build_absolute_uri(reverse('verify_email', kwargs={'uidb64': uid, 'token': token}))
            
            subject = "Email Verification for Your Account"
            message = render_to_string('admin_portal/verify_email.html', {'user': user, 'verification_url': verification_url})
            
            send_mail(subject, message, 'garimaarora2923@gmail.com', [user.email])
            
            messages.success(request, "Account created successfully. Please check your email for verification.")
            
            return redirect('login')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'admin_portal/register.html', {'form': form})

# Email verification view
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        messages.success(request, "Email verified successfully! You can now log in.")
    else:
        messages.error(request, "Email verification failed. Please try again.")
    
    return redirect('login')

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'admin_portal/password_reset.html'
    email_template_name = 'admin_portal/password_reset_email.html'
    success_url = '/password_reset/done/'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'admin_portal/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'admin_portal/password_reset_confirm.html'
    success_url = '/password_reset/complete/'

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'admin_portal/password_reset_complete.html'

from django.contrib.auth import views as auth_views

# Password reset views
class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'admin_portal/password_reset.html'
    email_template_name = 'admin_portal/password_reset_email.html'
    success_url = '/password_reset/done/'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'admin_portal/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'admin_portal/password_reset_confirm.html'
    success_url = '/password_reset/complete/'

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'admin_portal/password_reset_complete.html'

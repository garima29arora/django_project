from django.urls import path
from admin_portal import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify_email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


 #Password reset URL patterns
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

from django.urls import path
from . import views
# Create your views here
urlpatterns = [
    path('register/', views.register, name='register'),
    
    # email verification urls
    
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),


    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # forger password urls
    
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('reset_password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    
]
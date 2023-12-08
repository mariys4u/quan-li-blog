from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from .models import Account
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import re

from django.contrib.sites.shortcuts import get_current_site
from . token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required



def register(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            # Email verification setup (template)
            current_site = get_current_site(request)

            subject = 'Account verification email'

            message = render_to_string('accounts/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': user_tokenizer_generate.make_token(user),
            })

            # Email verification setup (email)
            send_mail(subject, message, [settings.EMAIL_HOST_USER], [email])
                  
            return redirect('/accounts/login/?command=verification&email='+email)

        
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        captcha = request.POST.get('g-recaptcha-response')
        
        email_validation = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        if not re.match(email_validation, email):
            messages.error(request, 'Vui lòng nhập lại email hoặc mật khẩu')
            return redirect('login')

        
        
        if captcha and password and email:
            user = auth.authenticate(email=email, password=password, captcha=captcha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Bạn đã đăng xuất thành công')
                return redirect('home')
            else:
                messages.error(request, 'Vui lòng kiểm tra lại email hoặc mật khẩu hoặc captcha')
                return redirect('login')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại email hoặc mật khẩu hoặc captcha')
            return redirect('login')
    context = {'form': form}
    return render(request,'accounts/login.html', context)     

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('home')




def email_verification(request, uidb64, token):

    # uniqueid
    try:
        
        unique_id = urlsafe_base64_decode(uidb64).decode()

        user = Account.objects.get(pk=unique_id)
    
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            
        user = None
    
    # Success

    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True

        user.save()
        messages.success(request, 'Email của bạn đã được xác thực thành công')

        return redirect('login')


    # Failed 

    else:

        messages.error(request, 'Link đã hết hạn')
        


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # Reset password email setup (template)
            current_site = get_current_site(request)

            subject = 'Reset password email'

            message = render_to_string('accounts/reset-password-email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': user_tokenizer_generate.make_token(user),
            })

            # Reset password email setup (email)
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)    
            
            messages.success(request, 'Vui lòng kiểm tra email của bạn để lấy lại mật khẩu')
                  
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')




def reset_password(request, uidb64, token):
    try:
        unique_id = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=unique_id)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user and user_tokenizer_generate.check_token(user, token):
        request.session['uid'] = uidb64
        messages.success(request, 'Vui lòng nhập mật khẩu mới')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Link đã hết hạn')
        return redirect('login')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password and confirm_password:
            password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
            if not re.match(password_regex, password):
                messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự, ít nhất 1 chữ hoa, 1 chữ thường, 1 số và 1 ký tự đặc biệt')
                return redirect('resetPassword')
        
        
        if password == confirm_password:
            uidb64 = request.session['uid']
            user_id = force_str(urlsafe_base64_decode(uidb64).decode())
            user = Account.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Mât khẩu đã được thay đổi thành công')
            return redirect('login')
        else:
            messages.error(request, 'Mật khẩu không khớp')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
    
    

# if client wants to resend email verification link when he/she did not receive the email or the link has been expired when resgistred successfully

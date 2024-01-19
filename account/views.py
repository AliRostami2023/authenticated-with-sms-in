from django.contrib import messages
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from account.forms import RegisterForm, RegisterVerifyForm, LoginForm, LoginVerifyForm
import random
from account.models import Otp, User
from utils import send_otp_code


# Create your views here.


class Home(View):
    def get(self, request):
        return render(request, 'home.html')


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:home-page')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            Otp.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['register_otp_code'] = {
                'full_name': form.cleaned_data['full_name'],
                'phone_number': form.cleaned_data['phone'],
                'password': form.cleaned_data['password']
            }
            messages.success(request, 'we send you a code', 'success')
            return redirect('account:verify-page')
        return render(request, self.template_name, {'form': form})


class RegisterVerifyView(View):
    form_class = RegisterVerifyForm
    template_name = 'verify.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:home-page')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session['register_otp_code']
        code_instance = Otp.objects.get(phone_number=user_session['phone_number'])

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['verify_code'] == code_instance.code:
                User.objects.create_user(user_session['full_name'], user_session['phone_number'],
                                         user_session['password'])
                code_instance.delete()
                messages.success(request, 'you registered...', 'success')
                return redirect('account:home-page')
            else:
                messages.error(request, 'code is wrong', 'danger')
                return redirect('account:verify-page')

        return render(request, self.template_name, {'form': form})
    

class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:home-page')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone']
            user = User.objects.filter(phone_number__iexact=phone_number).exists()
            if user:
                random_code = random.randint(1000, 9999)
                send_otp_code(form.cleaned_data['phone'], random_code)
                Otp.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
                request.session['login_otp_code'] = {
                    'phone_number': form.cleaned_data['phone']
                }
                messages.success(request, 'we send code...', 'success')
                return redirect('account:verify-login-page')
            else:
                messages.error(request, 'this phone is not registered', 'danger')

        return render(request, self.template_name, {'form': form})


class VerifyLoginView(View):
    form_class = LoginVerifyForm
    template_name = 'verify-login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:home-page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        user_session = request.session['login_otp_code']
        code_instance = Otp.objects.get(phone_number=user_session['phone_number'])

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                user = User.objects.filter(id=request.user.id).first()
                login(request, user)
                code_instance.delete()
                messages.success(request, 'you logined', 'success')
                return redirect('account:home-page')
            else:
                messages.error(request, 'code is wrong', 'danger')
                return redirect('account:verify-login-page')
            
        return render(request, self.template_name, {'form': form})



class LogOut(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logout successfully')
        return redirect('account:home-page')

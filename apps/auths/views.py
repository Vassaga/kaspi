
from django.shortcuts import render, redirect
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages

# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView

from auths.forms.register_form import RegisterForm
from auths.models import MyUser

# Create your views here.



class RegisterView(View):
    """User Register"""

    template_name = 'register.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = RegisterForm()
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'form': form
            }
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form  = RegisterForm(request.POST)
        if form.is_valid():
            del form.cleaned_data['password2']
            MyUser.objects.create(**form.cleaned_data)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('success/')
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'form': form
            }
        )
        
class RegistrationSuccessView(View):
    template_name = 'register_done.html'

    def get(self, request):
        return render(request, self.template_name)


''' AUTHS VIEWS '''

from django.shortcuts import render, redirect
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib import messages

from auths.forms.register_form import RegisterForm
from auths.models import MyUser


class RegisterView(View):

    """ СТРАНИЦА РЕГИСТРАЦИИ ПОЛЬЗОВАТЕЛЯ. """

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
            try:
                del form.cleaned_data['password2']
                fio = form.cleaned_data['fio']
                number = form.cleaned_data['number']
                password = form.cleaned_data['password']
                MyUser.objects.create_user(number=number, fio=fio, password=password)
                messages.success(request, 'Регистрация прошла успешно!')
                return redirect('success/')
            except Exception as e:
                messages.error(request, f'Что то пошло не так. Ошибка: {e}')
                return redirect('/reg/success/')
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

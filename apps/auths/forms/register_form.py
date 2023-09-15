from django import forms 

from django.core.exceptions import ValidationError
from typing import Any

from auths.models import MyUser

def normalize_number(phone_number):
    normalized_number = '7'+''.join(filter(str.isdigit, phone_number))
    if len(normalized_number) != 11:
        raise ValidationError('неверный формат номера')
    else:
        return normalized_number

class RegisterForm(forms.Form):
    number = forms.CharField(label="введите номер", max_length=10)
    fio = forms.CharField(label="введите ФИО", max_length=120)
    password = forms.CharField(label="Пароль", min_length=6)
    password2 = forms.CharField(label="Повторите пароль", min_length=6)


    def clean(self) -> dict[str, Any]:
        return super().clean()
    
    def clean_number(self):
        data: str = self.cleaned_data['number']
        number = normalize_number(data)
        if MyUser.objects.filter(number=number).exists() == True:
            raise ValidationError('пользователь с таким номером уже зарегистрирован')
        return normalize_number(data)
    
    def clean_fio(self):
        data: str = self.cleaned_data['fio']
        if len(data) < 3:
            raise ValidationError('Введите корректное имя')
        return data
    
    def clean_password2(self) -> dict[str, Any]:
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise ValidationError('Пароли не совпадают')
        return self.cleaned_data
    
    
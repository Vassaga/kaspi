from django import forms 

class AuthorisationForm(forms.Form):
    number = forms.CharField(label="введите номер", max_length=10)
    fio = forms.CharField(label="введите ФИО", max_length=120)
    password = forms.CharField(label="Пароль", min_length=6)
    password2 = forms.CharField(label="Повторите пароль", min_length=6)
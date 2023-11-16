from django.shortcuts import render

# Create your views here.


def main_page(request): # главная страница приложения
    return render(
        template_name='main.html',
        request=request
    )
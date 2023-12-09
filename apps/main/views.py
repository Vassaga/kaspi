from django.shortcuts import render

# Create your views here.

from shop.product_generator import *


def main_page(request): # главная страница приложения

    if Category.objects.count() == 0:
        ProductGenerator()
    if request.user.is_authenticated:
        user = request.user
        return render(
            template_name='main.html',
            request=request,
            context = {
                        'user': user
                    }
        )
    else:
        return render(
            template_name='main.html',
            request=request
        )
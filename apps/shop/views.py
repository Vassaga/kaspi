from django.shortcuts import render

# Create your views here.


def shop_page(request): # главная страница приложения
    if request.user.is_authenticated:
        user = request.user  
        return render(
            template_name='shop.html',
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
    
def catalog_page(request): # главная страница приложения
    if request.user.is_authenticated:
        user = request.user  
        return render(
            template_name='catalog.html',
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
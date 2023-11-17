from django.shortcuts import render

# Create your views here.


def main_page(request): # главная страница приложения
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
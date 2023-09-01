from django.shortcuts import render

# Create your views here.


def bank_main_page(request):
    return render(
        template_name='bank.html',
        request=request
    )
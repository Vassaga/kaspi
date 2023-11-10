from django.shortcuts import render, redirect
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.

from auths.models import MyUser
from bank.models import BankAccount

# def bank_main_page(request):
#     user = request.user
#     bank_account = BankAccount.objects.get(owner=user)
#     return render(
#         template_name='bank.html',
#         request=request,
#         context = {
#             'user': user,
#             'balance': bank_account.balance
#         }
#     )

class BankMainPage(View):
    """Main page"""

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            user = request.user
            bank_account = BankAccount.objects.get(owner=user)
            return render(
                template_name='bank.html',
                request=request,
                context = {
                    'user': user,
                    'balance': bank_account.balance
                }
            )
        else:
            # user = request.user
            # bank_account = BankAccount.objects.get(owner=user)
            return redirect('login/')

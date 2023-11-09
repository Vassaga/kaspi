from django.shortcuts import render

# Create your views here.

from auths.models import MyUser
from bank.models import BankAccount

def bank_main_page(request):
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
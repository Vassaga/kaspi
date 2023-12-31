
''' BANK VIEWS '''

import json

from decimal import Decimal

from django.shortcuts import render, redirect
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from bank.models import BankAccount, Transfer
from bank.forms.create_bankaccount import BankAccountForm
from bank.forms.transfer_self_bank_acc_form import TransferSelfForm
from bank.forms.transfer_any_bank_acc_form import TransferAnyFormByIBAN, TransferAnyFormByNumber
from bank.currency_converter import currency_converter
from shop.models import Purchase


class BankMainPageView(View):

    """ ГЛАВНАЯ СТРАНИЦА ПОЛЬЗОВАТЕЛЯ БАНКА. """

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            if request.user.is_authenticated:
                user = request.user   # получаем авторизованного пользователя
                # вытаскиваем типы счетов:
                Gold_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.GOLD).order_by('owner', 'type')
                Dep_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.DEP).order_by('owner', 'type')
                Red_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.RED).order_by('owner', 'type')
                Inst = Purchase.objects.filter(user=user, remaining_amount__gt=0.01)
                BadInst = Purchase.objects.filter(
                    user=user,
                    next_pay_date__lte=timezone.now()
                )
                return render(
                    template_name='bank.html',
                    request=request,
                    context = {
                        'user': user,
                        'inst': Inst,
                        'badinst': BadInst,
                        'Gold_accounts': Gold_accounts,
                        'Dep_accounts' : Dep_accounts,
                        'Red_accounts' : Red_accounts
                    }
                )
            else:
                return redirect('login/')
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
        
class BankAccountDetailsView(View):

    """ СТРАНИЦА ИНФОРМАЦИИ О СЧЕТЕ. ДЕЙСТВИЯ. """

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            if request.user.is_authenticated:
                user = request.user   # получаем авторизованного пользователя
                # вытаскиваем типы счетов:
                Gold_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.GOLD).order_by('owner', 'type')
                Dep_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.DEP).order_by('owner', 'type')
                Red_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.RED).order_by('owner', 'type')
                return render(
                    template_name='account_details.html',
                    request=request,
                    context = {
                        'user': user,
                        'Gold_accounts': Gold_accounts,
                        'Dep_accounts' : Dep_accounts,
                        'Red_accounts' : Red_accounts
                    }
                )
            else:
                return redirect('/login/')
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
        
class BankAccountDetailsInfoView(View):

    """ СТРАНИЦА ИНФОРМАЦИИ О СЧЕТЕ. ИНФО О СЧЕТЕ. """

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            if request.user.is_authenticated:
                user = request.user   # получаем авторизованного пользователя
                # вытаскиваем типы счетов:
                Gold_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.GOLD).order_by('owner', 'type')
                Dep_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.DEP).order_by('owner', 'type')
                Red_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.RED).order_by('owner', 'type')
                return render(
                    template_name='account_details_info.html',
                    request=request,
                    context = {
                        'user': user,
                        'Gold_accounts': Gold_accounts,
                        'Dep_accounts' : Dep_accounts,
                        'Red_accounts' : Red_accounts
                    }
                )
            else:
                return redirect('/login/')
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
        
class BankAccountDetailsInfo2View(View):

    """ СТРАНИЦА ИНФОРМАЦИИ О СЧЕТЕ. ВЫПИСКА. """

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            if request.user.is_authenticated:
                user = request.user   # получаем авторизованного пользователя
                # вытаскиваем типы счетов:
                Gold_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.GOLD).order_by('owner', 'type')
                Transfers = Transfer.objects.filter(outaccount__owner=user).order_by('-datetime')
                Purchases = Purchase.objects.filter(user=user).order_by('-pk')
                return render(
                    template_name='account_details_vipiska.html',
                    request=request,
                    context = {
                        'user': user,
                        'Gold_accounts': Gold_accounts,
                        'Transfers': Transfers,
                        'Purchases': Purchases
                    }
                )
            else:
                return redirect('/login/')
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')


class CreateBankAccountView(View):

    """
    СТРАННИЦА СОЗДАНИЯ СЧЕТА.

        Параметры:
        - account_type 
        Извлекаем информацию о типе счета из параметров запроса
        (данные о типе создаваемого счета сидят в ссылках на странице выбора создаваемого счета)

        -  user = request.user:
        Получаем авторизованного пользователя, что бы отображать (обрабатывать) именно его счета

    """
    template_name = 'create_bankaccount.html'

    def get(self, request, *args, **kwargs):
        form = BankAccountForm()
        try:
            account_type = kwargs.get('account_type', None)
            return render(request, self.template_name, {'form': form, 'account_type': account_type})
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
    
    def post(self, request, *args, **kwargs):
        try:
            form = BankAccountForm(request.POST) 
            user = request.user
            account_type = kwargs.get('account_type', None)
            if form.is_valid():
                currency = form.cleaned_data['currency']
                if account_type == 'gold':
                    type = BankAccount.AccauntType.GOLD
                elif account_type == 'red':
                    type = BankAccount.AccauntType.RED
                elif account_type == 'dep':
                    type = BankAccount.AccauntType.DEP
                else:
                    type = BankAccount.AccauntType.GOLD  # Значение по умолчанию - нужно ли нам это?
                if account_type == 'gold' and currency == 'KZT':
                    balance = '1000000'
                else:
                    balance = '0'
                BankAccount.objects.create(owner=user, balance=balance, currency=currency, type=type)
                return redirect('/bank/')
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
    
    
class TransfersPageView(View):

    """ СТРАННИЦА ПЕРЕВОДОВ. """

    template_name = 'transfers_page.html'

    def get(self, request):
        return render(request, self.template_name)
    

class TransferSelfBankAccountsView(View):

    """ СТРАННИЦА ПЕРЕВОДОВ МЕЖДУ СВОИМИ СЧЕТАМИ. """

    template_name = 'transfer_self_bank_accounts.html'

    def get(self, request):
        try:
            form = TransferSelfForm(user=request.user)
            return render(request, self.template_name, {'form': form,})
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
    
    def post(self, request, *args, **kwargs):
        try:
            form = TransferSelfForm(request.POST)
            # user = request.user
            if form.is_valid():
                outamount = form.cleaned_data['outamount']
                outaccount = form.cleaned_data['outaccount']
                outaccount_object = form.fields['outaccount'].queryset.get(pk=outaccount.pk)
                inaccount = form.cleaned_data['inaccount']
                inaccount_object = form.fields['inaccount'].queryset.get(pk=inaccount.pk)
                inamount = currency_converter(float(outamount), str(outaccount_object.currency), str(inaccount_object.currency))
                if outaccount_object.balance < outamount:
                    messages.error(request, 'Недостаточно средств на счете списания.')
                    return redirect('success/')
                else:
                    inaccount_object.balance += inamount
                    outaccount_object.balance -= outamount
                    outaccount_object.save()
                    inaccount_object.save()
                    incurrency = inaccount_object.currency
                    outcurrency = outaccount_object.currency
                    Transfer.objects.create(
                        outaccount=outaccount_object, 
                        inaccount=inaccount_object,
                        outamount=outamount,
                        inamount=inamount,
                        outcurrency=outcurrency,
                        incurrency=incurrency,
                        outbalance=outaccount_object.balance,
                        inbalance=inaccount_object.balance)
                messages.success(request, 'Транзакция успешно выполнена.')        
                return redirect('success/')
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')

class TransferSuccessView(View):

    """ СТРАННИЦА О СТАТУСЕ ПЕРЕВОДОВ МЕЖДУ СВОИМИ СЧЕТАМИ. """

    template_name = 'transfer_done.html'

    def get(self, request):
        return render(request, self.template_name)
    
    
class TransfersHistoryView(View):

    """ СТРАННИЦА ИСТОРИИ ПЕРЕВОДОВ. """

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            if request.user.is_authenticated:
                user = request.user   
                Transfers = Transfer.objects.filter(Q(transaction_type='Transfer') & Q(outaccount__owner=user)).order_by('-datetime')
                return render(
                    template_name = 'transfer_history.html',
                    request=request,
                    context = {
                        'user': user,
                        'Transfers': Transfers,
                    }
                )
            else:
                return redirect('login/')
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
        

class TransferAnyChoicePageView(View):

    """ СТРАННИЦА ВЫБОРА ПЕРЕВОДА ДЛЯ КЛИЕНТА КАСПИ. """

    template_name = 'transfer_any_choice.html'

    def get(self, request):
        return render(request, self.template_name)

class TransferAnyBankAccountsViewByNumber(View):

    """ СТРАННИЦА ПЕРЕВОДОВ НА СЧЕТ ДРУГОГО КЛИЕНТА КАСПИ ПО НОМЕРУ ТЕЛЕФОНА. """

    template_name = 'transfer_any_bank_accounts_1.html'

    def get(self, request):
        try:
            form = TransferAnyFormByNumber(user=request.user)
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
    
    def post(self, request, *args, **kwargs):
        try:
            form = TransferAnyFormByNumber(request.POST)
            # user = request.user
            if form.is_valid():
                outamount = form.cleaned_data['outamount']
                outaccount = form.cleaned_data['outaccount']
                inaccount = form.cleaned_data['inaccount']
                inamount = currency_converter(float(outamount), str(outaccount.currency), str(inaccount.currency))
                if outaccount.balance < outamount:
                    messages.error(request, 'Недостаточно средств на счете списания.')
                    return redirect('/transfers/success/')
                else:
                    inaccount.balance += inamount
                    outaccount.balance -= outamount
                    outaccount.save()
                    inaccount.save()
                    incurrency = inaccount.currency
                    outcurrency = outaccount.currency
                    Transfer.objects.create(
                        outaccount=outaccount, 
                        inaccount=inaccount,
                        outamount=outamount, 
                        inamount=inamount,
                        outcurrency=outcurrency,
                        incurrency=incurrency,
                        outbalance=outaccount.balance,
                        inbalance=inaccount.balance)
                messages.success(request, 'Транзакция успешно выполнена.')        
                return redirect('/transfers/success/')
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
    
class TransferAnyBankAccountsViewByIBAN(View):

    """ СТРАННИЦА ПЕРЕВОДОВ НА СЧЕТ ДРУГОГО КЛИЕНТА КАСПИ ПО НОМЕРУ СЧЕТА. """

    template_name = 'transfer_any_bank_accounts.html'

    def get(self, request):
        try:
            form = TransferAnyFormByIBAN(user=request.user)
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
    
    def post(self, request, *args, **kwargs):
        try:
            form = TransferAnyFormByIBAN(request.POST)
            # user = request.user
            if form.is_valid():
                outamount = form.cleaned_data['outamount']
                outaccount = form.cleaned_data['outaccount']
                inaccount = form.cleaned_data['inaccount']
                inamount = currency_converter(float(outamount), str(outaccount.currency), str(inaccount.currency))
                if outaccount.balance < outamount:
                    messages.error(request, 'Недостаточно средств на счете списания.')
                    return redirect('/transfers/success/')
                else:
                    inaccount.balance += inamount
                    outaccount.balance -= outamount
                    outaccount.save()
                    inaccount.save()
                    incurrency = inaccount.currency
                    outcurrency = outaccount.currency
                    Transfer.objects.create(
                        outaccount=outaccount, 
                        inaccount=inaccount,
                        outamount=outamount, 
                        inamount=inamount,
                        outcurrency=outcurrency,
                        incurrency=incurrency,
                        outbalance=outaccount.balance,
                        inbalance=inaccount.balance)
                messages.success(request, 'Транзакция успешно выполнена.')        
                return redirect('/transfers/success/')
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')
    

class UserInstsView(View):

    """ СТРАННИЦА РАССРОЧЕК ПОЛЬЗОВАТЕЛЯ. """
    template_name = 'user_insts.html'

    def get(self, request):
        try:
            user = request.user
            Inst = Purchase.objects.filter(user=user, remaining_amount__gt=0.01)
            # BadInst = Purchase.objects.filter(user=user, remaining_amount__gt=0.01, next_pay_date__lte=timezone.now())
            return render(
                request, 
                self.template_name, 
                context = {
                    'user': user,
                    'inst': Inst,
                    # 'badinst': BadInst,
                })
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')

    def post(self, request, *args, **kwargs):
        try:
            # data = request.POST.get('monthly_payment')
            # user = request.user
            data = request.POST.get('data')
            data_dict = json.loads(data) if data else {}
            try:
                value1 = data_dict.get('key1')
                value2 = data_dict.get('key2')
                purchase=Purchase.objects.get(pk=value1)
                print(value1, value2, purchase)
                outaccount = BankAccount.objects.get(iban=purchase.iban)
                inaccount = BankAccount.objects.get(iban='7777777777777777') # МАГАЗИН продумай - ибан банка изменится в другой базе
                amount = Decimal(value2)
                converted_amount = currency_converter(amount, 'KZT', outaccount.currency)
                if outaccount.balance < converted_amount:
                    messages.error(request, 'Недостаточно средств на счету')
                    return redirect('/transfers/success/')
                else:
                    outaccount.balance -= converted_amount
                    outaccount.save()
                    inaccount.balance += amount
                    inaccount.save()
                    purchase.remaining_amount -= amount
                    purchase.next_pay_date += timezone.timedelta(minutes=5)
                    purchase.save()
                    Transfer.objects.create(
                            outaccount=outaccount, 
                            inaccount=inaccount,
                            outamount=purchase.monthly_payment,
                            inamount=purchase.monthly_payment,
                            outcurrency='KZT',
                            incurrency='KZT',
                            outbalance=outaccount.balance,
                            inbalance=inaccount.balance,
                            transaction_type='Inst')
                    messages.success(request, 'Платеж успешно проведен.')
                    return redirect('/transfers/success/')
            except Exception as e:
                messages.success(request, f'Транзакция не выполнена. Ошибка: {e}')
            return redirect('/transfers/success/')
        except Exception as e:
            messages.error(request, f'Что то пошло не так. Ошибка: {e}')
            return redirect('/transfers/success/')

""" SHOP VIEWS """


from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils import timezone

from shop.forms.purchase_create_form import PurchaseCreateForm
from bank.models import BankAccount

from bank.currency_converter import currency_converter

from shop.models import (
    Category,
    Product,
    Purchase
)
from shop.product_generator import *

def shop_page(request): # главная страница приложения МАГАЗИН
    if request.user.is_authenticated:
        user = request.user
        products = Product.objects.all().order_by('rating')
        return render(
            template_name='shop.html',
            request=request,
            context = {
                        'user': user,
                        'products': products
                    }
        )
    else:
        products = Product.objects.all().order_by('rating')
        return render(
            template_name='shop.html',
            request=request,
            context = {
                        'products': products
                    }
        )
    
def catalog_page(request): # каталог приложения МАГАЗИН
    if request.user.is_authenticated:
        user = request.user
        categories = Category.objects.all().order_by('name')
        return render(
            template_name='catalog.html',
            request=request,
            context = {
                        'user': user,
                        'categories': categories
                    }
        )
    else:
        categories = Category.objects.all().order_by('name')
        return render(
            template_name='catalog.html',
            request=request,
            context = {
                        'categories': categories
                    }
        )
    
class ProductsPageView(View):

    """ СТРАННИЦА ОБЗОРА ВСЕХ ТОВАРОВ ОДНОЙ КАТЕГОРИИ. """

    template_name = 'products.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        category = Category.objects.get(pk=pk)
        products = Product.objects.filter(category=category)
        return render(
            request, 
            self.template_name, 
            context = {'pk': pk, 'products': products, 'category': category})


class ProductPageView(View):

    """ СТРАННИЦА ОБЗОРА ОДНОГО ТОВАРА. """

    template_name = 'product.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            pk = kwargs.get('pk', None)
            product = Product.objects.get(pk=pk)
            # product = Product.objects.filter(category=category)
            return render(
                request, 
                self.template_name, 
                context = {'pk': pk, 'user': user, 'product': product}
            )
        else:
            return redirect('/bank/login/')
        
class PurchaseSuccessView(View):

    """ СТРАННИЦА О СТАТУСЕ ПОКУПКИ. """

    template_name = 'purchase_done.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PurchaseProductView(View):

    """ СТРАННИЦА СОВЕРШЕНИЯ ПОКУПКИ (тип. КОРЗИНА). """

    template_name = 'purchase.html'

    def get(self, request, *args, **kwargs):
        form = PurchaseCreateForm(user=request.user)
        if request.user.is_authenticated:
            user = request.user
            pk = kwargs.get('pk', None)
            product = Product.objects.get(pk=pk)
            return render(
                request, 
                self.template_name, 
                context = {'pk': pk, 'user': user, 'product': product, 'form': form}
            )
        else:
            return redirect('login/')
        
    def post(self, request, *args, **kwargs):
        form = PurchaseCreateForm(request.POST, user=request.user)
        print('покапка 01')   # удали
        if request.user.is_authenticated:
            if form.is_valid():
                print('покупка 02')   # удали
                user = request.user #?
                pk = kwargs.get('pk', None)
                product = Product.objects.get(pk=pk)
                quantity = form.cleaned_data['quantity']
                price = product.price*quantity
                bankaccount = form.cleaned_data['BankAccount']
                obj_BankAccount = BankAccount.objects.get(pk=bankaccount.pk)
                inst = int(form.cleaned_data['my_field'])
                converted_price = currency_converter(price, 'KZT', obj_BankAccount.currency)
                # converted_balance = currency_converter(bankaccount.balance, obj_BankAccount.currency, 'KZT')
                # if inst == 'option1' and obj_BankAccount.type == 'Gold':  # Логика покупки, если без рассрочки и каспи ГОЛД
                if inst == 0:     # Логика покупки, если без рассрочки
                    try:
                        if obj_BankAccount.balance < converted_price:
                            messages.error(request, 'Недостаточно средств на счете списания.')
                            return redirect('success/')
                        elif product.quantity < quantity:
                            messages.error(request, 'Количество товара в наличии не достаточно.')
                            return redirect('success/')
                        else:
                            obj_BankAccount.balance -= converted_price
                            product.quantity -= quantity
                            obj_BankAccount.save() # Сохраняем изменения баланса в базе данных
                            product.save() # Сохраняем изменения количества товара в базе данных
                            Purchase.objects.create(
                                user=user,
                                product=product,
                                quantity=quantity,
                                price=price,
                                iban=bankaccount.iban,
                                purchase_type='Cash',
                            )
                    except:
                        messages.error(request, 'Ошибка покупки.')
                        return redirect('success/') 
                elif inst != 0: # Логика покупки, c рассрочкой N месяц
                    try:
                        print('рассрочка 03')   # удали
                        product.quantity -= quantity
                        obj_BankAccount.save() # Сохраняем изменения баланса в базе данных
                        product.save() # Сохраняем изменения количества товара в базе данных
                        print('04')   # удали
                        Purchase.objects.create(
                            user=user,
                            product=product,
                            quantity=quantity,
                            price=price,
                            iban=bankaccount.iban,
                            purchase_type='Inst',
                            inst_duration=inst,
                            monthly_payment=(price/inst),
                            # next_pay_date=timezone.now() + timezone.timedelta(days=30),  # настрой единый период??
                            next_pay_date=timezone.now() + timezone.timedelta(minutes=5),  # настрой единый период??
                            remaining_amount=price
                        )
                        print('рассрочка ok')
                    except:
                        messages.error(request, 'Ошибка покупки.')
                        return redirect('success/')  
                messages.success(request, 'Покупка успешно выполнена.')        
                return redirect('success/')
        else:
            return redirect('login/')
        messages.error(request, 'Ошибка.')        
        return redirect('success/')
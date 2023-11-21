from django.shortcuts import render, redirect
from django.views import View

from shop.models import (
    Category,
    Product,
    Purchase
)


def shop_page(request): # главная страница приложения
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
    
def catalog_page(request): # главная страница приложения
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
            pk = kwargs.get('pk', None)
            product = Product.objects.get(pk=pk)
            # product = Product.objects.filter(category=category)
            return render(
                request, 
                self.template_name, 
                context = {'pk': pk, 'product': product}
            )
        

class PurchaseProductView(View):

    template_name = 'purchase.html'

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
    
    # def post(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         user = request.user
    #         pk = kwargs.get('pk', None)
    #         product = Product.objects.get(pk=pk)

        
        # Здесь можно добавить логику оформления покупки, например, создание заказа или изменение статуса товара
        
        # После завершения логики перенаправьте пользователя на другую страницу
        return redirect('success_purchase')  # Или перенаправление на страницу с сообщением об успешной покупке
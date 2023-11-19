''' SHOP URLS'''


from django.urls import path
from shop.views import shop_page, catalog_page

urlpatterns = [
    path('shop/catalog/', catalog_page),
    path('shop/', shop_page),
]
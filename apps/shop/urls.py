''' SHOP URLS'''


from django.urls import path
from shop.views import shop_page, catalog_page, ProductPageView

urlpatterns = [
    path('shop/catalog/<str:pk>/', ProductPageView.as_view(), name='view_product'),
    path('shop/catalog/', catalog_page),
    path('shop/', shop_page),
]
''' SHOP URLS'''


from django.urls import path
from shop.views import shop_page, catalog_page, ProductsPageView, ProductPageView

urlpatterns = [
    path('shop/catalog/<str:pk>/', ProductsPageView.as_view(), name='view_products'),
    path('shop/catalog/', catalog_page),
    path('shop/<str:pk>/', ProductPageView.as_view(), name='view_product'),
    path('shop/', shop_page),
]
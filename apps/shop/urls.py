
""" SHOP URLS """

from django.urls import path
from shop.views import (
        shop_page, 
        catalog_page,
        DoneView, 
        ProductsPageView, 
        ProductPageView, 
        PurchaseProductView, 
        PurchaseSuccessView
    )

urlpatterns = [
    path('shop/done/', DoneView.as_view()),
    path('shop/catalog/<str:pk>/', ProductsPageView.as_view(), name='view_products'),
    path('shop/catalog/', catalog_page),
    path("shop/purchase/<str:pk>/success/", PurchaseSuccessView.as_view(), name='purchase_success'),
    path("shop/purchase/<str:pk>/", PurchaseProductView.as_view(), name='purchase_product'),
    path('shop/<str:pk>/', ProductPageView.as_view(), name='view_product'),
    path('shop/', shop_page),
]
''' BANK URLS'''



from django.urls import path

from bank.views import bank_main_page

urlpatterns = [
    path('bank/', bank_main_page),
]
''' BANK URLS'''



from django.urls import path

from bank.views import BankMainPage

urlpatterns = [
    path('bank/', BankMainPage.as_view()),
]
''' BANK URLS'''

from django.urls import path

from bank.views import (
    BankMainPageView, 
    CreateBankAccountView, 
    TransfersPageView, 
    TransferSelfBankAccountsView,
    TransferSuccessView
    )

urlpatterns = [
    path('transfers/self/success/', TransferSuccessView.as_view()),
    path('transfers/self/', TransferSelfBankAccountsView.as_view()),
    path('transfers/', TransfersPageView.as_view()),
    path('bank/create_account/<str:account_type>/', CreateBankAccountView.as_view(), name='create_account'),
    path('bank/', BankMainPageView.as_view()),
]
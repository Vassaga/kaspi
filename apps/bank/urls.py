''' BANK URLS'''

from django.urls import path

from bank.views import (
    BankMainPageView, 
    CreateBankAccountView, 
    TransfersPageView, 
    TransferSelfBankAccountsView,
    TransferSuccessView,
    TransferAnyBankAccountsViewByNumber,
    TransferAnyBankAccountsViewByIBAN,
    TransfersHistoryView,
    TransferAnyChoicePageView,
    UserInstsView
     )

urlpatterns = [
    path('transfers/self/success/', TransferSuccessView.as_view()),
    path('transfers/any/success/', TransferSuccessView.as_view()),
    path('transfers/self/', TransferSelfBankAccountsView.as_view()),
    path('transfers/any/choice/1/', TransferAnyBankAccountsViewByNumber.as_view()),
    path('transfers/any/choice/2/', TransferAnyBankAccountsViewByIBAN.as_view()),
    path('transfers/any/choice/', TransferAnyChoicePageView.as_view()),
    path('transfers/history/', TransfersHistoryView.as_view()),
    path('transfers/', TransfersPageView.as_view()),
    path('bank/user_insts/', UserInstsView.as_view()),
    path('bank/create_account/<str:account_type>/', CreateBankAccountView.as_view(), name='create_account'),
    path('bank/', BankMainPageView.as_view()),
]
''' BANK URLS'''

from django.urls import path

from bank.views import (
    BankMainPageView,
    BankAccountDetailsView,
    BankAccountDetailsInfoView,
    BankAccountDetailsInfo2View,
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
    path('transfers/success/', TransferSuccessView.as_view()),
    path('transfers/self/', TransferSelfBankAccountsView.as_view()),
    path('transfers/any/choice/1/', TransferAnyBankAccountsViewByNumber.as_view()),
    path('transfers/any/choice/2/', TransferAnyBankAccountsViewByIBAN.as_view()),
    path('transfers/any/choice/', TransferAnyChoicePageView.as_view()),
    path('transfers/history/', TransfersHistoryView.as_view()),
    path('transfers/', TransfersPageView.as_view()),
    path('bank/user_insts/', UserInstsView.as_view()),
    path('bank/create_account/<str:account_type>/', CreateBankAccountView.as_view(), name='create_account'),
    path('bank/details/info2/', BankAccountDetailsInfo2View.as_view(), name='account_details_info2'),
    path('bank/details/info/', BankAccountDetailsInfoView.as_view(), name='account_details_info'),
    path('bank/details/', BankAccountDetailsView.as_view(), name='account_details'),
    path('bank/', BankMainPageView.as_view()),
]
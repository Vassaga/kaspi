''' BANK URLS'''



from django.urls import path

from bank.views import BankMainPage, CreateBankAccountView

urlpatterns = [
    path('bank/', BankMainPage.as_view()),
    # path('bank/create_account/', CreateBankAccountView.as_view(), name='create_account'),
    path('bank/create_account/<str:account_type>/', CreateBankAccountView.as_view(), name='create_account'),
]
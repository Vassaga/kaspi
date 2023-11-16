
''' AUTHS URLS'''

from django.contrib import admin
from django.urls import path, include

from auths.views import RegisterView, RegistrationSuccessView


urlpatterns = [
    path('reg/success/', RegistrationSuccessView.as_view()),
    path('reg/', RegisterView.as_view()),
    path("bank/", include("django.contrib.auth.urls")),
    
]
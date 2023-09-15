''' AUTHS URLS'''

from django.contrib import admin
from django.urls import path


from auths.views import RegisterView, RegistrationSuccessView


urlpatterns = [
    path('reg/success/', RegistrationSuccessView.as_view()),
    path('reg/', RegisterView.as_view()),
    
]
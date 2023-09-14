# """MODELS BANK"""

# from django.core.exceptions import ValidationError
# from django.db import models
# from django.db.models.query import QuerySet
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from django.core.validators import RegexValidator

# from auths.models import MyUser


# class BankAccount(models.Model):
#     # доработать

#     class Currencies(models.TextChoices):
#         TENGE = 'KZT', 'Tenge'
#         RUBLI = 'RUB', 'Rubli'
#         EURO = 'EUR', 'Euro'
#         DOLLAR = 'USD', 'Dollar'

#     class AccountType(models.TextChoices): # доработать
#         ...


#     iban = models.CharField(
#         verbose_name='номер счета',
#         max_length=20,
#         validators=[
#             RegexValidator(regex=r'^\d{16}$', message='Number не верный формат')
#         ]
#     )

#     owner = models.OneToOneField(
#         verbose_name='пользователь',
#         related_name='счет',
#         to=MyUser,
#         on_delete=models.CASCADE
#     )

#     balance = models.DecimalField(
#         verbose_name='баланс счета',
#         max_digits=10,  # Максимальное количество цифр
#         decimal_places=2,  # Количество знаков после десятичной точки
#     )

#     currency = models.CharField(
#         verbose_name='валюта',
#         max_length=4,
#         choices=Currencies.choices,
#         default=Currencies.TENGE
#     )

#     type = models.CharField(         # доработать
#         ...
#     )

#     is_activ = models.BooleanField(
#         default=False
#     )




# class BankCard(models.Model):
#     number = models.CharField(
#         verbose_name='номер',
#         max_length=16,
#         validators=[
#             RegexValidator(regex=r'^\d{16}$', message='Number не верный формат')
#         ]
#     )
#     owner = models.OneToOneField(
#         verbose_name='пользователь',
#         related_name='card',
#         to=MyUser,
#         on_delete=models.CASCADE
#     )
#     cvv = models.CharField(
#         verbose_name='номер',
#         max_length=3,
#         validators=[
#             RegexValidator(regex=r'^\d{3}$', message='CVV не верный формат')
#         ]
#     )
#     experation_time = models.DateField(
#         verbose_name='срок действия'
#     )

#     class Meta:
#         ordering = ('-id',)
#         verbose_name = 'Банковская карта'
#         verbose_name_plural = 'Банковская карты'
"""MODELS BANK"""
import random
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from auths.models import MyUser


class BankAccount(models.Model):

    """Bank Account"""

    class Currencies(models.TextChoices):
        TENGE = 'KZT', 'Tenge'
        RUBLI = 'RUB', 'Rubli'
        EURO = 'EUR', 'Euro'
        DOLLAR = 'USD', 'Dollar'

    class AccauntType(models.TextChoices):
        GOLD = 'Gold', 'Kaspi Gold'
        RED = 'Red', 'Kaspi Red'
        DEP = 'Dep', 'Kaspi Deposit'

    iban = models.CharField(
        verbose_name='номер счета',
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(regex=r'^\d{16}$', message='Number не верный формат')
        ]
    )

    owner = models.ForeignKey(
        verbose_name='пользователь',
        related_name='счет',
        to=MyUser,
        on_delete=models.CASCADE
    )

    balance = models.DecimalField(
        verbose_name='баланс счета',
        max_digits=10,  
        decimal_places=2,  
    )

    currency = models.CharField(
        verbose_name='валюта',
        max_length=4,
        choices=Currencies.choices,
        default=Currencies.TENGE
    )

    type = models.CharField(
        verbose_name='тип счета',
        max_length=4,
        choices=AccauntType.choices,
        default=AccauntType.GOLD
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.get_type_display()} - {self.balance} {self.currency}"


@receiver(pre_save, sender=BankAccount)
def generate_iban(sender, instance, **kwargs):
    if not instance.iban:
        # Генерация уникального 16-значного числа
        generated_iban = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        # Проверка на уникальность в базе данных
        while BankAccount.objects.filter(iban=generated_iban).exists():
            generated_iban = ''.join([str(random.randint(0, 9)) for _ in range(16)])

        instance.iban = generated_iban

class Transfer(models.Model):
    """Transfer Account"""
    class TransactionTypes(models.TextChoices):
        DEPOSIT = 'Deposit', 'Deposit'
        WITHDRAWAL = 'Withdrawal', 'Withdrawal'
        TRANSFER = 'Transfer', 'Transfer'

    # user = models.ForeignKey(
    #     MyUser,
    #     verbose_name='отправитель',
    #     on_delete=models.CASCADE
    #     )
    outaccount = models.ForeignKey(
        BankAccount,
        verbose_name='счет-получатель',
        on_delete=models.CASCADE,
        related_name='sent_transfers'
    )
    inaccount = models.ForeignKey(
        BankAccount,
        verbose_name='счет-отправитель',
        on_delete=models.CASCADE,
        related_name='received_transfers'
    )

    amount = models.DecimalField(
        verbose_name='сумма',
        max_digits=10,  
        decimal_places=2,
        validators=[MinValueValidator(0)],  
    )

    balance = models.DecimalField(
        verbose_name='остаток на счете',
        max_digits=10,  
        decimal_places=2,
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionTypes.choices,
        default=TransactionTypes.TRANSFER,
        verbose_name='Тип транзакции',
    )

    datetime = models.DateTimeField(
        verbose_name='дата перевода',
        auto_now_add=True
        )
    
    class Meta:
        ordering = ('-pk',)
        verbose_name = 'перевод'
        verbose_name_plural = 'переводы'

    def __str__(self):
        return f"{self.datetime} со счета {self.outaccount.type} {self.outaccount.iban} пользователя {self.outaccount.owner.fio}  на счет пользователя {self.inaccount.owner.fio} {self.inaccount.iban} сумму ({self.amount})"

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
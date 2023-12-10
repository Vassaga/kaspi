

# ---------------------------------------------------------------------------------------------------------
# Сам себе придумал геморрой, но он работает. Функцию оставляем тут, но использовать, наверное не будем :)
# ---------------------------------------------------------------------------------------------------------

""" ФУНКЦИЯ ДЛЯ ИЗВЛЕЧЕНИЯ НЕЗАКРЫТЫХ РАССРОЧЕК И АВТОСПИСАНИЯ СРЕДСТВ """

import os
from django.db import connection
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base") 
django.setup()

from dramatiq import actor
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from bank.models import BankAccount, Transfer
from shop.models import Purchase

scheduler = BackgroundScheduler()
scheduler.start()


@actor
def instcontrol():
    with connection.cursor() as cursor:
        cursor.execute("BEGIN")
        try:
            purchases = Purchase.objects.filter(remaining_amount__gt=0)
            for purchase in purchases:
                if purchase.next_pay_date <= timezone.now():
                    try:
                        outaccount = BankAccount.objects.get(iban=purchase.iban)
                        inaccount = BankAccount.objects.get(iban='7777777777777777')
                        outaccount.balance -= purchase.monthly_payment
                        outaccount.save()
                        print('001')
                        purchase.remaining_amount -= purchase.monthly_payment
                        purchase.next_pay_date += timezone.timedelta(minutes=1)  # настрой единый период??
                        purchase.save()
                        print('002')
                        
                        inaccount.balance += purchase.monthly_payment
                        inaccount.save()
                        Transfer.objects.create(
                                outaccount=outaccount, 
                                inaccount=inaccount,
                                outamount=purchase.monthly_payment,
                                inamount=purchase.monthly_payment,
                                outcurrency=outaccount.currency,
                                incurrency=outaccount.currency,
                                outbalance=outaccount.balance,
                                inbalance=inaccount.balance,
                                transaction_type='Inst')
                        print('003')
                        print('ok')
                    except:
                        print('not ok')
            cursor.execute("COMMIT")
        except:
            cursor.execute("ROLLBACK")
        

scheduler.add_job(instcontrol, 'interval', seconds=60)


""" ФУНКЦИЯ ДЛЯ НАЧИСЛЕНИЯ ПРОЦЕНТОВ НА ДЕПОЗИТ. """

import os
from django.db import connection
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base") 
django.setup()

from dramatiq import actor
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from bank.models import BankAccount

scheduler = BackgroundScheduler()

scheduler.start()


@actor
def DepPercents():
    with connection.cursor() as cursor:
        cursor.execute("BEGIN")
        try:
            depaccounts = BankAccount.objects.filter(type='Dep')
            print(depaccounts)
            for depaccount in depaccounts:

                print(depaccount.balance)
                depaccount.balance = depaccount.balance + (depaccount.balance/100)*10
                depaccount.save()
                print(depaccount.balance)

            cursor.execute("COMMIT")
        except:
            cursor.execute("ROLLBACK")
        

scheduler.add_job(DepPercents, 'interval', seconds=20)

# запуск функции в 00,00 часов каждое первое число месяца:
# scheduler.add_job(DepPercents, trigger='cron', day='1', hour='0', minute='0')  
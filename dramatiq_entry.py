# dramatiq_entry.py

import os

from dramatiq import Worker
from apps.shop.tasks import instcontrol  # импортируем задачу по списанию рассрочек
from apps.bank.tasks import DepPercents # импортируем задачу по процентам на дипозите

# Загрузка настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")  # Замените на свои настройки Django

# Создание и запуск Worker для dramatiq
# worker = Worker([instcontrol])
worker = Worker([DepPercents])
worker.run()
# dramatiq_entry.py

import os
from django.conf import settings
from django.core.management import call_command
from dramatiq import Worker
from apps.shop.tasks import instcontrol  # Импортируйте вашу задачу

# Загрузка настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")  # Замените на свои настройки Django

# Инициализация настроек Django
settings.configure()
call_command('migrate')  # Применение миграций (если это необходимо)
call_command('runserver', '--noreload', '--nothreading')  # Запуск Django сервера (если нужно)

# Создание и запуск Worker для dramatiq
worker = Worker([instcontrol])
worker.run()
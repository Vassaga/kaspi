"""MODELS AUTHS"""

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



class MyUserManager(BaseUserManager):
    """ClientManager."""

    @classmethod
    def normalize_number(self, phone_number):
        normalized_number = '7'+''.join(filter(str.isdigit, phone_number))
        if len(normalized_number) != 11:
            raise ValidationError('неверный формат номера')
        else:
            return normalized_number

    def create_user(self, number: str, password: str) -> 'MyUser':

        if not number:
            raise ValidationError('Number required')

        custom_user: 'MyUser' = self.model(
            number=self.normalize_number(number),
            password=password
        )
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return custom_user

    def create_superuser(self, number: str, password: str) -> 'MyUser':

        custom_user: 'MyUser' = self.model(
            number=self.normalize_number(number),
            password=password
        )
        custom_user.is_superuser = True
        custom_user.is_active = True
        custom_user.is_staff = True
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return


class MyUser(AbstractBaseUser, PermissionsMixin):

    number = models.CharField(
        verbose_name='номер телефона',
        unique=True,
        max_length=11
    )
    fio = models.CharField(
        verbose_name='ФИО',
        max_length=120
    )
    
    is_staff = models.BooleanField(
        default=False
    )
    objects = MyUserManager()


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'number'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='Groups',
        blank=True,
        related_name='customuser_set',  # Установите уникальное имя обратной связи для связи с группами
        related_query_name='customuser'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='User permissions',
        blank=True,
        related_name='customuser_set',  # Установите уникальное имя обратной связи для связи с разрешениями пользователя
        related_query_name='customuser'
    )
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

from auths.models import MyUser


class Category(models.Model):
    """ МОДЕЛЬ КАТЕГОРИИ ТОВАРА. """
    name = models.CharField(
        verbose_name= 'Категория',
        max_length=100
    )

    # class Meta:
    #     app_label = 'shop'

    def __str__(self):
        return self.name

class Product(models.Model):

    """ МОДЕЛЬ ТОВАРА. """

    name = models.CharField(
        verbose_name= 'Наименование',
        max_length=100
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        decimal_places=2,
        max_digits=12
    )

    quantity = models.IntegerField(
        verbose_name='количество',
        default=0,
        blank=False,
    )

    rating = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def __str__(self):
        return self.name



class Purchase(models.Model):
    
    """ МОДЕЛЬ ПОКУПКИ. """

    class PurchaseTypes(models.TextChoices):
        CASH = 'Cash', 'Наличные'
        INST = 'Inst', 'Рассрочка'

    user = models.ForeignKey(
        MyUser,
        verbose_name='Покупатель',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=12, 
        decimal_places=2, 
        default='0'
    )

    purchase_date = models.DateTimeField(
        verbose_name='Дата покупки',
        auto_now_add=True
    )

    purchase_type = models.CharField(
        verbose_name='Способ оплаты',
        max_length=4,
        choices=PurchaseTypes.choices,
        default=PurchaseTypes.CASH
    )

    inst_duration = models.IntegerField(
        verbose_name='Срок рассрочки (месяцы)',
        blank=True,
        null=True
    )

    monthly_payment = models.DecimalField(
        verbose_name='Ежемесячный платеж',
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    remaining_amount = models.DecimalField(
        verbose_name='Оставшаяся сумма к оплате',
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.fio} купил {self.product.name} ({self.purchase_date})"



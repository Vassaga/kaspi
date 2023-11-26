# Generated by Django 4.2.7 on 2023-11-26 09:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Стоимость')),
                ('quantity', models.IntegerField(default=0, verbose_name='количество')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Рейтинг')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='количество')),
                ('price', models.DecimalField(decimal_places=2, default='0', max_digits=12, verbose_name='Стоимость')),
                ('iban', models.CharField(max_length=100, verbose_name='номер счета')),
                ('purchase_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')),
                ('purchase_type', models.CharField(choices=[('Cash', 'Полная оплата'), ('Inst', 'Рассрочка')], default='Cash', max_length=4, verbose_name='Способ оплаты')),
                ('inst_duration', models.IntegerField(blank=True, null=True, verbose_name='Срок рассрочки (месяцы)')),
                ('monthly_payment', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Ежемесячный платеж')),
                ('remaining_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Оставшаяся сумма к оплате')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
        ),
    ]

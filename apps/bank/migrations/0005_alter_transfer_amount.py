# Generated by Django 4.2.7 on 2023-11-12 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_transfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='сумму'),
        ),
    ]

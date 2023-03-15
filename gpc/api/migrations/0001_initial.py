# Generated by Django 4.1.7 on 2023-03-15 13:30

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(db_index=True, unique=True, validators=[django.core.validators.MinValueValidator(1, 'Должно быть целое число, большее 0')], verbose_name='Номер заказа')),
                ('price_usd', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Должно быть целое число, большее 0')], verbose_name='Стоимость (USD)')),
                ('price_rub', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Должно быть целое число, большее 0')], verbose_name='Стоимость (RUB)')),
                ('delivery_day', models.DateField(db_index=True, default=datetime.date.today, verbose_name='Срок поставки')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('delivery_day',),
            },
        ),
    ]

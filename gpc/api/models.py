from datetime import date
from django.core.validators import MinValueValidator
from django.db import models


class Order(models.Model):
    """Модель заказов."""

    number = models.PositiveIntegerField(
        verbose_name='Номер заказа',
        db_index=True,
        unique=True,
        validators=(
            MinValueValidator(1, 'Должно быть целое число, большее 0'),
        )
    )
    price_usd = models.PositiveSmallIntegerField(
        verbose_name='Стоимость (USD)',
        validators=(
            MinValueValidator(1, 'Должно быть целое число, большее 0'),
        )
    )
    price_rub = models.FloatField(
        verbose_name='Стоимость (RUB)',
    )
    delivery_day = models.DateField(
        verbose_name='Срок поставки',
        db_index=True,
        default=date.today
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('delivery_day',)

    def __str__(self):
        return self.number

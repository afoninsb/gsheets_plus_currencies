from rest_framework import serializers

from api.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор модели Order."""

    class Meta:
        model = Order
        fields = ('number', 'price_usd', 'price_rub', 'delivery_day')

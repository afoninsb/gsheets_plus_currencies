from rest_framework import serializers
from django.db.models import Sum

from api.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор модели Order."""

    class Meta:
        model = Order
        exclude = ('id',)


class OrdersSerializer(serializers.Serializer):
    total = serializers.SerializerMethodField()
    orders = OrderSerializer(many=True, read_only=True)

    def get_total(self, obj) -> float:
        return Order.objects.aggregate(Sum('price_rub'))['price_rub__sum']

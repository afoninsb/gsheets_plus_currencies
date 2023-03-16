from rest_framework import status
from api.serializers import OrderSerializer
from api.models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.shortcuts import get_object_or_404


@api_view(('GET',))
def orders(request):
    """Выдача суммы заказов в рублях и списка заказов."""

    queryset = Order.objects.all()
    serializer = OrderSerializer(queryset, many=True)
    total = Order.objects.aggregate(Sum('price_rub'))['price_rub__sum']
    return Response(
        {
            'tottal': total,
            'orders': serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(('GET',))
def order(request, number):
    """Выдача информации о заказе."""

    cur_order = get_object_or_404(Order, number=number)
    serializer = OrderSerializer(cur_order)
    return Response(serializer.data, status=status.HTTP_200_OK)

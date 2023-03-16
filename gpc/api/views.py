from rest_framework import status
from api.serializers import OrderSerializer, OrdersSerializer
from api.models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='get', responses={200: OrdersSerializer()})
@api_view(('GET',))
def orders(request):
    """Выдача суммы заказов в рублях и списка заказов."""

    queryset = Order.objects.all()
    return Response(
        OrdersSerializer({'orders': queryset}).data,
        status=status.HTTP_200_OK
    )


@swagger_auto_schema(method='get', responses={200: OrderSerializer})
@api_view(('GET',))
def order(request, number):
    """Выдача информации о заказе."""

    cur_order = get_object_or_404(Order, number=number)
    return Response(OrderSerializer(cur_order).data, status=status.HTTP_200_OK)

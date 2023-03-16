from django.contrib import admin

from api.models import Order


@admin.register(Order)
class RecipeAdmin(admin.ModelAdmin):
    """Представление заказов в админ-панели."""

    list_display = (
        'number',
        'price_usd',
        'price_rub',
        'delivery_day',
    )
    list_filter = ('delivery_day',)
    search_fields = ('number',)
    readonly_fields = ('number', 'price_usd', 'price_rub')

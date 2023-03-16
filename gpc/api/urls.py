from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from api.views import order, orders
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="gsheets_plus_currencies",
      default_version='v1',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@dummy.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

app_name = 'api'

router = SimpleRouter()

# router.register('order', OrdersViewSet, basename='orders')

urlpatterns = [
    path('order/<int:number>/', order, name='one_order'),
    path('order/', orders, name='orders'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

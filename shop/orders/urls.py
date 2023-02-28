from django.urls import path

from orders.views import index

app_name = "orders"

urlpatterns = [
    path('', index, name='render'),
]


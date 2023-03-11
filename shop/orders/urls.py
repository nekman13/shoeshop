from django.urls import path

import orders
from orders.views import (
    OrderCancelView,
    OrderCreateView,
    OrderDetailView,
    OrderListView,
    OrderSuccessView,
)

app_name = "orders"

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="create_order"),
    path("order-success/", OrderSuccessView.as_view(), name="order_success"),
    path("order-canceled/", OrderCancelView.as_view(), name="order_canceled"),
    path("", OrderListView.as_view(), name="orders"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
]

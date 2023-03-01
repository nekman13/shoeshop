from django.urls import reverse_lazy
from django.views.generic import CreateView

from common.views import CommonMixin
from orders.forms import OrderForm
from shoes.models import Basket


class OrderCreateView(CommonMixin, CreateView):
    """Класс для создания заказа"""

    template_name = "orders/order-create.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:create_order")
    title = "Оформление заказа"
    flag = "orders"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context["baskets"] = Basket.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

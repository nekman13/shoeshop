from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, ListView

from common.views import CommonMixin
from orders.forms import OrderForm
from orders.models import Order
from shoes.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderSuccessView(CommonMixin, TemplateView):
    """Класс для отображения страницы успешной оплаты"""

    template_name = "orders/success.html"
    title = "SHOESHOP - Спасибо за заказ!"


class OrderCancelView(CommonMixin, TemplateView):
    """Класс для отображения страницы не успешной оплаты"""

    template_name = "orders/cancel.html"


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

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.get_stripe_shoes(),
            metadata={"order_id": self.object.id},
            mode="payment",
            success_url=f'{settings.DOMAIN_NAME}{reverse_lazy("orders:order_success")}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse_lazy("orders:order_canceled")}',
        )
        return redirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Fulfill the purchase...
        fulfill_order(session)
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()


class OrderListView(CommonMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Заказы'
    model = Order
    context_object_name = 'orders'
    ordering = ("-created_at",)

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)

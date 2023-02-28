from django.shortcuts import render

from shoes.models import Basket
from users.models import User


def index(request):
    context = {
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'orders/order-create.html', context=context)



# Django
from django.db.models import Sum

# local Django
from .models import CartItem
from .utils import get_cart_id


def cart_items_count(request):
    count = CartItem.objects.filter(cart__cart_id=get_cart_id(request)).aggregate(Sum('quantity'))
    return {'count': count['quantity__sum']}

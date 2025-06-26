from .models import CartItem
from django.db.models import Sum

def cart_item_count(request):
    if request.user.is_authenticated:
        total = CartItem.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum'] or 0
    else:
        total = 0
    return {'cart_item_count': total}

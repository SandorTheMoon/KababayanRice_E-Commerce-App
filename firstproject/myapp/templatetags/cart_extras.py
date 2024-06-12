# myapp/templatetags/cart_extras.py
from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def subtotal(item):
    subtotal_amnt = item.product.product_price * item.quantity
    return subtotal_amnt


@register.filter
def convenience_fee(total_price):
    fee = total_price * 0.10
    return '{:.2f}'.format(fee)

@register.filter
def total_convenience_fee(total_price):
    convenience_fee_rate = Decimal('0.10')
    total = total_price + (total_price * convenience_fee_rate)
    return '{:.2f}'.format(total)
from django.contrib import admin
from .models import Account, ShippingAddress, Product, CartItem, Order

# Register your models here.
admin.site.register(Account)
admin.site.register(ShippingAddress)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)

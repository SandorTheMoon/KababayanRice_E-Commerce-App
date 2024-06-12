from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class ShippingAddress(models.Model):
    account = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.CharField(max_length=255, default='', blank=False)
    province = models.CharField(max_length=255, default='', blank=False)
    city = models.CharField(max_length=255, default='', blank=False)
    barangay = models.CharField(max_length=255, default='', blank=False)
    postal_code = models.CharField(max_length=255, default='', blank=False)
    home_address = models.CharField(max_length=255, default='', blank=False)

    def __str__(self):
        return self.home_address
    
class Product(models.Model):
    account = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    product_picture = models.ImageField(upload_to="product_pictures/", null=True, blank=True)
    product_name = models.CharField(max_length=255, default='', blank=False)
    product_price = models.IntegerField(blank=False)
    product_origin = models.CharField(max_length=255, default='', blank=False)
    product_description = models.CharField(max_length=510, default='', blank=False)
    

    def __str__(self):
        return self.product_name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity} - {self.user.username}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    seller = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=[(1, 'To pack'), (2, 'To ship'), (3, 'To deliver'), (4, 'Canceled')], default=1, null=True, blank=True)

    def __str__(self):
        return f"Order for {self.product.product_name} by {self.user.username}"
    
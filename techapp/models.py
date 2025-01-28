from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class Gadget(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     features = models.JSONField(default=list)
#     image= models.ImageField(upload_to='gadgets/')

#     def __str__(self):
#         return self.name

class ContactDetail(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()    
    
    def __str__(self):
        return self.name
    
# upadate profile
    
# models.py
# from django.contrib.auth.models import User
# from django.db import models

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     address = models.TextField(max_length=255, blank=True, null=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
    
#     def __str__(self):
#         return self.user.username
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)  # JSON field to store list
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        # Assuming 'features' is a list
        feature_list = "\n".join([f"• {feature}" for feature in self.features])
        return f"{self.name}\nFeatures:\n{feature_list}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def total(self):
        return self.product.price * self.quantity
    
from django.contrib.auth.models import User

class BillingDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.PositiveIntegerField()
    shipping_address = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Delivered')
    
    def __str__(self):
        return f"Order #{self.id} - ({self.status})"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def total(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
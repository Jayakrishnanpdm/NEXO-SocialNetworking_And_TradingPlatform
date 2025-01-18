from django.db import models
from Customer.models import Customer
from Products.models import Product
# Create your models here.

class Order(models.Model):
    CART_STAGE = 0
    ORDER_CONFIRMED = 1
    ORDER_DISPATCHED = 2
    ORDER_DELIVERED = 3
    ORDER_CANCELLED = 4
    status_choices = ((CART_STAGE,'Cart Stage'),(ORDER_CONFIRMED,'Order Confirmed'),(ORDER_DISPATCHED,'Order Dispatched'),(ORDER_DELIVERED,'Order Delivered'),(ORDER_CANCELLED,'Order Cancelled'))
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,related_name='order',null=True)
    status = models.IntegerField(choices=status_choices,default=CART_STAGE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,related_name='order_item',null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,related_name='order_item',null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.product.name) 

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,related_name='shipping_address',null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,related_name='shipping_address',null=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address       
    
class Payment(models.Model):
    cass_on_delivery = 0
    credit_card = 1
    status_choices = ((cass_on_delivery,'Cash On Delivery'),(credit_card,'Credit Card'))
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,related_name='payment',null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,related_name='payment',null=True)
    amount = models.FloatField()
    status = models.IntegerField(choices=status_choices,default=cass_on_delivery)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.amount)    

        
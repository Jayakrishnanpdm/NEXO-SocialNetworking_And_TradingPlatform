from django.shortcuts import render
from Products.models import Product
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
def cart(request,id): 
        ordered_items=None
        quantity=1
        user=request.user.customer_profile
        order,created=Order.objects.get_or_create(owner=user,order_status=Order.CART_STAGE)
        product=Product.objects.get(id=id)
        user=request.user.customer_profile
        order, created=Order.objects.get_or_create(owner=user,order_status=Order.CART_STAGE)
        existing_item=OrderItem.objects.filter(product=product,quantity=quantity,order=order).first()
        if existing_item:
            existing_item.quantity=existing_item.quantity+quantity
            existing_item.save()
        else:
            item=OrderItem.objects.create(product=product,quantity=quantity,order=order)
        ordered_items=OrderItem.objects.filter(order=order)
        return render(request,'cart.html',{'ordered_items':ordered_items})
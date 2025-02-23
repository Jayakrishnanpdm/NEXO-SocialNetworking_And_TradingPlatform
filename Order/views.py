from django.shortcuts import render,redirect
from Products.models import Product
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, F
# Create your views here.
@login_required(login_url='/signin/')
def cart(request): 
    user=request.user.customer_profile
    order,created=Order.objects.get_or_create(customer=user,complete=False,status=Order.CART_STAGE)
    if request.method=='POST':
        id=request.POST.get('product_id') 
        product=Product.objects.get(id=id)
        existing_order_item=OrderItem.objects.filter(order=order,product=product)
        if existing_order_item.exists():
            order_item=existing_order_item[0]
            order_item.quantity+=1
            order_item.save()
        else:
            order_item=OrderItem.objects.create(product=product,order=order,quantity=1)
    total_price = order.items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0
    print("Total Price Value:", total_price)
    print("Total Price Type:", type(total_price))
    return render(request,'cart.html',{'order_items':order.items.all(),'total_price':total_price})

def removeItem(request,id):
    order_item=OrderItem.objects.get(id=id)
    product=order_item.product
    user=request.user.customer_profile
    order=Order.objects.get(customer=user,status=Order.CART_STAGE)
    existing_order_item=OrderItem.objects.filter(order=order,product=product)
    if existing_order_item.exists():
        order_item=existing_order_item[0]
        order_item.quantity-=1
        order_item.save()
        if order_item.quantity==0:
            order_item.delete()
    return redirect('cart')

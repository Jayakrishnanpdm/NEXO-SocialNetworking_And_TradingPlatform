from django.shortcuts import render,redirect
from Products.models import Product
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.core.mail import send_mail
from django.conf import settings
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

def checkout(request):  
    user=request.user.customer_profile
    order=Order.objects.get(customer=user,status=Order.CART_STAGE)
    total_price = 0
    if order:
        total_price = order.items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0
        request.session["cart_visited"] = True    
    return render(request,'checkout.html',{'total_price':total_price})

def orderConfirm(request):
    if not request.session.get("payment_visited"):
        return redirect("payment") 
    user=request.user.customer_profile
    order=Order.objects.get(customer=user,status=Order.CART_STAGE)
    total_price = order.items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0

    # Fetch product and seller details
    order_items = order.items.all()
    product_details = []
    for item in order_items:
        product_details.append(f"Product: {item.product.name},Seller: {item.product.seller.name},Phone: {item.product.seller.phone}")

    # Create email content
    subject = "Order Details & Seller Information"
    message = f"Dear {user.name},\n\nHere are the seller details for your order:\n\n"
    message += "\n".join(product_details)
    message += f"\n\nTotal Price: ₹{total_price}"
    message += "\n\nPlease contact the seller for any queries regarding the product.\n\n"
    message += "\nThank you for shopping with us!"


    # Send email
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Sender email
        [request.user.email],  # Customer email
        fail_silently=False
    )

    order.complete=True
    order.status=Order.ORDER_CONFIRMED
    order.save()
    payment_method = request.session.pop("payment_method","Not Available")
    request.session.pop("cart_visited", None)
    request.session.pop("payment_visited", None)
    context={'total_price':total_price,'payment_method':payment_method.replace("_", " ").title(),'order':order}
    return render(request,'order_confirm.html',context) 
from django.shortcuts import render

# Create your views here.
def cart(request): 
    return render(request, 'cart.html') # This is the view that will be rendered when the user visits the order page.

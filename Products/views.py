from django.shortcuts import render

# Create your views here.
def products(request):
    return render(request, 'products.html') # This is the view that will be rendered when the user visits the products page.


def product_detail(request):
    return render(request, 'product_detail.html') # This is the view that will be rendered when the user visits the product detail page.


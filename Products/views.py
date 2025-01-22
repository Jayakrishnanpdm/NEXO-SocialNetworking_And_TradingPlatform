from django.shortcuts import render
from .models import Product, ProductImage

# Create your views here.

def products(request):
    # Fetch all products with their first image
    products_with_images = []
    for product in Product.objects.all():
        first_image = product.images.first()  # Use the related_name 'images' to get images
        products_with_images.append({
            'product': product,
            'image': first_image.image.url if first_image else None  # Handle case where no image exists
        })
    return render(request, 'products.html',{'products_with_images':products_with_images}) # This is the view that will be rendered when the user visits the products page.


def product_detail(request):
    return render(request, 'product_detail.html') # This is the view that will be rendered when the user visits the product detail page.


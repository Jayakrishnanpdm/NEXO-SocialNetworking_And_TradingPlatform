from django.shortcuts import render
from Products.models import Product, ProductImage

# Create your views here.
def home(request):
    products_with_images_priority = []
    for product in Product.objects.filter(priority__lt=5).order_by('priority'):
        first_image = product.images.first()  # Use the related_name 'images' to get images
        products_with_images_priority.append({
            'product': product,
            'image': first_image.image.url if first_image else None  # Handle case where no image exists
        })

    products_with_images_id = []
    products_with_images_id = [
        {
            'product': product,
            'image': product.images.first().image.url if product.images.first() else None
        }
        for product in Product.objects.all().order_by('-id')[:4]
    ]   
    return render(request, 'home.html',{'products_with_images_priority':products_with_images_priority, 'products_with_images_id':products_with_images_id})

def contact(request):
    return render(request, 'contact.html') 

def about(request): 
    return render(request, 'about.html')

def sell(request):
    return render(request, 'sell.html') 
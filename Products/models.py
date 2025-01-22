from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Product(models.Model):
    model = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    priority = models.IntegerField(default=0)
    digital = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f"Image for {self.product.name}"

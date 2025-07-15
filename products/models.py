from django.db import models
from users.models import Base
from django.conf import settings

# Create your models here.


class Category(Base):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name
    


class Product(Base):
    title = models.CharField(max_length=100, verbose_name="Nomi")
    description = models.TextField(verbose_name="Tavsifi")
    image = models.ImageField(upload_to='products/', verbose_name="Rasm")
    price = models.PositiveIntegerField(verbose_name="Narxi (so'mda)")
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Product")

    def __str__(self):
        return self.title
    

class Cart(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    is_ordered = models.BooleanField(default=False) 

    def __str__(self):
        return f"Savat (User: {self.user.username})"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def product_list(self):
        return ", ".join([item.product.title for item in self.items.all()])


class CartItem(Base):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

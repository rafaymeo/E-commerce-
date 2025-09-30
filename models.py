# yourapp/models.py

from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)  # Store hashed password only

    def __str__(self):
        return self.username

from django.db import models

class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True)
    available_sizes = models.CharField(max_length=1, choices=SIZE_CHOICES, default='M')
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=20)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"Order by {self.first_name} {self.last_name}"


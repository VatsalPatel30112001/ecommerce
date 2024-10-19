from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator

class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)  
    email = models.EmailField(max_length=100, unique=True, blank=False)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Product(models.Model):    
    name = models.CharField(max_length=100, unique=True, blank=False)  
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MaxValueValidator(25)])

    def __str__(self):
        return self.name

class Order(models.Model):
    order_number = models.CharField(max_length=10, unique=True)
    order_date = models.DateField()
    address = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')

    def save(self, *args, **kwargs):
        if not self.order_number: 
            last_order = Order.objects.all().order_by('id').last()
            if last_order:
                last_order_number = last_order.order_number
                order_int = int(last_order_number.split('ORD')[-1]) + 1
                new_order_number = f'ORD{order_int:05d}'
            else:
                new_order_number = 'ORD00001'

            self.order_number = new_order_number

        super().save(*args, **kwargs)  

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
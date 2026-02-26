# Django autodiscovery shim for clean-architecture models
from django.db import models
class orders(models.Model):
    orderNumber=models.CharField(max_length=255)
    total=models.FloatField()
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def calculateTotal(self):
        total=sum(item.calculateSubtotal() for item in self.items.all())
        self.total=total
        return self.total
    def __str__(self):
        return self.orderNumber
    
class orderItems(models.Model):
    order=models.ForeignKey('orders.orders', related_name='items', on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.FloatField()

    def calculateSubtotal(self):
        return self.quantity * self.price



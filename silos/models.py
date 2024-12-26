from django.db import models
from farmers.models import User

class Silo(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    current_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    def available_space(self):
        """Returns the remaining available space in the silo."""
        return self.capacity - self.current_stock

class SiloLog(models.Model):
    silo = models.ForeignKey(Silo, on_delete=models.CASCADE, related_name='logs')
    change_type = models.CharField(max_length=50, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')])
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.silo.name} at {self.timestamp}"

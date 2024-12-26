from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=[('manager', 'Manager'), ('farmer', 'Farmer')])

    # Set the USERNAME_FIELD to email to make it the login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    # Fix the reverse accessor clash
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='farmers_user_set',  # Unique related_name
        blank=True, 
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='farmers_user_permissions',  # Unique related_name
        blank=True, 
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.name

class Order(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    grain_type = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Pending')  # e.g., Pending, Approved, Rejected
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.grain_type}"
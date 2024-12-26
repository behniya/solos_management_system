from rest_framework import serializers
from .models import User, Order
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['name'],  # Use 'name' as the username
            name=validated_data['name'],
            role=validated_data.get('role')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'farmer', 'grain_type', 'quantity', 'status', 'created_at']
        read_only_fields = ['created_at']

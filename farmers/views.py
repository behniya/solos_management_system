from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User, Order
from .serializers import UserSerializer, OrderSerializer
from django.contrib.auth import authenticate

# Registration
class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login
class LoginView(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            if user.check_password(password): 
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': user.role,
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


# Orders
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        if user.role == 'manager':
            orders = Order.objects.all()

        else:  # farmer
            orders = Order.objects.filter(farmer=user)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    

    def post(self, request):

        if request.user.role != 'farmer':
            return Response({'error': 'Only farmers can create orders'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        data['farmer'] = request.user.id
        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            order = Order.objects.get(pk=pk)
            if request.user.role == 'farmer' and order.farmer != request.user:
                return Response({'error': 'You can only view your own orders'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):

        try:
            order = Order.objects.get(pk=pk)
            if request.user.role == 'farmer' and order.farmer != request.user:
                return Response({'error': 'You can only edit your own orders'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


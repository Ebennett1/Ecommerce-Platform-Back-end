from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from rest_framework import generics, status
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import UserSerializer, RegisterSerializer, CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return HttpResponse("Welcome to the home page!")

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        try:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            return cart
        except Exception as e:
            logger.error(f"Failed to fetch cart: {e}")
            raise

class AddToCart(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        try:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            product = Product.objects.get(id=request.data['product_id'])
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += request.data['quantity']
                cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            logger.error('Product not found')
            return Response({'detail': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error adding to cart: {e}')
            return Response({'detail': 'Error adding to cart'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateCartItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Validate that quantity is not negative
        quantity = request.data.get('quantity')
        if quantity is not None and int(quantity) < 0:
            return Response({"detail": "Quantity cannot be negative"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

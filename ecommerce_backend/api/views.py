from django.shortcuts import render
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from rest_framework import generics, status
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import UserSerializer, RegisterSerializer, CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer, MyTokenObtainPairSerializer
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

# Custom Token Obtain Pair View
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        logger.debug(f"Login attempt with data: {request.data}")
        response = super().post(request, *args, **kwargs)
        logger.debug(f"Response data: {response.data}")
        return response

# Home View
def home(request):
    return HttpResponse("Welcome to the home page!")

# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# User Detail View
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Category Views
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Product Views
class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category_id')
        search_query = self.request.query_params.get('search')
        
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        
        if search_query is not None:
            queryset = queryset.filter(name__icontains=search_query)
        
        return queryset


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Cart Views
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
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        # Validate that quantity is not negative
        quantity = request.data.get('quantity')
        if quantity is not None and int(quantity) < 0:
            return Response({"detail": "Quantity cannot be negative"}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f"Updating cart item {instance.id} with quantity {quantity}")
        data = {'quantity': quantity}

        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated cart item: {serializer.data}")
            return Response(serializer.data)
        else:
            logger.error(f"Failed to update cart item: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Order Views
class OrderCreate(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        logger.debug(f"Order creation request data: {request.data}")
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Order created successfully: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Order creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    


class ClearOrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        orders.delete()
        return Response({"message": "Order history cleared."}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reorder(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        cart, created = Cart.objects.get_or_create(user=request.user)
        for item in order.items.all():
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item.product)
            if not created:
                cart_item.quantity += item.quantity
                cart_item.save()
        return Response({"message": "Items added to cart"}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def create_payment_intent(request):
    try:
        total_price = request.data['total_price']
        intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),  # amount in cents
            currency='usd',
            metadata={'integration_check': 'accept_a_payment'},
        )
        return Response({'clientSecret': intent['client_secret']})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

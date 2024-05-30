from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_id', 'quantity', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Update the instance with the validated data
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        order = Order.objects.create(user=user, total_price=0)  # Initial total_price, will update later

        cart_items = CartItem.objects.filter(cart__user=user)
        total_price = 0

        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total_price += item.product.price * item.quantity

        order.total_price = total_price
        order.save()

        # Clear the cart
        cart_items.delete()

        return order

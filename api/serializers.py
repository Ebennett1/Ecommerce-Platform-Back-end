from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Category, Product, Cart, CartItem, Order, OrderItem
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Custom JWT serializer to include additional user data in the token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token
    
# Serializer for the Profile model
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number']

# Serializer for the User model, including the related Profile
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile = instance.profile
        profile.phone_number = profile_data.get('phone_number', profile.phone_number)
        profile.save()

        return instance

# Serializer for user registration, creating a user and their profile
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
        Profile.objects.create(user=user)  # Create an associated profile for the new user
        return user

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Serializer for the Product model
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# Serializer for the CartItem model
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

# Serializer for the Cart model
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

# Serializer for the OrderItem model
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

# Serializer for the Order model
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
            OrderItem.objects.create(
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

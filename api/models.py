from django.db import models
from django.contrib.auth.models import User

# Profile model to extend the default Django User model with additional fields
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to the Django User model, one-to-one relationship
    phone_number = models.CharField(max_length=15, blank=True)   # Optional phone number field

    def __str__(self):
        return self.user.username  # Returns the username of the associated User

# Category model to represent product categories
class Category(models.Model):
    name = models.CharField(max_length=255)                      # Name of the category
    description = models.TextField(blank=True, null=True)        # Optional description of the category

    def __str__(self):
        return self.name  # Returns the name of the category

# Product model to represent products in the store
class Product(models.Model):
    name = models.CharField(max_length=255)                      # Name of the product
    description = models.TextField()                             # Detailed description of the product
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price of the product
    stock = models.IntegerField(default=0)                       # Stock quantity available
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)  # Foreign key to Category, allows null
    image = models.CharField(max_length=500, null=True, blank=True) # Optional URL to product image
    created_at = models.DateTimeField(auto_now_add=True)         # Timestamp for when the product was created
    updated_at = models.DateTimeField(auto_now=True)             # Timestamp for when the product was last updated

    def __str__(self):
        return self.name  # Returns the name of the product

# Cart model to represent a shopping cart for a user
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to the Django User model, one-to-one relationship
    created_at = models.DateTimeField(auto_now_add=True)         # Timestamp for when the cart was created

    def __str__(self):
        return f"Cart of {self.user.username}"  # Returns a string representation of the cart and the associated user

# CartItem model to represent items in a shopping cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)  # Foreign key to Cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)                  # Foreign key to Product
    quantity = models.PositiveIntegerField(default=1)                               # Quantity of the product in the cart
    created_at = models.DateTimeField(auto_now_add=True)                            # Timestamp for when the cart item was created
    updated_at = models.DateTimeField(auto_now=True)                                # Timestamp for when the cart item was last updated

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"  # Returns a string representation of the product and its quantity in the cart

# Order model to represent a user's order
class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),  # Order is being processed
        ('shipped', 'Shipped'),        # Order has been shipped
        ('delivered', 'Delivered'),    # Order has been delivered
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)                     # Foreign key to the Django User model
    total_price = models.DecimalField(max_digits=10, decimal_places=2)           # Total price of the order
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing')  # Status of the order
    created_at = models.DateTimeField(auto_now_add=True)                         # Timestamp for when the order was created
    updated_at = models.DateTimeField(auto_now=True)                             # Timestamp for when the order was last updated

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"  # Returns a string representation of the order and the associated user

# OrderItem model to represent items in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Foreign key to Order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)                    # Foreign key to Product
    quantity = models.PositiveIntegerField()                                          # Quantity of the product in the order
    price = models.DecimalField(max_digits=10, decimal_places=2)                      # Price of the product at the time of order

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"  # Returns a string representation of the product and its quantity in the order

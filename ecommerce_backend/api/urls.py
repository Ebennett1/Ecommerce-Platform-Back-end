from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MyTokenObtainPairView
from django.contrib.auth import views as auth_views
from .views import (
    RegisterView, UserProfileUpdateView, CategoryList, ProductList, ProductDetail,
    CartDetail, AddToCart, UpdateCartItem, OrderCreate, OrderHistoryView,
    ClearOrderHistoryView, create_payment_intent, reorder, PasswordResetView
)

urlpatterns = [
    # User registration endpoint
    path('register/', RegisterView.as_view(), name='register'),
    
    # JWT authentication endpoints
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile update endpoint
    path('profile/', UserProfileUpdateView.as_view(), name='profile-update'),
    
    # Password reset endpoint
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    
    # Category endpoints
    path('categories/', CategoryList.as_view(), name='category-list'),
    
    # Product endpoints
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    
    # Cart endpoints
    path('cart/', CartDetail.as_view(), name='cart-detail'),
    path('cart/add/', AddToCart.as_view(), name='add-to-cart'),
    path('cart/update/<int:pk>/', UpdateCartItem.as_view(), name='update-cart-item'),
    
    # Order endpoints
    path('orders/create/', OrderCreate.as_view(), name='order-create'),
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
    path('order-history/clear/', ClearOrderHistoryView.as_view(), name='clear-order-history'),
    path('order-history/reorder/<int:order_id>/', reorder, name='reorder'),
    
    # Payment intent creation endpoint
    path('create-payment-intent/', create_payment_intent, name='create-payment-intent'),
]

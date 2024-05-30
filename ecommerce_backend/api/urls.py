from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MyTokenObtainPairView
from .views import RegisterView, UserDetailView, CategoryList, ProductList, ProductDetail, CartDetail, AddToCart, UpdateCartItem, OrderCreate, OrderList, OrderDetail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('cart/', CartDetail.as_view(), name='cart-detail'),
    path('cart/add/', AddToCart.as_view(), name='add-to-cart'),
    path('cart/update/<int:pk>/', UpdateCartItem.as_view(), name='update-cart-item'),
    path('orders/create/', OrderCreate.as_view(), name='order-create'),
    path('orders/', OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
]








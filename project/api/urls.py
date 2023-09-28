from django.urls import path, include, re_path
from rest_framework import routers
from .views import *
from djoser.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'users', UserViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('signup/', CustomUserCreateView.as_view(), name='register'),
    path('login', CustomObtainAuthToken.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('cart/<int:product_id>', CartProductsView.as_view(), name='cart_add'),
    path('cart', CartProductsView.as_view(), name='cart'),
    path('product/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='products'),
    path('product/<int:pk>', ProductViewSet.as_view({'delete': 'destroy', 'patch': 'partial_update'}), name='product_remove'),
    path('cart_remove/<int:pk>', CartProductsView.as_view(), name='cart_product_remove'),
    path('order/', Order.as_view(), name='order_create')
]


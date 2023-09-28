from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from djoser.serializers import UserCreateSerializer
from django.utils.translation import gettext_lazy as _

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']

class ClientSerializer(UserCreateSerializer):
    class Meta:
        model = Client
        fields = ['username', 'fio', 'email', 'password']

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"), style={'input_type': 'password'},
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = {'email': _('Email or password is incorrect.')}
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = {'email': _('This field is required.')}
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CartProductsSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')
    description = serializers.CharField(source='product.description')
    price = serializers.IntegerField(source='product.price')

    class Meta:
        model = CartProducts
        fields = ['id', 'product_id', 'name', 'description', 'price']



class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'cart_products']

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product']

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'order_price']




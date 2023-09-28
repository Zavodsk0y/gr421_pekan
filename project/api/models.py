from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, MinLengthValidator

class Product(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Client(AbstractUser):
    username = models.CharField(max_length=60, unique=True)
    fio = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, validators=[EmailValidator(message='Ошибка валидации почты')])
    password = models.CharField(max_length=255, validators=[MinLengthValidator(6, message='Введен пароль длиной менее 6-ти символов!')])
    REQUIRED_FIELDS = ['username', 'fio', 'password']

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cart')

class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_price = models.IntegerField()

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)








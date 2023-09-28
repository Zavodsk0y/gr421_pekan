from djoser import utils
from rest_framework import viewsets, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import *



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action == 'create' or self.action == 'delete' or self.action == 'patch':
            return [IsAdminUser()]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Proudct removed'}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.perform_create(serializer)
        response_data = {
            'id' : serializer.data['id'],
            'message': 'Product added'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomUserCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=user)
        token_key = token.key
        return Response({'auth_token': token_key}, status=status.HTTP_201_CREATED)
    def perform_create(self, serializer):
        user = serializer.save()
        return user

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_401_UNAUTHORIZED)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        token_key = token.key
        return Response({'auth_token': token_key}, status=status.HTTP_200_OK)

class Logout(APIView):
    def get(self, request):
        utils.logout_user(request)
        return Response({"message": "logout"}, status=status.HTTP_200_OK)


class IsGuest(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated

class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        raise PermissionDenied(detail="Access Forbidden", code=status.HTTP_403_FORBIDDEN)

class CartProductsView(APIView):
    permission_classes = [CustomIsAuthenticated]
    http_method_names = ['post', 'get', 'delete']

    def get_object(self, pk):
        try:
            return CartProducts.objects.get(pk=pk)
        except CartProducts.DoesNotExist:
            raise Http404

    def post(self, request, product_id):
        if not request.auth:
            raise PermissionDenied("Access Forbidden", code=403)
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(client=request.user)
        cart_product = CartProducts.objects.create(cart=cart, product_id=product_id)
        return Response({'message': 'Product added to cart'}, status=status.HTTP_200_OK)

    def get(self, request):
        cart = Cart.objects.get(client=request.user)
        cart_products = CartProducts.objects.filter(cart=cart)
        serializer = CartProductsSerializer(cart_products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cart_product = self.get_object(pk)
        cart_product.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
class Order(APIView):
    permission_classes = [CustomIsAuthenticated]

    def post(self, request):
        client = request.user
        cart = client.cart.first()
        if not cart:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        cart_products = cart.cart_products.all()
        if not cart_products:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        order_price = sum(cart_product.product.price for cart_product in cart_products)
        order = Order.objects.create(client=client, order_price=order_price)

        for cart_product in cart_products:
            OrderProduct.objects.create(order=order, product=cart_product.product)

        cart.cart_products.clear()

        response_data = {
            "order_id": order.id,
            "message": "Order is processed"
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def get(self, request):
        client = request.user
        orders = Order.objects.filter(client=client)
        response_data = []
        for order in orders:
            order_data = {
                "id": order.id,
                "products": [order_product.product.id for order_product in order.orderproduct_set.all()],
                "order_price": order.order_price
            }
            response_data.append(order_data)

        return Response(response_data, status=status.HTTP_200_OK)


















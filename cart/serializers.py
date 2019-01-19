from rest_framework import serializers
from .models import Cart, Cart_items
from products.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['card_id', 'title', 'price', 'time_created', 'time_completed', 'total']

class Cart_itemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    cart = CartSerializer(read_only=True)

    class Meta:
        model = Cart_items
        fields = ['cart_item_id', 'cart', 'product', 'quantity']

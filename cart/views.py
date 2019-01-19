from .models import Cart, Cart_items
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from products.models import Product
from rest_framework.exceptions import NotFound, ParseError
from django.db import transaction
from rest_framework import status

@api_view(["GET"])
def add_to_cart(request, p_id):
    user = authenticate(request, username=request.GET["username"], password=request.GET["password"])
    print(request.GET["username"], request.GET["password"])
    print(user)
    try:
        product = Product.objects.get(pk=p_id)
        quantity = int(float(request.GET["quantity"]))
        if quantity < 1:
            raise ParseError("The number of items to be added must be at least 1")
        elif product.inventory_count == 0 or product.inventory_count < quantity < 1:
            raise ParseError("The product {0} does not have sufficient inventory".format(p_id))

    except ObjectDoesNotExist:
        raise NotFound("Product {0} is not found, please try another product".format(p_id))

    try:
        cart = Cart.objects.get(customer=user)
    except ObjectDoesNotExist:
        cart = Cart.objects.create(customer=user)

    try:
        cart_item = Cart_items.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
    except ObjectDoesNotExist:
        cart_item = Cart_items.objects.create(cart=cart, product=product, quantity=quantity)

    cart.total += quantity * float(product.price)
    cart.save()
    cur_cart = {}
    for item in Cart_items.objects.filter(cart=cart):
        cur_cart[item.product.title] = item.quantity

    return JsonResponse({'Status': "Product {0} is added successfully to the shopping cart".format(p_id), "Cart":cur_cart})


@api_view(["GET"])
def check_out(request):
    user = authenticate(request, username=request.GET["username"], password=request.GET["password"])
    try:
        cart = Cart.objects.get(customer=user)
        final_cart = {}
        for item in Cart_items.objects.filter(cart=cart):
            with transaction.atomic():
                product = Product.objects.select_for_update().get(pk=item.product.id)
                final_cart[item.product.title] = item.quantity
                if product.inventory_count < item.quantity:
                    return JsonResponse({'Detail': "The product {} does not have sufficient inventory".format(product.id)})
                product.inventory_count -= item.quantity
                product.save()
        Cart.objects.filter(cart=cart).delete()
        return JsonResponse({'Status': "Shopping card check out successfully", 'Cart': final_cart})

    except ObjectDoesNotExist:
        raise NotFound("You don't have a cart, add something before check out")


@api_view(["GET"])
def remove_item(request, p_id):
    user = authenticate(request, username=request.GET["username"], password=request.GET["password"])
    print(request.GET["username"], request.GET["password"])
    print(user)
    try:
        product = Product.objects.get(pk=p_id)
    except ObjectDoesNotExist:
        raise NotFound("The product you are trying to remove is not found")
    try:
        cart = Cart.objects.get(customer=user)
        cart_item = Cart_items.objects.filter(cart=cart, product=product).first()
        if cart_item:
            quantity = int(float(request.GET["quantity"]))
            if quantity >= cart_item.quantity:
                Cart_items.objects.filter(cart=cart, product=product).delete()
            else:
                cart_item.quantity -= quantity
                cart_item.save()
            cur_cart = {}
            for item in Cart_items.objects.filter(cart=cart):
                cur_cart[item.product.title] = item.quantity
            return JsonResponse({'Status': "Product{0} is adjusted successfully in your shopping cart", 'Cart': cur_cart})
        else:
            raise NotFound("You don't have this product at your cart")

    except ObjectDoesNotExist:
        raise NotFound("You don't have a cart, add something before remove")

@api_view()
def ask_login(request):
    content = "please go to /login to login as test_user"
    return Response(content, status=status.HTTP_401_UNAUTHORIZED)


def login_fake(request):
    user = authenticate(request, username = 'test_user', password='temp_password')
    if user is not None:
        login(request, user)
        return JsonResponse({"result": 'Login Successful'})
    else:
        return JsonResponse({"result": 'Login Failed'})


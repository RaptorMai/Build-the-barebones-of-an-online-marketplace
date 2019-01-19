from .models import Cart, Cart_items
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from products.models import Product
from rest_framework.exceptions import NotFound, ParseError
from django.db import transaction

@api_view(["GET"])
@login_required(login_url='/ask_login')
def add_to_cart(request, p_id):
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
        cart = Cart.objects.get(customer=request.user)
    except ObjectDoesNotExist:
        cart = Cart.objects.create(customer=request.user)

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
@login_required(login_url='/ask_login')
def check_out(request):
    try:
        cart = Cart.objects.get(customer=request.user)
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
@login_required(login_url='/ask_login')
def remove_item(request, p_id):
    try:
        product = Product.objects.get(pk=p_id)
    except ObjectDoesNotExist:
        raise NotFound("The product you are trying to remove is not found")
    try:
        cart = Cart.objects.get(customer=request.user)
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

def ask_login(request):
    return HttpResponse("please go to /login to login as test_user")

def login_fake(request):
    user = authenticate(request, username = 'test_user', password='temp_password')
    if user is not None:
        login(request, user)
        return JsonResponse({"result": 'Login Successful'})
    else:
        return JsonResponse({"result": 'Login Failed'})


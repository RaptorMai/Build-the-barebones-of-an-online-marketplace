from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        in_stock = self.request.query_params.get('in_stock', None)
        if in_stock == 'True':
            queryset = Product.objects.exclude(inventory_count=0)
        return queryset

@api_view(["GET"])
def product_purchase(request, p_id):
    product = get_object_or_404(Product, pk=p_id)
    if product.inventory_count > 0:
        product.inventory_count -= 1
        product.save()
        return JsonResponse({'status': "Purchased Product {0} Successful".format(p_id)})
    else:
        return JsonResponse({'status': "Purchased Product {0} has zero inventory right now".format(p_id)})
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('products', views.ProductView, base_name='products')

urlpatterns = [
    path('<int:p_id>/checkout/', views.product_purchase, name='checkout'),
]

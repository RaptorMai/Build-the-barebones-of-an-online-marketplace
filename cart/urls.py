from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('cart', CartView, base_name='cart')

urlpatterns = [
    path('add/<int:p_id>/', views.add_to_cart, name='add_cart'),
    path('checkout', views.check_out, name='checkout'),
    path('remove_item/<int:p_id>/', views.remove_item, name='remove_item'),

]

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from products.urls import router as product_router
from products.urls import router as cart_router
import cart.views as cart_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    url(r'^login/$', cart_views.login_fake, name='userlogin'),
    url(r'^ask_login/$', cart_views.ask_login, name='ask_login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='/products'), name='userlogout'),
]

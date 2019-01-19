from django.db import models
from products.models import Product
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Cart Model
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)
    time_completed = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(default=0.00, validators=[MinValueValidator(0, "total can't be smaller than zero")])

    def __str__(self):
        if self.completed:
            return "Cart{0} with total {1} is completed".format(self.cart_id, self.total)
        else:
            return "Cart{0} with total {1} is not completed".format(self.cart_id, self.total)




class Cart_items(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "Cart{0} has {1} product{2}".format(self.cart, self.quantity. self.product)
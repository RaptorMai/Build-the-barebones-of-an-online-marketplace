from django.db import models


class Product(models.Model):
    """ Product field """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    inventory_count = models.PositiveIntegerField()

    def __str__(self):
        return self.title
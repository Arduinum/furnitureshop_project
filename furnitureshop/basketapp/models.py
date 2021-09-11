from django.db import models

from furnitureshop import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name='колличество',
        default=0
    )
    add_datetime = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True
    )

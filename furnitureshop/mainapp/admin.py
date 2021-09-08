from django.contrib import admin
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser


admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ShopUser)

from django.contrib import admin

from .models import Courier, CartItem, Cart

admin.site.register(Courier)
admin.site.register(CartItem)
admin.site.register(Cart)

from django.contrib import admin
from .models import Category, Book, CartItem, Order, OrderItem

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)



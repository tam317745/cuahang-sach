from django.contrib import admin
from .models import Category, Book, CartItem, Order, OrderItem
from django.core.files.storage import default_storage

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'storage_backend')

    def storage_backend(self, obj):
        return default_storage.__class__.__name__
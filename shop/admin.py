from django.contrib import admin
from .models import CustomUser, Category, Product, Order, OrderUpdate, ContactUs

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(OrderUpdate)
admin.site.register(ContactUs)


# class OrdersInline(admin.TabularInline):
#     model = Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'unit_type', 'per_unit_price',
                    'available_quantity', 'publish_date', 'category')

    list_filter = ('product_id', 'product_name', 'available_quantity', 'category')
    # inlines = [OrdersInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'first_name', 'email', 'state', 'status', 'display_ordered_item')
    list_filter = ('order_id', 'state', 'status')

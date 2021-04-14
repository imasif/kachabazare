from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Product, Order, OrderUpdate, ContactUs, Category

# Register your models here.
# admin.site.register(Group)
admin.site.register(User)
# admin.site.register(Category)
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_filter = ('title',)
    search_fields = ('title', 'slug')
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'first_name', 'email', 'state', 'status', 'display_ordered_item',)
    list_filter = ('order_id', 'state', 'status')

    # def last_activity_planned_date(self, obj):
    #     return ("%s " % (obj.first_name,)).upper()
    #     upper_case_name.short_description = 'Name'
        # if latest_activity and latest_activity.status_id == 2:
        #     return latest_activity.planned_execution_date
        # else:
        #     return None

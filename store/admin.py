from django.contrib import admin, messages
from django.db.models import Count, F,QuerySet
from django.utils.html import format_html, urlencode    
from django.urls import reverse

from . import models
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"
    less_than_10 = "<10"
    
    def lookups(self, request,model_admin):
        return [
            (self.less_than_10,"Low")
        ]
        
    def queryset(self, request, queryset:QuerySet):
        if self.value() == self.less_than_10:
            return queryset.filter(inventory__lt=10)
        # return queryset
    
    
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'products_count'
    ]   
    list_per_page = 10
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # reverse("admin:app_model_page")
        url = (
            reverse("admin:store_product_changelist")
            + '?'
            + urlencode({
                "collection__id":str(collection.id)
            })
        ) # filtering products
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        # return collection.products_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = [
        'title',
        'unit_price',
        'inventory',
        "inventory_status",
        "collection_title",
        ]
    list_editable = ['unit_price']
    list_filter = ['collection','last_update',InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title__istartswith']
    
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return "Low"
        return "OK"
    
    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset:QuerySet):
        updated_count = queryset.update(inventory=1)
        self.message_user(
            request,
            f"{updated_count} products were updated successfully",
            messages.SUCCESS
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'membership',
        "order_made"
        ]
    list_prefetch_related = ['order_set'] 
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']
    
    @admin.display(ordering='order_made')
    def order_made(self,customer):
        url = (
            reverse("admin:store_order_changelist")
            + '?'    
            + urlencode({
                "customer__id":str(customer.id)
            })
        )
        return format_html('<a href="{}">{}</a>',url, customer.order_made)
        # return customer.order_made
        
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_made=Count("order")
        )
        
        
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'placed_at',
        'payment_status', 
        'customer','email'
        ]
    list_per_page = 10
    list_select_related = ['customer']
    
    def customer (self, order):
        return order.customer
    
    def email(self, order):
        return order.customer.email
    
    

# admin.site.register(models.Product, ProductAdmin)
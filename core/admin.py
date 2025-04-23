from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


# Register your models here.


class TagInline(GenericStackedInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 1
    
    
admin.site.unregister(Product)
    
@admin.register(Product)
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]
    
    
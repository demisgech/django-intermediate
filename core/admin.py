from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import User
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
     add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", 
                           "password1", "password2",
                           "email","first_name","last_name"
                           ),
            },
        ),
    )

class TagInline(GenericStackedInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 1
    
    
admin.site.unregister(Product)
    
@admin.register(Product)
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]
    
    
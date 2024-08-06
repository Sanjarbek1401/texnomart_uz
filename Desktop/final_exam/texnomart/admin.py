from django.contrib import admin
from django.contrib.auth.models import User,Group as auth_group
from .models import Category,Product,Comment,Attribute,AttributeValue,ProductAttribute,Image

# Register your models here.
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
admin.site.unregister(User)
admin.site.unregister(auth_group)

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']
    prepopulated_fields = {'slug':('category_name',)}

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug']
    prepopulated_fields = {'slug':('product_name',)}
    


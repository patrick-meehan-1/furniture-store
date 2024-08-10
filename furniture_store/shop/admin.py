from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'category', 'stock',
                    'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    list_per_page = 20
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'review', 'rating']
    list_editable = ['review', 'rating']
    list_per_page = 20

admin.site.register(Review, ReviewAdmin)
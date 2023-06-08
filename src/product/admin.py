from django.contrib import admin
from django.db.models import Count
from . import models

# Register your models here.

class ProductVariantPriceInline(admin.TabularInline):
    model = models.ProductVariantPrice
    extra=0
    min_num=1
    max_num=10 

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra=0
    min_num=1
    max_num=10

class ProductVariantInline(admin.TabularInline):
    model = models.ProductVariant
    extra=0
    min_num=1
    max_num=10

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["title", "sku"]
    inlines = [
        ProductVariantPriceInline,
        ProductImageInline,
        ProductVariantInline
    ]


@admin.register(models.Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display=["title"]
    inlines = [
        ProductVariantInline
    ]

@admin.register(models.ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
   list_display= [ "product","variant_title", "variant"]


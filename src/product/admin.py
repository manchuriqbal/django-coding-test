from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["title", "sku"]


@admin.register(models.Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display=["title"]

@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display= ["product"]

@admin.register(models.ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
   list_display= [ "product","variant_title", "variant"]

@admin.register(models.ProductVariantPrice)
class ProductVariantPriceAdmin(admin.ModelAdmin):
    list_display=["price", "stock", "product"]
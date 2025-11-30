from django.contrib import admin
from .models import Category, Product, ProductImage, ProductReview, Cart, CartItem, UserBehavior

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug']
    list_filter = ['parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'ai_recommended_price', 'stock', 'is_active', 'sales_count', 'views_count']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'sku']
    list_editable = ['price', 'ai_recommended_price', 'stock', 'is_active']
    inlines = [ProductImageInline]
    readonly_fields = ['views_count', 'sales_count', 'rating_average', 'rating_count']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'product__name']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['user__username']

@admin.register(UserBehavior)
class UserBehaviorAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'behavior_type', 'timestamp']
    list_filter = ['behavior_type', 'timestamp']
    search_fields = ['user__username', 'product__name']
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer_segment', 'total_orders', 'total_spent', 'average_order_value', 'created_at']
    list_filter = ['customer_segment', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_orders', 'total_spent', 'average_order_value', 'created_at', 'updated_at']
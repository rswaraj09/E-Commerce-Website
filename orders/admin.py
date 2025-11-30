from django.contrib import admin
from .models import Order, OrderItem, Payment, Shipping, OrderHistory

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['total']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'status', 'payment_status', 'total', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_id', 'user__username']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount', 'method', 'status', 'created_at']
    list_filter = ['method', 'status', 'created_at']
    search_fields = ['order__order_id', 'transaction_id']

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ['order', 'tracking_number', 'carrier', 'estimated_delivery']
    list_filter = ['carrier', 'estimated_delivery']
    search_fields = ['order__order_id', 'tracking_number']
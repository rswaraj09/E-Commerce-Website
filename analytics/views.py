from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg
from .models import SalesAnalytics, ProductAnalytics, CustomerAnalytics
from products.models import Product
from orders.models import Order
import json
from datetime import datetime, timedelta

@staff_member_required
def analytics_dashboard(request):
    """Main analytics dashboard"""
    # Get recent sales data
    recent_orders = Order.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=30)
    )
    
    total_revenue = recent_orders.aggregate(Sum('total'))['total__sum'] or 0
    total_orders = recent_orders.count()
    avg_order_value = recent_orders.aggregate(Avg('total'))['total__avg'] or 0
    
    # Get top products
    top_products = Product.objects.order_by('-sales_count')[:5]
    
    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'top_products': top_products,
    }
    
    return render(request, 'analytics/dashboard.html', context)

@staff_member_required
def sales_analytics(request):
    """Sales analytics page"""
    sales_data = SalesAnalytics.objects.order_by('-date')[:30]
    return render(request, 'analytics/sales.html', {'sales_data': sales_data})

@staff_member_required
def product_analytics(request):
    """Product analytics page"""
    products = Product.objects.order_by('-views_count')[:20]
    return render(request, 'analytics/products.html', {'products': products})

@staff_member_required
def customer_analytics(request):
    """Customer analytics page"""
    customers = CustomerAnalytics.objects.order_by('-total_spent')[:20]
    return render(request, 'analytics/customers.html', {'customers': customers})

@staff_member_required
def get_sales_data(request):
    """API endpoint for sales chart data"""
    sales_data = SalesAnalytics.objects.order_by('-date')[:30]
    
    data = {
        'dates': [item.date.strftime('%Y-%m-%d') for item in sales_data],
        'revenue': [float(item.total_revenue) for item in sales_data],
        'orders': [item.total_orders for item in sales_data],
    }
    
    return JsonResponse(data)

@staff_member_required
def get_product_data(request):
    """API endpoint for product performance data"""
    products = Product.objects.order_by('-sales_count')[:10]
    
    data = {
        'products': [product.name for product in products],
        'sales': [product.sales_count for product in products],
        'views': [product.views_count for product in products],
    }
    
    return JsonResponse(data)
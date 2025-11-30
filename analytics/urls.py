from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
    path('sales/', views.sales_analytics, name='sales_analytics'),
    path('products/', views.product_analytics, name='product_analytics'),
    path('customers/', views.customer_analytics, name='customer_analytics'),
    path('api/sales-data/', views.get_sales_data, name='api_sales_data'),
    path('api/product-data/', views.get_product_data, name='api_product_data'),
]



from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('order/<str:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('payment/<str:order_id>/', views.payment_view, name='payment'),
    path('payment/success/<str:order_id>/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]



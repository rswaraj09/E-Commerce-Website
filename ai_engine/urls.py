from django.urls import path
from . import views

app_name = 'ai_engine'

urlpatterns = [
    path('recommendations/', views.get_user_recommendations, name='recommendations'),
    path('train-models/', views.train_models, name='train_models'),
    path('update-pricing/', views.update_dynamic_pricing, name='update_pricing'),
    path('customer-segments/', views.customer_segmentation, name='customer_segments'),
]



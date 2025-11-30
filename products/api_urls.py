from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet)
router.register(r'categories', api_views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/<int:user_id>/', api_views.get_recommendations, name='api_recommendations'),
]



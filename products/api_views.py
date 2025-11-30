from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['GET'])
def get_recommendations(request, user_id):
    # Placeholder for AI recommendations
    # This will be implemented with the AI engine
    return Response({
        'user_id': user_id,
        'recommendations': [],
        'message': 'AI recommendations will be implemented'
    })



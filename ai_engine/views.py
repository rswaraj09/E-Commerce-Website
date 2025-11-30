from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import ProductRecommendation, CustomerSegment
from .ai_services import RecommendationEngine, PricingEngine, SegmentationEngine

@login_required
def get_user_recommendations(request):
    """Get AI-powered product recommendations for the user"""
    # This is a placeholder - will be implemented with actual ML models
    recommendations = ProductRecommendation.objects.filter(user=request.user)[:10]
    
    # For now, return some sample products as recommendations
    from products.models import Product
    sample_products = Product.objects.all()[:8]
    
    # Create recommendation-like objects for the template
    recommendation_data = []
    for i, product in enumerate(sample_products):
        recommendation_data.append({
            'product': product,
            'confidence_score': 85 + (i * 2),  # Sample confidence scores
            'algorithm': 'collaborative_filtering'
        })
    
    return render(request, 'ai_engine/recommendations.html', {
        'recommendations': recommendation_data
    })

@staff_member_required
def train_models(request):
    """Train/retrain AI models - admin only"""
    if request.method == 'POST':
        model_type = request.POST.get('model_type')
        
        try:
            if model_type == 'recommendations':
                engine = RecommendationEngine()
                result = engine.train_model()
            elif model_type == 'pricing':
                engine = PricingEngine()
                result = engine.train_model()
            elif model_type == 'segmentation':
                engine = SegmentationEngine()
                result = engine.train_model()
            else:
                result = {'success': False, 'message': 'Invalid model type'}
                
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'ai_engine/train_models.html')

@staff_member_required
def update_dynamic_pricing(request):
    """Update product prices using AI predictions"""
    try:
        engine = PricingEngine()
        updated_count = engine.update_all_prices()
        
        return JsonResponse({
            'success': True,
            'message': f'Updated pricing for {updated_count} products'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@staff_member_required
def customer_segmentation(request):
    """View customer segments"""
    segments = CustomerSegment.objects.all()
    return render(request, 'ai_engine/customer_segments.html', {
        'segments': segments
    })
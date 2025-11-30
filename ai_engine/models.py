from django.db import models
from django.contrib.auth.models import User

import pickle

class CustomerSegment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    criteria = models.JSONField()  # Store segmentation criteria
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ProductRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200, null=True, blank=True)
    score = models.FloatField()
    algorithm = models.CharField(max_length=50)  # collaborative, content-based, hybrid
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.product_name} ({self.score})"

class PricingModel(models.Model):
    product_name = models.CharField(max_length=200, null=True, blank=True)
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    confidence_score = models.FloatField()
    factors = models.JSONField()  # Store factors affecting price
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - ${self.predicted_price}"

class SalesForecast(models.Model):
    product_name = models.CharField(max_length=200, null=True, blank=True)
    forecast_date = models.DateField()
    predicted_sales = models.IntegerField()
    predicted_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    confidence_interval = models.FloatField()
    model_version = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Forecast for {self.forecast_date}"

class MLModel(models.Model):
    MODEL_TYPES = [
        ('recommendation', 'Recommendation Engine'),
        ('pricing', 'Dynamic Pricing'),
        ('segmentation', 'Customer Segmentation'),
        ('forecasting', 'Sales Forecasting'),
    ]
    
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    version = models.CharField(max_length=10)
    accuracy = models.FloatField(null=True, blank=True)
    model_data = models.BinaryField()  # Pickled model
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} v{self.version}"
    
    def save_model(self, model_object):
        self.model_data = pickle.dumps(model_object)
        self.save()
    
    def load_model(self):
        return pickle.loads(self.model_data)
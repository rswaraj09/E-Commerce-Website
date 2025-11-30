from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Category
from orders.models import Order

class SalesAnalytics(models.Model):
    date = models.DateField()
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unique_customers = models.IntegerField(default=0)
    conversion_rate = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ('date',)
    
    def __str__(self):
        return f"Sales Analytics - {self.date}"

class ProductAnalytics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    views = models.IntegerField(default=0)
    cart_additions = models.IntegerField(default=0)
    purchases = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    conversion_rate = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ('product', 'date')
    
    def __str__(self):
        return f"{self.product.name} - {self.date}"

class CategoryAnalytics(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    views = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        unique_together = ('category', 'date')
    
    def __str__(self):
        return f"{self.category.name} - {self.date}"

class CustomerAnalytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_order_date = models.DateTimeField(null=True, blank=True)
    days_since_last_order = models.IntegerField(default=0)
    predicted_ltv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    churn_probability = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Analytics - {self.user.username}"

class WebsiteAnalytics(models.Model):
    date = models.DateField()
    page_views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    bounce_rate = models.FloatField(default=0.0)
    session_duration = models.FloatField(default=0.0)  # in minutes
    
    class Meta:
        unique_together = ('date',)
    
    def __str__(self):
        return f"Website Analytics - {self.date}"
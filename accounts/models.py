from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # AI/ML related fields
    customer_segment = models.CharField(max_length=50, blank=True, null=True)
    lifetime_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase_frequency = models.IntegerField(default=0)
    last_purchase_date = models.DateTimeField(blank=True, null=True)
    preferred_categories = models.JSONField(default=list, blank=True)
    
    # Behavioral tracking
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def update_purchase_stats(self, order_total):
        """Update purchase statistics when a new order is placed"""
        self.total_orders += 1
        self.total_spent += order_total
        self.average_order_value = self.total_spent / self.total_orders
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

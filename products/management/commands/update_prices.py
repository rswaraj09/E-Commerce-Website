from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Update product prices with correct INR values'

    def handle(self, *args, **options):
        self.stdout.write('Updating product prices...')
        
        # Price updates for existing products
        price_updates = {
            'iPhone 15 Pro': 85000,
            'Samsung Galaxy S24': 75000,
            'MacBook Air M3': 120000,
            'Dell XPS 13': 95000,
            'Sony WH-1000XM5': 25000,
            'Casual Cotton T-Shirt': 1200,
            'Denim Jeans Classic': 3500,
            'Winter Wool Sweater': 4500,
            'Running Sneakers': 6000,
            'Leather Jacket': 12000,
            'Python Programming Guide': 800,
            'Machine Learning Basics': 1000,
            'Web Development Handbook': 900,
            'Data Science Cookbook': 1100,
            'Smart Home Speaker': 8000,
            'Garden Tool Set': 3000,
            'LED Desk Lamp': 2500,
            'Yoga Mat Premium': 2500,
            'Dumbbell Set': 8000,
            'Fitness Tracker': 6000,
        }
        
        updated_count = 0
        for product_name, new_price in price_updates.items():
            try:
                product = Product.objects.get(name=product_name)
                product.price = new_price
                product.save()
                self.stdout.write(f'Updated {product_name}: ₹{new_price:,}')
                updated_count += 1
            except Product.DoesNotExist:
                self.stdout.write(f'Product not found: {product_name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} products!')
        )

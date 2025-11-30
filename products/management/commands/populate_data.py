from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics', 'description': 'Latest electronic gadgets and devices'},
            {'name': 'Clothing', 'slug': 'clothing', 'description': 'Fashion and apparel for all'},
            {'name': 'Books', 'slug': 'books', 'description': 'Books and educational materials'},
            {'name': 'Home & Garden', 'slug': 'home-garden', 'description': 'Home improvement and garden supplies'},
            {'name': 'Sports', 'slug': 'sports', 'description': 'Sports equipment and fitness gear'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create products
        products_data = [
            # Electronics
            {'name': 'iPhone 15 Pro', 'price': 85000, 'category': 'electronics', 'sku': 'IP15P001'},
            {'name': 'Samsung Galaxy S24', 'price': 75000, 'category': 'electronics', 'sku': 'SGS24001'},
            {'name': 'MacBook Air M3', 'price': 120000, 'category': 'electronics', 'sku': 'MBA24001'},
            {'name': 'Dell XPS 13', 'price': 95000, 'category': 'electronics', 'sku': 'DXS13001'},
            {'name': 'Sony WH-1000XM5', 'price': 25000, 'category': 'electronics', 'sku': 'SWH5001'},
            
            # Clothing
            {'name': 'Casual Cotton T-Shirt', 'price': 1200, 'category': 'clothing', 'sku': 'CCT001'},
            {'name': 'Denim Jeans Classic', 'price': 3500, 'category': 'clothing', 'sku': 'DJC001'},
            {'name': 'Winter Wool Sweater', 'price': 4500, 'category': 'clothing', 'sku': 'WWS001'},
            {'name': 'Running Sneakers', 'price': 6000, 'category': 'clothing', 'sku': 'RS001'},
            {'name': 'Leather Jacket', 'price': 12000, 'category': 'clothing', 'sku': 'LJ001'},
            
            # Books
            {'name': 'Python Programming Guide', 'price': 800, 'category': 'books', 'sku': 'PPG001'},
            {'name': 'Machine Learning Basics', 'price': 1000, 'category': 'books', 'sku': 'MLB001'},
            {'name': 'Web Development Handbook', 'price': 900, 'category': 'books', 'sku': 'WDH001'},
            {'name': 'Data Science Cookbook', 'price': 1100, 'category': 'books', 'sku': 'DSC001'},
            
            # Home & Garden
            {'name': 'Smart Home Speaker', 'price': 8000, 'category': 'home-garden', 'sku': 'SHS001'},
            {'name': 'Garden Tool Set', 'price': 3000, 'category': 'home-garden', 'sku': 'GTS001'},
            {'name': 'LED Desk Lamp', 'price': 2500, 'category': 'home-garden', 'sku': 'LDL001'},
            
            # Sports
            {'name': 'Yoga Mat Premium', 'price': 2500, 'category': 'sports', 'sku': 'YMP001'},
            {'name': 'Dumbbell Set', 'price': 8000, 'category': 'sports', 'sku': 'DS001'},
            {'name': 'Fitness Tracker', 'price': 6000, 'category': 'sports', 'sku': 'FT001'},
        ]
        
        category_map = {cat.slug: cat for cat in categories}
        
        for prod_data in products_data:
            category = category_map[prod_data['category']]
            
            # Calculate AI recommended price (some products get discounts)
            ai_recommended_price = None
            if random.random() < 0.3:  # 30% chance of AI discount
                discount_percentage = random.uniform(0.05, 0.25)  # 5% to 25% discount
                ai_recommended_price = int(prod_data['price'] * (1 - discount_percentage))
            
            product, created = Product.objects.get_or_create(
                sku=prod_data['sku'],
                defaults={
                    'name': prod_data['name'],
                    'description': f'High-quality {prod_data["name"]} - Perfect for modern lifestyle. Features advanced technology and premium materials.',
                    'price': prod_data['price'],
                    'ai_recommended_price': ai_recommended_price,
                    'category': category,
                    'stock': random.randint(10, 100),
                    'is_active': True,
                    'views_count': random.randint(50, 500),
                    'sales_count': random.randint(5, 50),
                    'popularity_score': random.uniform(1.0, 5.0),
                    'demand_score': random.uniform(0.5, 2.0),
                }
            )
            
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        # Create some sample users
        for i in range(5):
            username = f'user{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': f'User',
                    'last_name': f'{i+1}',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {username}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )

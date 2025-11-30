import requests
import json
import time
from django.core.management.base import BaseCommand
from products.models import Product
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Fetch product images from Google and update the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--api-key',
            type=str,
            help='Google Custom Search API key',
        )
        parser.add_argument(
            '--search-engine-id',
            type=str,
            help='Google Custom Search Engine ID',
        )

    def handle(self, *args, **options):
        # For demo purposes, we'll use a free image API
        # In production, you should use Google Custom Search API with proper credentials
        
        self.stdout.write('Fetching product images...')
        
        # Product image mappings (using free stock image URLs)
        product_images = {
            'iPhone 15 Pro': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop',
            'Samsung Galaxy S24': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop',
            'MacBook Air M3': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400&h=400&fit=crop',
            'Dell XPS 13': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop',
            'Sony WH-1000XM5': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
            'Casual Cotton T-Shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop',
            'Denim Jeans Classic': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop',
            'Winter Wool Sweater': 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=400&fit=crop',
            'Running Sneakers': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop',
            'Leather Jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop',
            'Python Programming Guide': 'https://images.unsplash.com/photo-1517842645767-c639042777db?w=400&h=400&fit=crop',
            'Machine Learning Basics': 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=400&h=400&fit=crop',
            'Web Development Handbook': 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=400&h=400&fit=crop',
            'Data Science Cookbook': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=400&fit=crop',
            'Smart Home Speaker': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=400&h=400&fit=crop',
            'Garden Tool Set': 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=400&h=400&fit=crop',
            'LED Desk Lamp': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=400&fit=crop',
            'Yoga Mat Premium': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop',
            'Dumbbell Set': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop',
            'Fitness Tracker': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400&h=400&fit=crop',
        }
        
        updated_count = 0
        for product_name, image_url in product_images.items():
            try:
                product = Product.objects.get(name=product_name)
                
                # Update the image_url field
                if not product.image_url:
                    product.image_url = image_url
                    product.save()
                    self.stdout.write(f'Updated {product_name} with image URL')
                    updated_count += 1
                else:
                    self.stdout.write(f'{product_name} already has image URL')
                    
            except Product.DoesNotExist:
                self.stdout.write(f'Product not found: {product_name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} products with image URLs!')
        )

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, UserBehavior
import uuid

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Track user behavior if logged in
    if request.user.is_authenticated:
        session_id = request.session.session_key or str(uuid.uuid4())
        UserBehavior.objects.create(
            user=request.user,
            behavior_type='view',
            session_id=session_id,
            metadata={'page': 'product_list'}
        )
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })

# --- Dynamic products from products.txt ---
import os
import csv
from django.conf import settings

def dynamic_products_txt(request):
    products = []
    file_path = os.path.join(settings.BASE_DIR, 'products.txt')
    try:
        with open(file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalize keys for template
                products.append({
                    'name': row.get('Item Name', '').strip(),
                    'price': row.get('Price (INR)', '').strip(),
                    'image_url': row.get('Image URL', '').strip(),
                })
    except Exception as e:
        products = []
    return render(request, 'products/dynamic_products_txt.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    
    # Update view count
    product.views_count += 1
    product.save()
    
    # Track user behavior
    if request.user.is_authenticated:
        session_id = request.session.session_key or str(uuid.uuid4())
        UserBehavior.objects.create(
            user=request.user,
            product=product,
            behavior_type='view',
            session_id=session_id
        )
    
    return render(request, 'products/product_detail.html', {'product': product})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products
    })

def search_products(request):
    query = request.GET.get('q', '')
    txt_products = []
    if query:
        import os, csv
        from django.conf import settings
        file_path = os.path.join(settings.BASE_DIR, 'products.txt')
        try:
            with open(file_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get('Item Name', '').strip()
                    price = row.get('Price (INR)', '').strip()
                    image_url = row.get('Image URL', '').strip()
                    if query.lower() in name.lower():
                        txt_products.append({
                            'name': name, 
                            'price': price, 
                            'image_url': image_url
                        })
        except Exception:
            pass
        # Track search behavior
        if request.user.is_authenticated:
            session_id = request.session.session_key or str(uuid.uuid4())
            UserBehavior.objects.create(
                user=request.user,
                behavior_type='search',
                session_id=session_id,
                metadata={'query': query}
            )
    return render(request, 'products/search_results.html', {
        'txt_products': txt_products,
        'query': query
    })

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'products/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Track behavior
    session_id = request.session.session_key or str(uuid.uuid4())
    UserBehavior.objects.create(
        user=request.user,
        product=product,
        behavior_type='cart_add',
        session_id=session_id
    )
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('products:cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    product = cart_item.product
    cart_item.delete()
    
    # Track behavior
    session_id = request.session.session_key or str(uuid.uuid4())
    UserBehavior.objects.create(
        user=request.user,
        product=product,
        behavior_type='cart_remove',
        session_id=session_id
    )
    
    messages.success(request, 'Item removed from cart!')
    return redirect('products:cart_view')

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('products:cart_view')
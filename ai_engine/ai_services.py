import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from .models import ProductRecommendation, PricingModel, CustomerSegment, MLModel
from products.models import Product, UserBehavior
from accounts.models import UserProfile
from orders.models import Order, OrderItem
import pickle

class RecommendationEngine:
    """AI-powered product recommendation system"""
    
    def __init__(self):
        self.model = None
        self.user_item_matrix = None
    
    def prepare_data(self):
        """Prepare data for collaborative filtering"""
        # Get user behavior data
        behaviors = UserBehavior.objects.filter(behavior_type__in=['view', 'purchase'])
        
        if not behaviors.exists():
            return None
            
        # Create user-item interaction matrix
        data = []
        for behavior in behaviors:
            if behavior.product:
                score = 3 if behavior.behavior_type == 'purchase' else 1
                data.append({
                    'user_id': behavior.user.id,
                    'product_id': behavior.product.id,
                    'score': score
                })
        
        if not data:
            return None
            
        df = pd.DataFrame(data)
        user_item_matrix = df.pivot_table(
            index='user_id', 
            columns='product_id', 
            values='score', 
            fill_value=0
        )
        
        return user_item_matrix
    
    def train_model(self):
        """Train the recommendation model"""
        try:
            self.user_item_matrix = self.prepare_data()
            
            if self.user_item_matrix is None:
                return {'success': False, 'message': 'Insufficient data for training'}
            
            # Calculate cosine similarity between users
            user_similarity = cosine_similarity(self.user_item_matrix)
            
            # Save the model
            model_data = {
                'user_item_matrix': self.user_item_matrix,
                'user_similarity': user_similarity
            }
            
            ml_model = MLModel.objects.create(
                name='Collaborative Filtering',
                model_type='recommendation',
                version='1.0',
                is_active=True
            )
            ml_model.save_model(model_data)
            
            return {'success': True, 'message': 'Recommendation model trained successfully'}
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_recommendations(self, user_id, num_recommendations=10):
        """Get product recommendations for a user"""
        try:
            # Load the active model
            ml_model = MLModel.objects.filter(
                model_type='recommendation', 
                is_active=True
            ).first()
            
            if not ml_model:
                return []
            
            model_data = ml_model.load_model()
            user_item_matrix = model_data['user_item_matrix']
            user_similarity = model_data['user_similarity']
            
            if user_id not in user_item_matrix.index:
                # Cold start problem - return popular products
                popular_products = Product.objects.order_by('-popularity_score')[:num_recommendations]
                return [{'product': p, 'score': p.popularity_score} for p in popular_products]
            
            # Find similar users
            user_idx = list(user_item_matrix.index).index(user_id)
            similar_users = user_similarity[user_idx]
            
            # Get product scores
            product_scores = {}
            for product_id in user_item_matrix.columns:
                score = 0
                total_similarity = 0
                
                for i, similarity in enumerate(similar_users):
                    if similarity > 0 and user_item_matrix.iloc[i, list(user_item_matrix.columns).index(product_id)] > 0:
                        score += similarity * user_item_matrix.iloc[i, list(user_item_matrix.columns).index(product_id)]
                        total_similarity += similarity
                
                if total_similarity > 0:
                    product_scores[product_id] = score / total_similarity
            
            # Sort and get top recommendations
            sorted_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for product_id, score in sorted_products[:num_recommendations]:
                try:
                    product = Product.objects.get(id=product_id)
                    recommendations.append({'product': product, 'score': score})
                except Product.DoesNotExist:
                    continue
            
            return recommendations
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []

class PricingEngine:
    """AI-powered dynamic pricing system"""
    
    def __init__(self):
        self.model = None
    
    def prepare_data(self):
        """Prepare data for pricing model"""
        products = Product.objects.all()
        
        data = []
        for product in products:
            data.append({
                'product_id': product.id,
                'views_count': product.views_count,
                'sales_count': product.sales_count,
                'rating_average': product.rating_average,
                'stock': product.stock,
                'demand_score': product.demand_score,
                'popularity_score': product.popularity_score,
                'current_price': float(product.price)
            })
        
        return pd.DataFrame(data)
    
    def train_model(self):
        """Train the pricing model"""
        try:
            df = self.prepare_data()
            
            if len(df) < 10:
                return {'success': False, 'message': 'Insufficient data for training'}
            
            # Features for price prediction
            features = ['views_count', 'sales_count', 'rating_average', 'stock', 
                       'demand_score', 'popularity_score']
            X = df[features]
            y = df['current_price']
            
            # Train Random Forest model
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Calculate accuracy
            accuracy = model.score(X_test, y_test)
            
            # Save the model
            ml_model = MLModel.objects.create(
                name='Dynamic Pricing RF',
                model_type='pricing',
                version='1.0',
                accuracy=accuracy,
                is_active=True
            )
            ml_model.save_model(model)
            
            return {
                'success': True, 
                'message': f'Pricing model trained successfully with accuracy: {accuracy:.2f}'
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def update_all_prices(self):
        """Update prices for all products using AI predictions"""
        try:
            # Load the active model
            ml_model = MLModel.objects.filter(
                model_type='pricing', 
                is_active=True
            ).first()
            
            if not ml_model:
                return 0
            
            model = ml_model.load_model()
            
            # Get all products
            products = Product.objects.all()
            updated_count = 0
            
            for product in products:
                features = [[
                    product.views_count,
                    product.sales_count,
                    product.rating_average,
                    product.stock,
                    product.demand_score,
                    product.popularity_score
                ]]
                
                predicted_price = model.predict(features)[0]
                
                # Update AI recommended price
                product.ai_recommended_price = max(predicted_price, float(product.price) * 0.7)  # Don't go below 70% of original
                product.save()
                updated_count += 1
            
            return updated_count
            
        except Exception as e:
            print(f"Error updating prices: {e}")
            return 0

class SegmentationEngine:
    """AI-powered customer segmentation"""
    
    def __init__(self):
        self.model = None
    
    def prepare_data(self):
        """Prepare customer data for segmentation"""
        profiles = UserProfile.objects.all()
        
        data = []
        for profile in profiles:
            data.append({
                'user_id': profile.user.id,
                'total_orders': profile.total_orders,
                'total_spent': float(profile.total_spent),
                'average_order_value': float(profile.average_order_value),
                'days_since_registration': (profile.created_at.date() - profile.created_at.date()).days or 1,
            })
        
        return pd.DataFrame(data)
    
    def train_model(self):
        """Train customer segmentation model"""
        try:
            df = self.prepare_data()
            
            if len(df) < 5:
                return {'success': False, 'message': 'Insufficient customer data for segmentation'}
            
            # Features for clustering
            features = ['total_orders', 'total_spent', 'average_order_value']
            X = df[features]
            
            # Normalize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # K-means clustering
            n_clusters = min(4, len(df))  # Max 4 segments
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(X_scaled)
            
            # Update user profiles with segments
            segment_names = ['High Value', 'Regular', 'New Customer', 'At Risk']
            
            for i, (_, row) in enumerate(df.iterrows()):
                try:
                    profile = UserProfile.objects.get(user_id=row['user_id'])
                    profile.customer_segment = segment_names[cluster_labels[i] % len(segment_names)]
                    profile.save()
                except UserProfile.DoesNotExist:
                    continue
            
            # Save model
            model_data = {
                'kmeans': kmeans,
                'scaler': scaler,
                'segment_names': segment_names
            }
            
            ml_model = MLModel.objects.create(
                name='Customer Segmentation',
                model_type='segmentation',
                version='1.0',
                is_active=True
            )
            ml_model.save_model(model_data)
            
            return {
                'success': True,
                'message': f'Customer segmentation completed with {n_clusters} segments'
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}



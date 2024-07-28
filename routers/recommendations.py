from typing import List

import pandas as pd
import torch
from fastapi import APIRouter
from sklearn.preprocessing import StandardScaler

from recommender import BookRecommender

recommendation_router = router = APIRouter()

# Load the trained model
model = BookRecommender()
model.load_state_dict(torch.load('book_recommender_model.pth'))
model.eval()

# Define the recommendation endpoint
@router.get("/recommendations", response_model=List[dict])
async def get_recommendations(book_title: str, num_recommendations: int = 5):
    # Load and process data
    books_df = pd.read_csv('books.csv', on_bad_lines='warn')
    books_df['num_pages'] = books_df['num_pages'].fillna(0)
    features = books_df[['average_rating', 'num_pages']].values
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Prepare features for prediction
    book_features = features_scaled
    book_features_tensor = torch.tensor(book_features, dtype=torch.float32)
    
    # Predict ratings
    model.eval()
    with torch.no_grad():
        predictions = model(book_features_tensor).numpy()
    
    # Find the book index
    book_idx = books_df[books_df['title'].str.contains(book_title, case=False)].index[0]
    book_rating = predictions[book_idx]
    
    distances = []
    for idx, rating in enumerate(predictions):
        distance = abs(book_rating - rating)
        distances.append((distance, idx))
    
    distances.sort()
    recommended_indices = [idx for _, idx in distances[:num_recommendations]]
    recommendations = books_df.iloc[recommended_indices]
    
    return recommendations[['title', 'authors', 'average_rating', 'num_pages']].to_dict(orient='records')

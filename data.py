from astrapy import DataAPIClient
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timedelta
import json

load_dotenv()

def create_mock_data():
    # Generate random engagement data
    post_types = ['carousel', 'reel', 'static']
    posts = []
    
    # Generate 50 mock posts over the last 30 days
    for _ in range(50):
        post_type = random.choice(post_types)
        
        # Adjust engagement ranges based on post type
        if post_type == 'carousel':
            likes = random.randint(500, 2000)
            shares = random.randint(50, 200)
            comments = random.randint(30, 150)
        elif post_type == 'reel':
            likes = random.randint(1000, 3000)
            shares = random.randint(100, 300)
            comments = random.randint(50, 200)
        else: 
            likes = random.randint(300, 1500)
            shares = random.randint(30, 150)
            comments = random.randint(20, 100)
        
        post_date = datetime.now() - timedelta(days=random.randint(0, 30))
        
        posts.append({
            "post_id": str(random.randint(10000, 99999)),
            "post_type": post_type,
            "likes": likes,
            "shares": shares,
            "comments": comments,
            "timestamp": post_date.isoformat(),
            "engagement_rate": round((likes + shares * 2 + comments * 3) / 1000, 2)
        })
    
    return posts

def store_data_in_astra():
    client = DataAPIClient(os.getenv("ASTRA_TOKEN"))
    db = client.get_database_by_api_endpoint(
        "https://af83915c-c251-4610-bef2-28af68c893bc-us-east1.apps.astra.datastax.com",
        keyspace="social_media_analytics",
    )

    collection_name = "social_media_posts"
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
    
    collection = db[collection_name]
    
    posts = create_mock_data()
    for post in posts:
        collection.insert_one(post)
    
    print(f"Stored {len(posts)} mock posts in Astra DB")

if __name__ == "__main__":
    store_data_in_astra()

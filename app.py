import os

#import psycopg2
#from db_setup import get_connection
#from fastapi import FastAPI, HTTPException

#app = FastAPI()

"""
ADD ENDPOINTS FOR FASTAPI HERE
Make sure to do the following:
- Use the correct HTTP method (e.g get, post, put, delete)
- Use correct STATUS CODES, e.g 200, 400, 401 etc. when returning a result to the user
- Use pydantic models whenever you receive user data and need to validate the structure and data types (VG)
This means you need some error handling that determine what should be returned to the user
Read more: https://www.geeksforgeeks.org/10-most-common-http-status-codes/
- Use correct URL paths the resource, e.g some endpoints should be located at the exact same URL, 
but will have different HTTP-verbs.
"""


# INSPIRATION FOR A LIST-ENDPOINT - Not necessary to use pydantic models, but we could to ascertain that we return the correct values
# @app.get("/items/")
# def read_items():
#     con = get_connection()
#     items = get_items(con)
#     return {"items": items}


# INSPIRATION FOR A POST-ENDPOINT, uses a pydantic model to validate
# @app.post("/validation_items/")
# def create_item_validation(item: ItemCreate):
#     con = get_connection()
#     item_id = add_item_validation(con, item)
#     return {"item_id": item_id}


# IMPLEMENT THE ACTUAL ENDPOINTS! Feel free to remove

from typing import List, Optional
import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException, status, Query, Path, Body
from decimal import Decimal
from datetime import datetime
import db

# Import schemas
try:
    from schemas import (
        UserCreate, UserResponse,
        AgencyCreate, AgencyResponse,
        HouseListingCreate, HouseListingResponse,
        BidCreate, BidResponse,
        FavoriteCreate, FavoriteResponse,
        ImageCreate, ImageResponse,
        ReviewCreate, ReviewResponse,
        ViewingCreate, ViewingResponse,
        CategoryCreate, CategoryResponse,
        AgentCreate, AgentResponse
    )
except ImportError:
    # Fallback if schemas not available
    pass

app = FastAPI(
    title="Hemnet Clone API",
    description="A simplified API for a real estate platform similar to Hemnet.se",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ========== HEALTH CHECK ==========
@app.get("/", tags=["Health"])
def root():
    return {"message": "Hemnet Clone API is running", "status": "healthy"}

@app.get("/health", tags=["Health"])
def health_check():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# ========== USER ENDPOINTS ==========
@app.get("/users", tags=["Users"])
def get_all_users(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    conn = get_connection()
    users = db.get_users(conn, limit, offset)
    return {"users": users, "count": len(users)}

@app.get("/users/{user_id}", tags=["Users"])
def get_user_by_id(user_id: int = Path(..., gt=0)):
    conn = get_connection()
    user = db.get_user(conn, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user_data: dict):
    conn = get_connection()
    try:
        # Validate required fields
        required_fields = ['email', 'password_hash', 'first_name', 'last_name', 'user_type', 'role']
        for field in required_fields:
            if field not in user_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        user_id = db.create_user(
            conn,
            email=user_data['email'],
            password_hash=user_data['password_hash'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone=user_data.get('phone'),
            user_type=user_data['user_type'],
            role=user_data['role']
        )
        if not user_id:
            raise HTTPException(status_code=400, detail="Failed to create user")
        
        return {"user_id": user_id, "message": "User created successfully"}
    
    except psycopg2.IntegrityError as e:
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=400, detail="Email already exists")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") 
    
@app.put("/users/{user_id}", tags=["Users"])
def update_user(user_id: int = Path(..., gt=0), user_data: dict = Body(...)):
    conn = get_connection()
    
    # Check if user exists
    existing_user = db.get_user(conn, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove fields that shouldn't be updated
    protected_fields = ['user_id', 'created_at', 'updated_at']
    for field in protected_fields:
        user_data.pop(field, None)
    
    if not user_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    try:
        updated = db.update_user(conn, user_id, **user_data)
        if updated:
            return {"message": "User updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update user")
    except psycopg2.IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(user_id: int = Path(..., gt=0)):
    conn = get_connection()
    deleted = db.delete_user(conn, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None

# ========== LISTING ENDPOINTS ==========
@app.get("/listings", tags=["Listings"])
def get_all_listings(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    city: Optional[str] = Query(None),
    min_price: Optional[Decimal] = Query(None, gt=0),
    max_price: Optional[Decimal] = Query(None, gt=0),
    category_id: Optional[int] = Query(None, gt=0)
):
    conn = get_connection()
    listings = db.get_listings(
        conn, limit, offset, 
        city=city, 
        min_price=min_price, 
        max_price=max_price,
        category_id=category_id
    )
    return {"listings": listings, "count": len(listings)}

@app.get("/listings/{listing_id}", tags=["Listings"])
def get_listing_by_id(listing_id: int = Path(..., gt=0)):
    conn = get_connection()
    listing = db.get_listing(conn, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Get images for this listing
    images = db.get_listing_images(conn, listing_id)
    listing['images'] = images
    
    return listing

@app.post("/listings", status_code=status.HTTP_201_CREATED, tags=["Listings"])
def create_listing(listing_data: dict):
    conn = get_connection()
    
    # Validate required fields
    required_fields = ['agent_id', 'category_id', 'user_id', 'title', 'description',
                      'price', 'address', 'city', 'postal_code']
    for field in required_fields:
        if field not in listing_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    try:
        listing_id = db.create_listing(conn, **listing_data)
        if not listing_id:
            raise HTTPException(status_code=400, detail="Failed to create listing")
        
        return {"listing_id": listing_id, "message": "Listing created successfully"}
    
    except psycopg2.IntegrityError as e:
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=400, detail="Invalid agent_id, category_id, or user_id")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.put("/listings/{listing_id}", tags=["Listings"])
def update_listing(listing_id: int = Path(..., gt=0), listing_data: dict = Body(...)):
    conn = get_connection()
    
    # Check if listing exists
    existing_listing = db.get_listing(conn, listing_id)
    if not existing_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Remove protected fields
    protected_fields = ['listing_id', 'created_at', 'updated_at', 'published_at', 'sold_at']
    for field in protected_fields:
        listing_data.pop(field, None)
    
    if not listing_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    try:
        updated = db.update_listing(conn, listing_id, **listing_data)
        if updated:
            return {"message": "Listing updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update listing")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/listings/{listing_id}/status", tags=["Listings"])
def update_listing_status(
    listing_id: int = Path(..., gt=0),
    status: str = Query(..., description="New status: active, sold, pending")
):
    conn = get_connection()
    
    if status == "sold":
        updated = db.update_listing(conn, listing_id, status=status, sold_at="NOW()")
    else:
        updated = db.update_listing(conn, listing_id, status=status)
    
    if not updated:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    return {"message": f"Listing status updated to {status}"}

@app.patch("/listings/{listing_id}/price", tags=["Listings"])
def update_listing_price(
    listing_id: int = Path(..., gt=0),
    new_price: Decimal = Query(..., gt=0)
):
    conn = get_connection()
    updated = db.update_listing(conn, listing_id, price=new_price)
    if not updated:
        raise HTTPException(status_code=404, detail="Listing not found")
    return {"message": "Price updated successfully", "new_price": new_price}

@app.delete("/listings/{listing_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Listings"])
def delete_listing(listing_id: int = Path(..., gt=0)):
    conn = get_connection()
    deleted = db.delete_listing(conn, listing_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Listing not found")
    return None

# ========== BID ENDPOINTS ==========
@app.get("/bids", tags=["Bids"])
def get_all_bids(listing_id: Optional[int] = Query(None, gt=0)):
    conn = get_connection()
    bids = db.get_bids(conn, listing_id)
    return {"bids": bids, "count": len(bids)}

@app.post("/bids", status_code=status.HTTP_201_CREATED, tags=["Bids"])
def create_bid(bid_data: dict):
    conn = get_connection()
    
    required_fields = ['listing_id', 'user_id', 'amount']
    for field in required_fields:
        if field not in bid_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    try:
        bid_id = db.create_bid(
            conn,
            listing_id=bid_data['listing_id'],
            user_id=bid_data['user_id'],
            amount=bid_data['amount'],
            comment=bid_data.get('comment')
        )
        
        if not bid_id:
            raise HTTPException(status_code=400, detail="Failed to create bid")
        
        return {"bid_id": bid_id, "message": "Bid placed successfully"}
    
    except psycopg2.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Invalid listing_id or user_id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/bids/{bid_id}/status", tags=["Bids"])
def update_bid_status(
    bid_id: int = Path(..., gt=0),
    status: str = Query(..., description="New status: pending, accepted, rejected")
):
    conn = get_connection()
    updated = db.update_bid_status(conn, bid_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Bid not found")
    return {"message": f"Bid status updated to {status}"}

# ========== FAVORITE ENDPOINTS ==========
@app.get("/users/{user_id}/favorites", tags=["Favorites"])
def get_user_favorites(user_id: int = Path(..., gt=0)):
    conn = get_connection()
    favorites = db.get_favorites(conn, user_id)
    return {"favorites": favorites, "count": len(favorites)}

@app.post("/favorites", status_code=status.HTTP_201_CREATED, tags=["Favorites"])
def add_to_favorites(favorite_data: dict):
    conn = get_connection()
    
    required_fields = ['user_id', 'listing_id']
    for field in required_fields:
        if field not in favorite_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    favorite_id = db.add_favorite(
        conn,
        user_id=favorite_data['user_id'],
        listing_id=favorite_data['listing_id']
    )
    
    if favorite_id:
        return {"favorite_id": favorite_id, "message": "Added to favorites"}
    else:
        return {"message": "Already in favorites"}

@app.delete("/favorites", status_code=status.HTTP_204_NO_CONTENT, tags=["Favorites"])
def remove_from_favorites(
    user_id: int = Query(..., gt=0),
    listing_id: int = Query(..., gt=0)
):
    conn = get_connection()
    removed = db.remove_favorite(conn, user_id, listing_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return None

# ========== AGENCY ENDPOINTS ==========
@app.get("/agencies", tags=["Agencies"])
def get_all_agencies(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    conn = get_connection()
    agencies = db.get_agencies(conn, limit, offset)
    return {"agencies": agencies, "count": len(agencies)}

@app.get("/agencies/{agency_id}", tags=["Agencies"])
def get_agency_by_id(agency_id: int = Path(..., gt=0)):
    conn = get_connection()
    agency = db.get_agency(conn, agency_id)
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    return agency

@app.post("/agencies", status_code=status.HTTP_201_CREATED, tags=["Agencies"])
def create_agency(agency_data: dict):
    conn = get_connection()
    
    required_fields = ['name', 'license_number']
    for field in required_fields:
        if field not in agency_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    try:
        agency_id = db.create_agency(conn, **agency_data)
        if not agency_id:
            raise HTTPException(status_code=400, detail="Failed to create agency")
        
        return {"agency_id": agency_id, "message": "Agency created successfully"}
    
    except psycopg2.IntegrityError as e:
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=400, detail="License number already exists")
        raise HTTPException(status_code=400, detail=str(e))

# ========== IMAGE ENDPOINTS ==========
@app.get("/listings/{listing_id}/images", tags=["Images"])
def get_listing_images(listing_id: int = Path(..., gt=0)):
    conn = get_connection()
    images = db.get_listing_images(conn, listing_id)
    return {"images": images, "count": len(images)}

@app.post("/images", status_code=status.HTTP_201_CREATED, tags=["Images"])
def add_image(image_data: dict):
    conn = get_connection()
    
    required_fields = ['listing_id', 'image_url']
    for field in required_fields:
        if field not in image_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    try:
        image_id = db.add_image(
            conn,
            listing_id=image_data['listing_id'],
            image_url=image_data['image_url'],
            display_order=image_data.get('display_order'),
            is_primary=image_data.get('is_primary', False),
            caption=image_data.get('caption')
        )
        
        if not image_id:
            raise HTTPException(status_code=400, detail="Failed to add image")
        
        return {"image_id": image_id, "message": "Image added successfully"}
    
    except psycopg2.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Invalid listing_id")

# ========== CATEGORY ENDPOINTS ==========
@app.get("/categories", tags=["Categories"])
def get_all_categories():
    conn = get_connection()
    categories = db.get_categories(conn)
    return {"categories": categories, "count": len(categories)}

@app.get("/categories/{category_id}", tags=["Categories"])
def get_category_by_id(category_id: int = Path(..., gt=0)):
    conn = get_connection()
    category = db.get_category(conn, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# ========== VIEWING ENDPOINTS ==========
@app.get("/viewings", tags=["Viewings"])
def get_all_viewings(
    user_id: Optional[int] = Query(None, gt=0),
    listing_id: Optional[int] = Query(None, gt=0)
):
    conn = get_connection()
    viewings = db.get_viewings(conn, user_id=user_id, listing_id=listing_id)
    return {"viewings": viewings, "count": len(viewings)}

@app.post("/viewings", status_code=status.HTTP_201_CREATED, tags=["Viewings"])
def create_viewing(viewing_data: dict):
    conn = get_connection()
    
    required_fields = ['listing_id', 'user_id', 'viewing_date', 'viewing_time']
    for field in required_fields:
        if field not in viewing_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    try:
        viewing_id = db.create_viewing(
            conn,
            listing_id=viewing_data['listing_id'],
            user_id=viewing_data['user_id'],
            viewing_date=viewing_data['viewing_date'],
            viewing_time=viewing_data['viewing_time'],
            status=viewing_data.get('status', 'pending'),
            notes=viewing_data.get('notes')
        )
        
        if not viewing_id:
            raise HTTPException(status_code=400, detail="Failed to create viewing")
        
        return {"viewing_id": viewing_id, "message": "Viewing booked successfully"}
    
    except psycopg2.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Invalid listing_id or user_id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========== AGENT ENDPOINTS ==========
@app.get("/agents", tags=["Agents"])
def get_all_agents(agency_id: Optional[int] = Query(None, gt=0)):
    conn = get_connection()
    agents = db.get_agents(conn, agency_id)
    return {"agents": agents, "count": len(agents)}

# ========== REVIEW ENDPOINTS ==========
@app.get("/reviews", tags=["Reviews"])
def get_all_reviews(agent_id: Optional[int] = Query(None, gt=0)):
    conn = get_connection()
    reviews = db.get_agent_reviews(conn, agent_id)
    return {"reviews": reviews, "count": len(reviews)}

@app.post("/reviews", status_code=status.HTTP_201_CREATED, tags=["Reviews"])
def create_review(review_data: dict):
    conn = get_connection()
    
    required_fields = ['agent_id', 'user_id', 'rating']
    for field in required_fields:
        if field not in review_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    if not 1 <= review_data['rating'] <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    try:
        review_id = db.create_review(
            conn,
            agent_id=review_data['agent_id'],
            user_id=review_data['user_id'],
            rating=review_data['rating'],
            comment=review_data.get('comment'),
            transaction=review_data.get('transaction')
        )
        
        if not review_id:
            raise HTTPException(status_code=400, detail="Failed to create review")
        
        return {"review_id": review_id, "message": "Review submitted successfully"}
    
    except psycopg2.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Invalid agent_id or user_id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
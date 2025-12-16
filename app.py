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
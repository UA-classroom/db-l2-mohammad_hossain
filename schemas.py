# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    user_type: str
    role: str

class UserCreate(UserBase):
    password_hash: str

class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Agency Schemas
class AgencyBase(BaseModel):
    name: str
    license_number: str
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    website: Optional[str] = None

class AgencyCreate(AgencyBase):
    pass

class AgencyResponse(AgencyBase):
    agency_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Agent Schemas
class AgentBase(BaseModel):
    agency_id: int
    user_id: int
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    years_experience: Optional[int] = None

class AgentCreate(AgentBase):
    pass

class AgentResponse(AgentBase):
    agent_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    category_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# House Listing Schemas
class HouseListingBase(BaseModel):
    agent_id: int
    category_id: int
    user_id: int
    title: str = Field(..., max_length=50)
    description: str
    price: Decimal = Field(..., gt=0)
    address: str
    city: str
    postal_code: str
    rooms: Optional[Decimal] = None
    size_sqm: Optional[Decimal] = None
    plot_size_sqm: Optional[Decimal] = None
    year_built: Optional[int] = None
    floor: Optional[int] = None
    balcony: Optional[bool] = False
    monthly_fee: Optional[Decimal] = None
    operating_cost: Optional[Decimal] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    status: str = "active"

class HouseListingCreate(HouseListingBase):
    pass

class HouseListingResponse(HouseListingBase):
    listing_id: int
    published_at: Optional[datetime] = None
    sold_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Image Schemas
class ImageBase(BaseModel):
    listing_id: int
    image_url: str
    display_order: Optional[int] = None
    is_primary: bool = False
    caption: Optional[str] = None

class ImageCreate(ImageBase):
    pass

class ImageResponse(ImageBase):
    image_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Bid Schemas
class BidBase(BaseModel):
    listing_id: int
    user_id: int
    amount: Decimal = Field(..., gt=0)
    status: str = "pending"
    comment: Optional[str] = None

class BidCreate(BidBase):
    pass

class BidResponse(BidBase):
    bid_id: int
    bid_date: datetime
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Favorite Schemas
class FavoriteBase(BaseModel):
    listing_id: int
    user_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    favorite_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Review Schemas
class ReviewBase(BaseModel):
    agent_id: int
    user_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    transaction: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    review_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Viewing Booking Schemas
class ViewingBase(BaseModel):
    listing_id: int
    user_id: int
    viewing_date: str
    viewing_time: datetime
    status: str = "pending"
    notes: Optional[str] = None

class ViewingCreate(ViewingBase):
    pass

class ViewingResponse(ViewingBase):
    viewing_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
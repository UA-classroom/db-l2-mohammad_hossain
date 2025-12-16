
from datetime import datetime
import psycopg2


"""
This file is responsible for making database queries, which your fastapi endpoints/routes can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 

- Try to return results with cursor.fetchall() or cursor.fetchone() when possible
- Make sure you always give the user response if something went right or wrong, sometimes 
you might need to use the RETURNING keyword to garantuee that something went right / wrong
e.g when making DELETE or UPDATE queries
- No need to use a class here
- Try to raise exceptions to make them more reusable and work a lot with returns
- You will need to decide which parameters each function should receive. All functions 
start with a connection parameter.
- Below, a few inspirational functions exist - feel free to completely ignore how they are structured
- E.g, if you decide to use psycopg3, you'd be able to directly use pydantic models with the cursor, these examples are however using psycopg2 and RealDictCursor
"""


### THIS IS JUST AN EXAMPLE OF A FUNCTION FOR INSPIRATION FOR A LIST-OPERATION (FETCHING MANY ENTRIES)
# def get_items(con):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("SELECT * FROM items;")
#             items = cursor.fetchall()
#     return items


### THIS IS JUST INSPIRATION FOR A DETAIL OPERATION (FETCHING ONE ENTRY)
# def get_item(con, item_id):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("""SELECT * FROM items WHERE id = %s""", (item_id,))
#             item = cursor.fetchone()
#             return item


### THIS IS JUST INSPIRATION FOR A CREATE-OPERATION
# def add_item(con, title, description):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 "INSERT INTO items (title, description) VALUES (%s, %s) RETURNING id;",
#                 (title, description),
#             )
#             item_id = cursor.fetchone()["id"]
#     return item_id

from psycopg2.extras import RealDictCursor, DictCursor
from typing import List, Optional, Dict, Any
from decimal import Decimal

# ========== USER OPERATIONS ==========
def get_users(con, limit: int = 100, offset: int = 0) -> List[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM users 
                ORDER BY user_id 
                LIMIT %s OFFSET %s;
            """, (limit, offset))
            return cursor.fetchall()

def get_user(con, user_id: int) -> Optional[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
            return cursor.fetchone()

def create_user(con, email: str, password_hash: str, first_name: str, last_name: str,
                phone: Optional[str], user_type: str, role: str) -> Optional[int]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO users 
                (email, password_hash, first_name, last_name, phone, user_type, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING user_id;
            """, (email, password_hash, first_name, last_name, phone, user_type, role))
            result = cursor.fetchone()
            return result["user_id"] if result else None

def update_user(con, user_id: int, **kwargs) -> bool:
    if not kwargs:
        return False
    
    set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
    values = list(kwargs.values())
    values.append(user_id)
    
    with con:
        with con.cursor() as cursor:
            cursor.execute(f"""
                UPDATE users 
                SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s;
            """, tuple(values))
            return cursor.rowcount > 0

def delete_user(con, user_id: int) -> bool:
    with con:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))
            return cursor.rowcount > 0

# ========== AGENCY OPERATIONS ==========
def get_agencies(con, limit: int = 100, offset: int = 0) -> List[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM realtor_agencies 
                ORDER BY agency_id 
                LIMIT %s OFFSET %s;
            """, (limit, offset))
            return cursor.fetchall()

def get_agency(con, agency_id: int) -> Optional[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM realtor_agencies WHERE agency_id = %s;", (agency_id,))
            return cursor.fetchone()

def create_agency(con, name: str, license_number: str, **kwargs) -> Optional[int]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            columns = ["name", "license_number"]
            values = [name, license_number]
            
            for key, value in kwargs.items():
                if value is not None:
                    columns.append(key)
                    values.append(value)
            
            placeholders = ", ".join(["%s"] * len(columns))
            columns_str = ", ".join(columns)
            
            cursor.execute(f"""
                INSERT INTO realtor_agencies ({columns_str})
                VALUES ({placeholders})
                RETURNING agency_id;
            """, tuple(values))
            result = cursor.fetchone()
            return result["agency_id"] if result else None

# ========== HOUSE LISTING OPERATIONS ==========
def get_listings(con, limit: int = 100, offset: int = 0, 
                 city: Optional[str] = None, min_price: Optional[Decimal] = None,
                 max_price: Optional[Decimal] = None, category_id: Optional[int] = None) -> List[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            query = "SELECT * FROM house_listing WHERE 1=1"
            params = []
            
            if city:
                query += " AND city ILIKE %s"
                params.append(f"%{city}%")
            
            if min_price:
                query += " AND price >= %s"
                params.append(min_price)
            
            if max_price:
                query += " AND price <= %s"
                params.append(max_price)
            
            if category_id:
                query += " AND category_id = %s"
                params.append(category_id)
            
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor.execute(query, tuple(params))
            return cursor.fetchall()

def get_listing(con, listing_id: int) -> Optional[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM house_listing WHERE listing_id = %s;", (listing_id,))
            return cursor.fetchone()

def create_listing(con, agent_id: int, category_id: int, user_id: int,
                   title: str, description: str, price: Decimal,
                   address: str, city: str, postal_code: str, **kwargs) -> Optional[int]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            # Required columns
            columns = ["agent_id", "category_id", "user_id", "title", "description", 
                      "price", "address", "city", "postal_code", "published_at"]
            values = [agent_id, category_id, user_id, title, description, price,
                     address, city, postal_code, "NOW()"]
            
            # Optional columns
            optional_fields = ['rooms', 'size_sqm', 'plot_size_sqm', 'year_built', 
                             'floor', 'balcony', 'monthly_fee', 'operating_cost',
                             'latitude', 'longitude', 'status']
            
            for field in optional_fields:
                if field in kwargs and kwargs[field] is not None:
                    columns.append(field)
                    values.append(kwargs[field])
            
            placeholders = ", ".join(["%s"] * len(columns))
            columns_str = ", ".join(columns)
            
            cursor.execute(f"""
                INSERT INTO house_listing ({columns_str})
                VALUES ({placeholders})
                RETURNING listing_id;
            """, tuple(values))
            result = cursor.fetchone()
            return result["listing_id"] if result else None

def update_listing(con, listing_id: int, **kwargs) -> bool:
    if not kwargs:
        return False
    
    set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
    values = list(kwargs.values())
    values.append(listing_id)
    
    with con:
        with con.cursor() as cursor:
            cursor.execute(f"""
                UPDATE house_listing 
                SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE listing_id = %s;
            """, tuple(values))
            return cursor.rowcount > 0

def delete_listing(con, listing_id: int) -> bool:
    with con:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM house_listing WHERE listing_id = %s;", (listing_id,))
            return cursor.rowcount > 0

# ========== BID OPERATIONS ==========
def get_bids(con, listing_id: Optional[int] = None) -> List[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            if listing_id:
                cursor.execute("""
                    SELECT * FROM bids 
                    WHERE listing_id = %s 
                    ORDER BY amount DESC;
                """, (listing_id,))
            else:
                cursor.execute("SELECT * FROM bids ORDER BY bid_date DESC;")
            return cursor.fetchall()

def create_bid(con, listing_id: int, user_id: int, amount: Decimal, 
               comment: Optional[str] = None) -> Optional[int]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO bids (listing_id, user_id, amount, comment)
                VALUES (%s, %s, %s, %s)
                RETURNING bid_id;
            """, (listing_id, user_id, amount, comment))
            result = cursor.fetchone()
            return result["bid_id"] if result else None

def update_bid_status(con, bid_id: int, status: str) -> bool:
    with con:
        with con.cursor() as cursor:
            cursor.execute("""
                UPDATE bids 
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE bid_id = %s;
            """, (status, bid_id))
            return cursor.rowcount > 0

# ========== FAVORITE OPERATIONS ==========
def get_favorites(con, user_id: int) -> List[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT f.*, h.title, h.price, h.city 
                FROM favorites f
                JOIN house_listing h ON f.listing_id = h.listing_id
                WHERE f.user_id = %s
                ORDER BY f.created_at DESC;
            """, (user_id,))
            return cursor.fetchall()

def add_favorite(con, user_id: int, listing_id: int) -> Optional[int]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO favorites (user_id, listing_id)
                VALUES (%s, %s)
                ON CONFLICT (user_id, listing_id) DO NOTHING
                RETURNING favorite_id;
            """, (user_id, listing_id))
            result = cursor.fetchone()
            return result["favorite_id"] if result else None

def remove_favorite(con, user_id: int, listing_id: int) -> bool:
    with con:
        with con.cursor() as cursor:
            cursor.execute("""
                DELETE FROM favorites 
                WHERE user_id = %s AND listing_id = %s;
            """, (user_id, listing_id))
            return cursor.rowcount > 0

# ========== IMAGE OPERATIONS ==========
def get_listing_images(con, listing_id: int) -> List[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM listing_images 
                WHERE listing_id = %s 
                ORDER BY display_order NULLS LAST;
            """, (listing_id,))
            return cursor.fetchall()

def add_image(con, listing_id: int, image_url: str, 
              display_order: Optional[int] = None,
              is_primary: bool = False,
              caption: Optional[str] = None) -> Optional[int]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO listing_images 
                (listing_id, image_url, display_order, is_primary, caption)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING image_id;
            """, (listing_id, image_url, display_order, is_primary, caption))
            result = cursor.fetchone()
            return result["image_id"] if result else None

# ========== CATEGORY OPERATIONS ==========
def get_categories(con) -> List[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM listing_categories ORDER BY name;")
            return cursor.fetchall()

def get_category(con, category_id: int) -> Optional[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM listing_categories WHERE category_id = %s;", (category_id,))
            return cursor.fetchone()

# ========== VIEWING BOOKING OPERATIONS ==========
def get_viewings(con, user_id: Optional[int] = None, 
                 listing_id: Optional[int] = None) -> List[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            query = "SELECT * FROM viewing_booking WHERE 1=1"
            params = []
            
            if user_id:
                query += " AND user_id = %s"
                params.append(user_id)
            
            if listing_id:
                query += " AND listing_id = %s"
                params.append(listing_id)
            
            query += " ORDER BY viewing_time ASC;"
            cursor.execute(query, tuple(params))
            return cursor.fetchall()

def create_viewing(con, listing_id: int, user_id: int,
                   viewing_date: str, viewing_time: datetime,
                   status: str = "pending", notes: Optional[str] = None) -> Optional[int]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO viewing_booking 
                (listing_id, user_id, viewing_date, viewing_time, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING viewing_id;
            """, (listing_id, user_id, viewing_date, viewing_time, status, notes))
            result = cursor.fetchone()
            return result["viewing_id"] if result else None

# ========== AGENT OPERATIONS ==========
def get_agents(con, agency_id: Optional[int] = None) -> List[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            if agency_id:
                cursor.execute("""
                    SELECT * FROM realtor_agent 
                    WHERE agency_id = %s 
                    ORDER BY agent_id;
                """, (agency_id,))
            else:
                cursor.execute("SELECT * FROM realtor_agent ORDER BY agent_id;")
            return cursor.fetchall()

# ========== REVIEW OPERATIONS ==========
def get_agent_reviews(con, agent_id: Optional[int] = None) -> List[Dict]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            if agent_id:
                cursor.execute("""
                    SELECT * FROM agent_reviews 
                    WHERE agent_id = %s 
                    ORDER BY created_at DESC;
                """, (agent_id,))
            else:
                cursor.execute("SELECT * FROM agent_reviews ORDER BY created_at DESC;")
            return cursor.fetchall()

def create_review(con, agent_id: int, user_id: int, rating: int,
                  comment: Optional[str] = None,
                  transaction: Optional[str] = None) -> Optional[int]:
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO agent_reviews 
                (agent_id, user_id, rating, comment, transaction)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING review_id;
            """, (agent_id, user_id, rating, comment, transaction))
            result = cursor.fetchone()
            return result["review_id"] if result else None

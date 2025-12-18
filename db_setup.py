
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host="localhost",  # change if needed
        port="5432",  # change if needed
    )


def create_tables():
    """
    A function to create the necessary tables for the project.
    """
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            # Add ALL your CREATE TABLE statements here
            # Example for house_listings:
            cursor.execute("""
               CREATE TABLE IF NOT EXISTS  users (
                    user_id SERIAL PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    phone VARCHAR(15),
                    user_type varchar(50) NOT NULL,
                    role VARCHAR(20) NOT NULL CHECK (role IN ('buyer', 'seller', 'admin', 'agent')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );  
     
             """)
            #indexex for users
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);")
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS  realtor_agencies (
                    agency_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    license_number VARCHAR(100) UNIQUE NOT NULL,
                    description TEXT,
                    phone VARCHAR(15),
                    email VARCHAR(100),
                    address VARCHAR(255),
                    city VARCHAR(50),
                    postal_code VARCHAR(50),
                    website VARCHAR(100),
                    created_at TIMESTAMP DEFAULT now()
                  ); 
            """)
            #indexex for realotor_agencies
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_realtor_agencies_city ON realtor_agencies(city);") 


  #3. REALTOR_AGENTS TABLE

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS  realtor_agent (
                    agent_id SERIAL PRIMARY KEY,
                    agency_id INTEGER REFERENCES realtor_agencies(agency_id),
                    user_id INTEGER REFERENCES users(user_id),
                    bio VARCHAR(200),
                    profile_image_url VARCHAR(500),
                    years_experience INTEGER,
                    created_at TIMESTAMP DEFAULT now(),
                    updated_at TIMESTAMP DEFAULT now()
                 );
            """)
            #index for realtor_agent
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_realtor_agent_user ON realtor_agent(user_id);")


#4. LISTING_CATEGORIES TABLE

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS listing_categories (
                    category_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT now()
                 );
            """)
           #Index for listing_categories
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_categories_name ON listing_categories(name);")


 # 5. HOUSE_LISTINGS TABLE
 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS house_listing (
                    listing_id SERIAL PRIMARY KEY,
                    agent_id INTEGER REFERENCES realtor_agent(agent_id),
                    category_id INTEGER REFERENCES listing_categories(category_id),
                    user_id INTEGER REFERENCES users(user_id),
                    title VARCHAR(50) NOT NULL,
                    description TEXT NOT NULL,
                    price DECIMAL NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    city VARCHAR(100) NOT NULL,
                    postal_code VARCHAR(10) NOT NULL,
                    rooms DECIMAL,
                    size_sqm DECIMAL,
                    plot_size_sqm DECIMAL,
                    year_built INTEGER,
                    floor INTEGER,
                    balcony BOOLEAN,
                    monthly_fee DECIMAL,
                    operating_cost DECIMAL,
                    latitude DECIMAL,
                    longitude DECIMAL,
                    status VARCHAR(50) DEFAULT 'active',
                    published_at TIMESTAMP,
                    sold_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT now(),
                    updated_at TIMESTAMP DEFAULT now()
                );
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_listing_city ON house_listing(city);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_listing_price ON house_listing(price);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_listing_category ON house_listing(category_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_listing_status ON house_listing(status);")

#6. LISTING_IMAGES TABLE

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS listing_images (
                    image_id SERIAL PRIMARY KEY,
                    listing_id INTEGER REFERENCES house_listing(listing_id) ON DELETE CASCADE,
                    image_url VARCHAR(500) NOT NULL,
                    display_order INTEGER,
                    is_primary BOOLEAN DEFAULT false,
                    caption VARCHAR(255),
                    created_at TIMESTAMP DEFAULT now()
                );

            """)

            cursor.execute("CREATE INDEX IF NOT EXISTS idx_images_listing ON listing_images(listing_id);")


# 7. BIDS TABLE

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bids (
                    bid_id SERIAL PRIMARY KEY,
                    listing_id INTEGER REFERENCES house_listing(listing_id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(user_id),
                    amount DECIMAL NOT NULL,
                    bid_date TIMESTAMP DEFAULT now(),
                    status VARCHAR(20) NOT NULL,
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT now(),
                    updated_at TIMESTAMP DEFAULT now()
                );

            
            """)

            cursor.execute("CREATE INDEX IF NOT EXISTS idx_bids_listing ON bids(listing_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_bids_user ON bids(user_id);")


#8. FAVORITES TABLE
 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    favorite_id SERIAL PRIMARY KEY,
                    listing_id INTEGER REFERENCES house_listing(listing_id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT now()
                );
             """)

            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_favorites_user_listing ON favorites(user_id, listing_id);")


# 9. AGENT_REVIEWS TABLE

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_reviews (
                    review_id SERIAL PRIMARY KEY,
                    agent_id INTEGER REFERENCES realtor_agent(agent_id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(user_id),
                    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                    comment TEXT,
                    transaction VARCHAR(20),
                    created_at TIMESTAMP DEFAULT now(),
                    updated_at TIMESTAMP DEFAULT now()
                );
            """)

            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_agent ON agent_reviews(agent_id);")


#10. VIEWING_BOOKINGS TABLE

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS viewing_booking (
                    viewing_id SERIAL PRIMARY KEY,
                    listing_id INTEGER REFERENCES house_listing(listing_id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(user_id),
                    viewing_date date NOT NULL,
                    viewing_time TIMESTAMP NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT now(),
                    updated_at TIMESTAMP DEFAULT now()
                );
            """)

            cursor.execute("CREATE INDEX IF NOT EXISTS idx_viewing_listing ON viewing_booking(listing_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_viewing_user ON viewing_booking(user_id);")

            


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")

"""
Multi-tenant migration: Add restaurants table and restaurant_id foreign keys

This script:
1. Creates restaurants table
2. Creates a default restaurant
3. Adds restaurant_id to users, tables, menu_items, orders
4. Associates all existing data with the default restaurant
"""

import psycopg2
import sys
import os
from pathlib import Path

# Add parent directory to path to import settings
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from app.core.config import settings

def migrate():
    # Parse DATABASE_URL
    db_url = settings.DATABASE_URL
    if not db_url.startswith('postgresql://'):
        print("Error: This migration is for PostgreSQL only")
        return False
        
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    try:
        print("Starting multi-tenant migration...")
        
        # 1. Create restaurants table
        print("Creating restaurants table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurants (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_restaurants_id ON restaurants(id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_restaurants_name ON restaurants(name);")
        
        # 2. Create default restaurant
        print("Creating default restaurant...")
        cursor.execute("""
            INSERT INTO restaurants (name, created_at)
            VALUES ('Default Restaurant', NOW())
            ON CONFLICT DO NOTHING
            RETURNING id;
        """)
        result = cursor.fetchone()
        if result:
            default_restaurant_id = result[0]
        else:
            cursor.execute("SELECT id FROM restaurants WHERE name = 'Default Restaurant' LIMIT 1;")
            default_restaurant_id = cursor.fetchone()[0]
        
        print(f"Default restaurant ID: {default_restaurant_id}")
        
        # 3. Add restaurant_id to users table
        print("Adding restaurant_id to users table...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS restaurant_id INTEGER;
        """)
        cursor.execute(f"""
            UPDATE users 
            SET restaurant_id = {default_restaurant_id}
            WHERE restaurant_id IS NULL;
        """)
        cursor.execute("""
            ALTER TABLE users 
            ALTER COLUMN restaurant_id SET NOT NULL;
        """)
        cursor.execute("""
            ALTER TABLE users
            ADD CONSTRAINT users_restaurant_id_fkey 
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            ON UPDATE NO ACTION ON DELETE NO ACTION
            NOT VALID;
        """)
        cursor.execute("ALTER TABLE users VALIDATE CONSTRAINT users_restaurant_id_fkey;")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_users_restaurant_id ON users(restaurant_id);")
        
        # Remove unique constraint on username, make it unique per restaurant
        cursor.execute("""
            ALTER TABLE users DROP CONSTRAINT IF EXISTS users_username_key;
        """)
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS users_username_restaurant_key 
            ON users(username, restaurant_id);
        """)
        
        # 4. Add restaurant_id to tables table
        print("Adding restaurant_id to tables table...")
        cursor.execute("""
            ALTER TABLE tables 
            ADD COLUMN IF NOT EXISTS restaurant_id INTEGER;
        """)
        cursor.execute(f"""
            UPDATE tables 
            SET restaurant_id = {default_restaurant_id}
            WHERE restaurant_id IS NULL;
        """)
        cursor.execute("""
            ALTER TABLE tables 
            ALTER COLUMN restaurant_id SET NOT NULL;
        """)
        cursor.execute("""
            ALTER TABLE tables
            ADD CONSTRAINT tables_restaurant_id_fkey 
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            ON UPDATE NO ACTION ON DELETE NO ACTION
            NOT VALID;
        """)
        cursor.execute("ALTER TABLE tables VALIDATE CONSTRAINT tables_restaurant_id_fkey;")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_tables_restaurant_id ON tables(restaurant_id);")
        
        # Remove unique constraint on table number, make it unique per restaurant
        cursor.execute("""
            DROP INDEX IF EXISTS ix_tables_number;
        """)
        cursor.execute("""
            ALTER TABLE tables DROP CONSTRAINT IF EXISTS tables_number_key;
        """)
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS tables_number_restaurant_key 
            ON tables(number, restaurant_id);
        """)
        
        # 5. Add restaurant_id to menu_items table
        print("Adding restaurant_id to menu_items table...")
        cursor.execute("""
            ALTER TABLE menu_items 
            ADD COLUMN IF NOT EXISTS restaurant_id INTEGER;
        """)
        cursor.execute(f"""
            UPDATE menu_items 
            SET restaurant_id = {default_restaurant_id}
            WHERE restaurant_id IS NULL;
        """)
        cursor.execute("""
            ALTER TABLE menu_items 
            ALTER COLUMN restaurant_id SET NOT NULL;
        """)
        cursor.execute("""
            ALTER TABLE menu_items
            ADD CONSTRAINT menu_items_restaurant_id_fkey 
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            ON UPDATE NO ACTION ON DELETE NO ACTION
            NOT VALID;
        """)
        cursor.execute("ALTER TABLE menu_items VALIDATE CONSTRAINT menu_items_restaurant_id_fkey;")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_menu_items_restaurant_id ON menu_items(restaurant_id);")
        
        # 6. Add restaurant_id to orders table
        print("Adding restaurant_id to orders table...")
        cursor.execute("""
            ALTER TABLE orders 
            ADD COLUMN IF NOT EXISTS restaurant_id INTEGER;
        """)
        cursor.execute(f"""
            UPDATE orders 
            SET restaurant_id = {default_restaurant_id}
            WHERE restaurant_id IS NULL;
        """)
        cursor.execute("""
            ALTER TABLE orders 
            ALTER COLUMN restaurant_id SET NOT NULL;
        """)
        cursor.execute("""
            ALTER TABLE orders
            ADD CONSTRAINT orders_restaurant_id_fkey 
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            ON UPDATE NO ACTION ON DELETE NO ACTION
            NOT VALID;
        """)
        cursor.execute("ALTER TABLE orders VALIDATE CONSTRAINT orders_restaurant_id_fkey;")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_orders_restaurant_id ON orders(restaurant_id);")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        print(f"All existing data has been associated with restaurant: 'Default Restaurant' (ID: {default_restaurant_id})")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)

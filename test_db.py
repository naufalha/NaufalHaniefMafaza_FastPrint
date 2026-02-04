import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def test_database():
    try:
        with connection.cursor() as cursor:
            # Test connection
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"Connected to database: {db_name}")
            
            # Check if tables exist
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            print(f"Tables in database: {tables}")
            
            # Check specific tables
            required_tables = ['kategori', 'status', 'produk']
            for table in required_tables:
                if table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ Table '{table}' exists with {count} records")
                else:
                    print(f"❌ Table '{table}' does not exist")
                    
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database()
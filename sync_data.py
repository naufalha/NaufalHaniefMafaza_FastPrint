import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from products.models import Kategori, Status, Produk
from scripts.fetch_fastprint import fetch_data

def sync_fastprint_data():
    try:
        # Ensure fresh database connection
        connection.ensure_connection()
        
        print("Fetching data from FastPrint API...")
        data = fetch_data()
        
        if data.get('error') == 0:
            products = data.get('data', [])
            print(f"\nProcessing {len(products)} products...")
            
            for product in products:
                # Get or create kategori
                kategori, created = Kategori.objects.get_or_create(
                    nama_kategori=product['kategori']
                )
                if created:
                    print(f"Created new category: {kategori.nama_kategori}")
                
                # Get or create status
                status, created = Status.objects.get_or_create(
                    nama_status=product['status']
                )
                if created:
                    print(f"Created new status: {status.nama_status}")
                
                # Update or create produk
                produk, created = Produk.objects.update_or_create(
                    id_produk=int(product['id_produk']),
                    defaults={
                        'nama_produk': product['nama_produk'],
                        'harga': float(product['harga']),
                        'kategori': kategori,
                        'status': status,
                    }
                )
                action = "Created" if created else "Updated"
                print(f"{action} product: {produk.nama_produk}")
            
            print(f"\n✅ Successfully synced {len(products)} products to database")
        else:
            print(f"❌ API Error: {data.get('ket', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    sync_fastprint_data()
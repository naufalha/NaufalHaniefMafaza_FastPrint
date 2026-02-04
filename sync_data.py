import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Kategori, Status, Produk
from scripts.fetch_fastprint import fetch_data

def sync_fastprint_data():
    try:
        data = fetch_data()
        
        if data.get('error') == 0:
            products = data.get('data', [])
            
            for product in products:
                # Get or create kategori
                kategori, _ = Kategori.objects.get_or_create(
                    nama_kategori=product['kategori']
                )
                
                # Get or create status
                status, _ = Status.objects.get_or_create(
                    nama_status=product['status']
                )
                
                # Update or create produk
                Produk.objects.update_or_create(
                    id_produk=int(product['id_produk']),
                    defaults={
                        'nama_produk': product['nama_produk'],
                        'harga': float(product['harga']),
                        'kategori': kategori,
                        'status': status,
                    }
                )
            
            print(f"✅ Synced {len(products)} products successfully")
        else:
            print(f"❌ API Error: {data.get('ket', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    sync_fastprint_data()
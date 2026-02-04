# FastPrint Product Management System

## Deskripsi Proyek
Aplikasi web Django untuk mengelola data produk FastPrint yang diambil dari API eksternal dan disimpan dalam database MySQL Railway.

## Fitur Utama
- ✅ Fetch data produk dari FastPrint API dengan autentikasi dinamis
- ✅ Penyimpanan data ke database MySQL dengan relasi yang tepat
- ✅ Interface web untuk CRUD operations
- ✅ Filter produk berdasarkan status (bisa dijual/tidak bisa dijual)
- ✅ Form validasi untuk input data
- ✅ Konfirmasi penghapusan data

## Struktur Database

### Tabel `kategori`
| Field | Type | Description |
|-------|------|-------------|
| id_kategori | INT (PK, Auto Increment) | Primary key |
| nama_kategori | VARCHAR(100, Unique) | Nama kategori produk |

### Tabel `status`
| Field | Type | Description |
|-------|------|-------------|
| id_status | INT (PK, Auto Increment) | Primary key |
| nama_status | VARCHAR(50, Unique) | Status produk |

### Tabel `produk`
| Field | Type | Description |
|-------|------|-------------|
| id_produk | INT (PK) | Primary key |
| nama_produk | VARCHAR(255) | Nama produk |
| harga | DECIMAL(10,2) | Harga produk |
| kategori_id | INT (FK) | Foreign key ke tabel kategori |
| status_id | INT (FK) | Foreign key ke tabel status |

## Instalasi dan Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd NaufalHaniefMafazaFastPrint
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Buat file `.env` dengan konfigurasi Railway MySQL:
```env
DB_NAME=railway
DB_USER=root
DB_PASSWORD=your_railway_password
DB_HOST=your_railway_host
DB_PORT=your_railway_port
```

### 5. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Sync Data dari FastPrint API
```bash
python sync_data.py
```

### 7. Jalankan Server
```bash
python manage.py runserver
```

## Struktur Proyek
```
NaufalHaniefMafazaFastPrint/
├── config/                 # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── products/               # Main app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Form validation
│   ├── urls.py            # URL routing
│   └── migrations/        # Database migrations
├── scripts/
│   └── fetch_fastprint.py # API fetching script
├── templates/
│   ├── base.html          # Base template
│   └── products/          # Product templates
├── sync_data.py           # Data synchronization script
├── test_db.py            # Database testing script
├── requirements.txt       # Python dependencies
└── .env                  # Environment variables
```

## API FastPrint

### Autentikasi
API menggunakan autentikasi berbasis waktu server:
- **Username**: `tesprogrammerDDMMYYCHH` (berubah setiap jam)
- **Password**: MD5 hash dari `bisacoding-DD-MM-YY`

### Endpoint
- **URL**: `https://recruitment.fastprint.co.id/tes/api_tes_programmer`
- **Method**: POST
- **Content-Type**: `application/x-www-form-urlencoded`

### Response Format
```json
{
  "error": 0,
  "version": "220523.0.1",
  "data": [
    {
      "no": "7",
      "id_produk": "6",
      "nama_produk": "ALCOHOL GEL POLISH CLEANSER GP-CLN01",
      "kategori": "L QUEENLY",
      "harga": "12500",
      "status": "bisa dijual"
    }
  ]
}
```

## Web Interface

### URL Routes
| URL | View | Description |
|-----|------|-------------|
| `/` | product_list | Daftar produk dengan filter |
| `/add/` | product_add | Form tambah produk |
| `/edit/<id>/` | product_edit | Form edit produk |
| `/delete/<id>/` | product_delete | Konfirmasi hapus produk |

### Fitur Interface
1. **Daftar Produk**
   - Filter berdasarkan status (bisa dijual/tidak bisa dijual)
   - Tabel responsif dengan Bootstrap
   - Tombol aksi (Edit/Hapus)

2. **Form Tambah/Edit**
   - Validasi nama produk (wajib diisi)
   - Validasi harga (harus angka positif)
   - Dropdown kategori dan status

3. **Konfirmasi Hapus**
   - Alert JavaScript untuk konfirmasi
   - Halaman konfirmasi terpisah

## Validasi Form

### Nama Produk
- **Required**: Ya
- **Validasi**: Tidak boleh kosong atau hanya spasi
- **Error**: "Nama produk harus diisi"

### Harga
- **Required**: Ya
- **Type**: Number (decimal)
- **Validasi**: Harus angka positif
- **Error**: "Harga harus berupa angka positif"

## Scripts Utilitas

### sync_data.py
Sinkronisasi data dari FastPrint API ke database:
```bash
python sync_data.py
```

### test_db.py
Testing koneksi database dan struktur tabel:
```bash
python test_db.py
```

## Dependencies
```
Django>=5.2.0
mysqlclient>=2.1.0
python-dotenv>=1.0.0
requests>=2.32.0
```

## Troubleshooting

### Error: Table doesn't exist
```bash
python manage.py makemigrations products
python manage.py migrate
```

### Error: MySQL connection
- Periksa kredensial di file `.env`
- Pastikan Railway MySQL service aktif
- Gunakan host eksternal, bukan `mysql.railway.internal`

### Error: API authentication
- API menggunakan waktu server, bukan waktu lokal
- Username dan password berubah setiap jam
- Script otomatis mengambil format dari response headers

## Best Practices
1. **Database**: Menggunakan foreign key constraints
2. **Security**: Environment variables untuk kredensial
3. **Validation**: Server-side dan client-side validation
4. **UX**: Konfirmasi untuk aksi destructive
5. **Code**: Separation of concerns (models, views, templates)

## Kontributor
- Naufal Hanief Mafaza

## Lisensi
MIT License
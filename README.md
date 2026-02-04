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


### Direktori Struktur
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

### Cara Kerja Autentikasi API
API FastPrint menggunakan sistem autentikasi dinamis berbasis waktu server yang berubah setiap jam.

#### 1. Mendapatkan Username dan Password

**Username Format**: `tesprogrammerDDMMYYCHH`
- `DD`: Tanggal (2 digit dengan zero padding)
- `MM`: Bulan (2 digit dengan zero padding) 
- `YY`: Tahun (2 digit terakhir)
- `C`: Karakter literal 'C'
- `HH`: Jam + 7 (dengan handling overflow 24 jam)

**Password Format**: MD5 hash dari `bisacoding-DD-MM-YY`
- `DD`: Tanggal (2 digit dengan zero padding)
- `MM`: Bulan (2 digit dengan zero padding)
- `YY`: Tahun (2 digit terakhir)

#### 2. Algoritma Fetch API

```python
def fetch_data():
    # Step 1: Dapatkan waktu server dari response headers
    initial_response = session.get(URL)
    expected_username = initial_response.headers.get('X-Credentials-Username', '').split(' ')[0]
    
    # Step 2: Extract komponen tanggal dari username yang diharapkan
    day_str = expected_username[13:15]    # Posisi 13-14
    month_str = expected_username[15:17]  # Posisi 15-16
    year_str = expected_username[17:19]   # Posisi 17-18
    
    # Step 3: Generate credentials
    username = expected_username  # Langsung ambil dari header
    raw_password = f"bisacoding-{day_str}-{month_str}-{year_str}"
    password_md5 = hashlib.md5(raw_password.encode()).hexdigest()
    
    # Step 4: Kirim POST request dengan form data
    response = session.post(URL, data={
        "username": username,
        "password": password_md5
    })
```

#### 3. Contoh Kredensial

**Tanggal Server**: 5 Februari 2026, Jam 10:00 GMT
- **Username**: `tesprogrammer050226C17` 
  - `05`: Tanggal 5
  - `02`: Bulan Februari
  - `26`: Tahun 2026
  - `C17`: Jam 10 + 7 = 17
- **Raw Password**: `bisacoding-05-02-26`
- **MD5 Password**: `4a8b2c3d1e5f6789...` (hasil MD5 hash)

#### 4. Mengapa Menggunakan Server Time
- API menggunakan waktu server, bukan waktu lokal client
- Kredensial berubah setiap jam berdasarkan waktu server
- Script otomatis mengambil username yang benar dari response header `X-Credentials-Username`
- Menghindari masalah timezone dan sinkronisasi waktu

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


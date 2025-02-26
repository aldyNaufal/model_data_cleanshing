# FastAPI Institution Name Cleaner

## Deskripsi
FastAPI Institution Name Cleaner adalah sebuah API berbasis FastAPI yang digunakan untuk membersihkan dan menstandarkan nama institusi pendidikan dengan menggantikan singkatan dengan nama lengkap serta melakukan fuzzy matching dengan nama institusi resmi.

## Fitur
- Mengganti singkatan institusi dengan nama lengkap
- Menstandarkan format nama institusi
- Menggunakan fuzzy matching untuk memperbaiki kesalahan penulisan

## Persyaratan
Sebelum memulai, pastikan Anda telah menginstal:
- Python 3.8 atau versi lebih baru
- pip (Python package manager)

## Instalasi
1. **Clone Repository (Opsional, jika menggunakan repo GitHub)**
   ```sh
   git clone https://github.com/username/repo-name.git
   cd repo-name
   ```

2. **Buat dan Aktifkan Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate  # Untuk Windows
   ```

3. **Install Dependensi**
   ```sh
   pip install -r requirements.txt
   ```
   Jika tidak ada file `requirements.txt`, Anda bisa menginstal paket secara manual:
   ```sh
   pip install fastapi uvicorn pandas openpyxl rapidfuzz
   ```

## Struktur File
```
project-directory/
│── Train_data.csv          # Dataset berisi daftar institusi & singkatannya
│── main.py                 # File utama FastAPI
│── requirements.txt        # Daftar dependensi
│── README.md               # Dokumentasi proyek
```

## Menjalankan Aplikasi
1. Jalankan perintah berikut di terminal:
   ```sh
   uvicorn main:app --reload
   ```
2. API akan berjalan di `http://127.0.0.1:8000`
3. Dokumentasi otomatis FastAPI dapat diakses di:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Cara Menggunakan API
### Endpoint: `/clean/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "name": "ITB (Institut Teknologi Bandung)"
  }
  ```
- **Response:**
  ```json
  {
    "cleaned": "INSTITUT TEKNOLOGI BANDUNG"
  }
  ```

## Deployment (Opsional)
### Menjalankan dengan Docker
1. **Buat Dockerfile** di dalam direktori proyek:
   ```dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY . /app
   RUN pip install --no-cache-dir -r requirements.txt
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
2. **Bangun dan Jalankan Container:**
   ```sh
   docker build -t fastapi-cleaner .
   docker run -p 8000:8000 fastapi-cleaner
   ```

## Lisensi
Proyek ini berada di bawah lisensi MIT. Silakan gunakan dan modifikasi sesuai kebutuhan Anda.

---
Happy coding! 🚀


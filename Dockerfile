# Menggunakan image Python versi terbaru
FROM python:3.9

# Menetapkan direktori kerja di dalam container
WORKDIR /app

# Menyalin semua file ke dalam container
COPY . /app

# Menginstal semua dependensi yang tercantum dalam requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Menjalankan aplikasi dengan Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Menggunakan image Python resmi yang ringan
FROM python:3.11-slim

# Menyiapkan working directory di dalam container
WORKDIR /app

# Menyalin file requirements.txt
COPY requirements.txt /app/

# Instal dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode proyek
COPY . /app/

# Mengekspos port 8501 (Port standar Streamlit)
EXPOSE 8501

# Command untuk menjalankan aplikasi di Azure Web App
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

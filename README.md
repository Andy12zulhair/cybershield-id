# Cybershield ID: Phishing URL Detection

Proyek ini bertujuan untuk mendeteksi URL phishing menggunakan Machine Learning.

## Struktur Folder
- `data/`: Dataset Phishing URL.
- `models/`: Model yang sudah dilatih (pickle).
- `notebooks/`: Eksperimen analisis data (EDA).
- `app.py`: Dashboard Streamlit terintegrasi.
- `features.py`: Modul ekstraksi fitur dari string URL.
- `train_model.py`: Script untuk melatih model Random Forest.
- `assets/`: Logo dan gambar pendukung.
- `Dockerfile`: Konfigurasi untuk deployment ke Azure.

## Cara Menjalankan Lokal
1. Aktifkan virtual environment: `venv\Scripts\activate` (Windows)
2. Install dependencies: `pip install -r requirements.txt`
3. Train model (Opsional jika ingin melatih ulang): `python train_model.py`
4. Jalankan Streamlit: `streamlit run app.py`

## Deployment ke Microsoft Azure
Proyek ini disiapkan untuk di-deploy ke **Azure Web App for Containers** (Layanan Microsoft Azure).
1. Pastikan Anda memiliki akun Azure dan Docker terinstal.
2. Build Docker image: 
   ```bash
   docker build -t cybershield-id .
   ```
3. Push image ke **Azure Container Registry (ACR)**.
4. Buat **Azure Web App** dan atur sumber image dari ACR tersebut. Aplikasi akan otomatis live!

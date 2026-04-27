import streamlit as st
import joblib
import pandas as pd
from features import extract_features, FEATURE_COLUMNS
import re

st.set_page_config(page_title="CyberShield ID", page_icon="🛡️", layout="wide")
st.title("🛡️ CyberShield ID - Detektor Phishing Indonesia")

# Load model
model = joblib.load('models/phishing_model.pkl')

# Sidebar navigasi
menu = st.sidebar.selectbox("Menu", ["Deteksi URL", "Edukasi Phishing", "Simulasi Serangan", "Cek Kerentanan"])

if menu == "Deteksi URL":
    st.subheader("🔍 Deteksi URL Phishing")
    url_input = st.text_input("Masukkan URL yang ingin dicek:", "https://example.com")

    if st.button("Cek Sekarang"):
        if url_input.strip():
            # Ekstrak fitur dari URL menggunakan modul features.py
            features = extract_features(url_input.strip())
            features_df = pd.DataFrame([features])[FEATURE_COLUMNS]

            # Prediksi
            prediction = model.predict(features_df)[0]
            proba = model.predict_proba(features_df)[0]

            if prediction == 0:
                st.success(f"✅ URL ini kemungkinan AMAN (confidence: {proba[0]*100:.1f}%)")
            else:
                st.error(f"⚠️ PERINGATAN: URL ini kemungkinan PHISHING! (confidence: {proba[1]*100:.1f}%)")
                st.warning("💡 **Actionable Insight:** Jangan klik tautan ini atau masukkan data pribadi Anda. Segera tinggalkan halaman ini.")

            st.markdown("---")
            st.subheader("📊 Analisis Mengapa URL Ini Diklasifikasikan Demikian")
            
            # Ambil Feature Importances dari Random Forest
            importances = model.feature_importances_
            feature_imp_df = pd.DataFrame({
                'Fitur': FEATURE_COLUMNS,
                'Kepentingan Model (%)': importances * 100,
                'Nilai URL Anda': features_df.iloc[0].values
            }).sort_values('Kepentingan Model (%)', ascending=False)

            # Menampilkan 5 Fitur Terpenting yang memengaruhi keputusan
            top_5 = feature_imp_df.head(5)
            
            import plotly.express as px
            import plotly.graph_objects as go
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Top 5 Fitur Penentu (Kepentingan Model):**")
                fig = px.bar(top_5, x='Kepentingan Model (%)', y='Fitur', orientation='h', 
                             title="Bobot Fitur terhadap Keputusan",
                             color='Kepentingan Model (%)', color_continuous_scale='Reds')
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                st.markdown("**Detail Nilai URL Anda pada Top 5 Fitur:**")
                st.dataframe(top_5[['Fitur', 'Nilai URL Anda']], hide_index=True)
                st.info("💡 **Penjelasan:** Model Machine Learning menggunakan pola dari ratusan ribu URL. Jika URL Anda memiliki panjang tak wajar atau banyak karakter spesial (angka, simbol), AI akan mencurigainya sebagai phishing.")

            # Tampilkan semua detail fitur
            with st.expander("Lihat seluruh detail 18 fitur yang diekstrak"):
                st.dataframe(features_df.T.rename(columns={0: 'Nilai Ekstraksi'}))
        else:
            st.warning("Silakan masukkan URL terlebih dahulu!")

elif menu == "Edukasi Phishing":
    st.subheader("📚 Edukasi Keamanan Siber (Bahasa Indonesia)")
    st.write("5 Tanda URL Phishing yang Harus Diwaspadai:")
    st.markdown("""
    1. URL panjang & aneh (banyak angka/huruf acak)
    2. Domain mirip tapi salah eja (g00gle.com, bankindonesia.id)
    3. Pakai https tapi ikon gembok palsu
    4. Minta data pribadi mendadak
    5. Link dari email/SMS yang tidak diminta
    """)

elif menu == "Simulasi Serangan":
    st.subheader("🎯 Simulasi Serangan Phishing")
    st.write("Coba tebak mana yang phishing!")
    # Bisa tambah quiz interaktif di sini

elif menu == "Cek Kerentanan":
    st.subheader("🔐 Cek Kerentanan Akun/Perangkat")
    password = st.text_input("Masukkan password contoh:", type="password")

    if password:
        score = 0
        feedback = []

        if len(password) >= 12:
            score += 1
        else:
            feedback.append("- Gunakan minimal 12 karakter")

        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("- Tambahkan huruf kapital (A-Z)")

        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("- Tambahkan huruf kecil (a-z)")

        if re.search(r'[0-9]', password):
            score += 1
        else:
            feedback.append("- Tambahkan angka (0-9)")

        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            feedback.append("- Tambahkan simbol (!@#$%...)")

        if score == 5:
            st.success("🟢 Password KUAT!")
        elif score >= 3:
            st.warning("🟡 Password SEDANG - bisa ditingkatkan")
        else:
            st.error("🔴 Password LEMAH!")

        if feedback:
            st.write("Saran perbaikan:")
            for f in feedback:
                st.write(f)

st.caption("CyberShield ID \u00a9 2026 - Dibuat untuk Microsoft AI Impact Challenge")

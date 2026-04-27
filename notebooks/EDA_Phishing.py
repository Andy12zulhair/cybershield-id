# %% [markdown]
# # Exploratory Data Analysis (EDA) - Phishing URL Dataset
# Notebook ini digunakan untuk mengeksplorasi dataset Phishing URL, memahami distribusi fitur,
# serta memilih fitur-fitur yang paling relevan untuk mendeteksi URL berbahaya.
# Ini mencakup aspek **Metodologi dan Eksplorasi Data**.

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi visualisasi
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Load Data
data_path = '../data/PhiUSIIL_Phishing_URL_Dataset.csv'
if not os.path.exists(data_path):
    print("Dataset tidak ditemukan. Pastikan path sudah benar.")
else:
    df = pd.read_csv(data_path)
    print("Dataset berhasil dimuat!")
    print(f"Jumlah baris: {df.shape[0]}, Jumlah kolom: {df.shape[1]}")

# %% [markdown]
# ## 1. Distribusi Kelas Target (Label)
# Memeriksa keseimbangan antara kelas URL legitimate (0) dan phishing (1).

# %%
plt.figure(figsize=(6, 4))
ax = sns.countplot(x='label', data=df, palette='viridis')
plt.title('Distribusi URL (0 = Aman, 1 = Phishing)')
plt.xlabel('Kelas')
plt.ylabel('Jumlah')
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='baseline', fontsize=11, color='black', xytext=(0, 5),
                textcoords='offset points')
plt.show()

# %% [markdown]
# ## 2. Analisis Fitur URL Length
# Apakah URL phishing cenderung lebih panjang dari URL biasa?

# %%
plt.figure(figsize=(10, 6))
sns.histplot(data=df[df['URLLength'] < 200], x='URLLength', hue='label', bins=50, kde=True, palette='viridis')
plt.title('Distribusi Panjang URL (dibatasi < 200 karakter)')
plt.xlabel('Panjang URL')
plt.ylabel('Frekuensi')
plt.show()

# %% [markdown]
# *Insight:* URL Phishing sering kali mencoba menyembunyikan identitas aslinya dengan membuat URL yang lebih panjang atau menambahkan banyak subdomain.

# %% [markdown]
# ## 3. Analisis Karakter Spesial dan Angka
# Phishing sering menggunakan karakter khusus dan angka acak. Mari kita lihat korelasinya.

# %%
features_to_compare = ['NoOfLettersInURL', 'NoOfDegitsInURL', 'NoOfOtherSpecialCharsInURL', 'SpacialCharRatioInURL', 'label']
sample_df = df[features_to_compare].dropna()

corr_matrix = sample_df.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
plt.title('Korelasi Fitur Teks URL terhadap Target (Label)')
plt.show()

# %% [markdown]
# ## 4. Feature Selection untuk Model Real-time
# Untuk kompetisi dan penggunaan praktis, kita tidak bisa mengekstrak fitur konten (seperti HTML tag) 
# karena lambat dan tidak efisien. Oleh karena itu, kita memilih fitur-fitur berbasis sintaks URL.

# %%
SELECTED_FEATURES = [
    'URLLength', 'DomainLength', 'IsDomainIP', 'TLDLength', 'NoOfSubDomain', 
    'HasObfuscation', 'NoOfObfuscatedChar', 'ObfuscationRatio', 'NoOfLettersInURL', 
    'LetterRatioInURL', 'NoOfDegitsInURL', 'DegitRatioInURL', 'NoOfEqualsInURL', 
    'NoOfQMarkInURL', 'NoOfAmpersandInURL', 'NoOfOtherSpecialCharsInURL', 
    'SpacialCharRatioInURL', 'IsHTTPS'
]

print(f"Menggunakan {len(SELECTED_FEATURES)} fitur untuk pemodelan agar dapat berjalan real-time.")

# %% [markdown]
# EDA selesai. Insight ini akan diintegrasikan langsung ke dashboard Streamlit untuk menjelaskan kepada pengguna 
# *mengapa* sebuah URL terdeteksi sebagai phishing.

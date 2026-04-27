import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from features import FEATURE_COLUMNS

# Load dataset
df = pd.read_csv('data/PhiUSIIL_Phishing_URL_Dataset.csv')

# Gunakan HANYA fitur URL-based yang sama dengan features.py
X = df[FEATURE_COLUMNS]
y = df['label']

print(f"Dataset: {X.shape[0]} baris, {X.shape[1]} fitur")
print(f"Fitur: {FEATURE_COLUMNS}")
print(f"Distribusi label:\n{y.value_counts()}")
print("-" * 50)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluasi
y_pred = model.predict(X_test)
print("Akurasi:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Simpan model
joblib.dump(model, 'models/phishing_model.pkl')
print("[OK] Model berhasil disimpan ke models/phishing_model.pkl")
print(f"[OK] Model dilatih dengan {len(FEATURE_COLUMNS)} fitur URL-based")

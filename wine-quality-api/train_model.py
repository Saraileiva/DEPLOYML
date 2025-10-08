import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

# Cargar dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
df = pd.read_csv(url, sep=';')

# Preparar datos
# Convertir calidad a binario: >=6 = high (1), <6 = low (0)
df['quality_binary'] = (df['quality'] >= 6).astype(int)

X = df.drop(['quality', 'quality_binary'], axis=1)
y = df['quality_binary']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Escalar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entrenar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluar
accuracy = model.score(X_test_scaled, y_test)
print(f"Accuracy: {accuracy:.2%}")

# Guardar modelo y scaler
joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("Modelo guardado exitosamente!")
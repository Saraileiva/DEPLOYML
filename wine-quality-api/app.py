from flask import Flask, request, jsonify
import joblib
import numpy as np

# Inicializar Flask
app = Flask(__name__)

# ⚠️ ¡IMPORTANTE! Asegúrate de que esta ruta sea la correcta para tu despliegue en PythonAnywhere.
BASE_PATH = '/home/sarahy28leiv/DEPLOYML/wine-quality-api' 

# Cargar modelo y scaler
model = joblib.load(f'{BASE_PATH}/model.pkl')
scaler = joblib.load(f'{BASE_PATH}/scaler.pkl')

# Nombres de las características
FEATURE_NAMES = [
    'fixed_acidity', 'volatile_acidity', 'citric_acid',
    'residual_sugar', 'chlorides', 'free_sulfur_dioxide',
    'total_sulfur_dioxide', 'density', 'pH',
    'sulphates', 'alcohol'
]

# ➕ PUNTO EXTRA: Rangos Válidos (mínimo, máximo)
VALID_RANGES = {
    'fixed_acidity': (4.6, 15.9),
    'volatile_acidity': (0.12, 1.58),
    'citric_acid': (0.0, 1.0),
    'residual_sugar': (0.9, 15.5),
    'chlorides': (0.012, 0.61),
    'free_sulfur_dioxide': (1.0, 72.0),
    'total_sulfur_dioxide': (6.0, 289.0),
    'density': (0.99, 1.0037),
    'pH': (2.74, 4.01),
    'sulphates': (0.33, 2.0),
    'alcohol': (8.4, 14.9)
}

@app.route('/')
def home():
    """Endpoint principal con información de la API"""
    return jsonify({
        'message': 'Wine Quality Prediction API',
        'version': '1.0',
        'endpoints': {
            '/': 'Información de la API',
            '/health': 'Health check',
            '/stats': 'Estadísticas del modelo (Punto Extra)',
            '/predict': 'Predicción de calidad (POST)',
            '/example': 'Ejemplo de datos de entrada'
        },
        'author': 'Miriam Sarai Leiva Cabrera'
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    })

@app.route('/example')
def example():
    """Retorna un ejemplo de datos de entrada"""
    return jsonify({
        'example_input': {
            'fixed_acidity': 7.4,
            'volatile_acidity': 0.7,
            'citric_acid': 0.0,
            'residual_sugar': 1.9,
            'chlorides': 0.076,
            'free_sulfur_dioxide': 11.0,
            'total_sulfur_dioxide': 34.0,
            'density': 0.9978,
            'pH': 3.51,
            'sulphates': 0.56,
            'alcohol': 9.4
        },
        'expected_output': {
            'quality': 'low',
            'probability_low': 0.85,
            'probability_high': 0.15
        }
    })

# ➕ PUNTO EXTRA: Endpoint de Estadísticas
@app.route('/stats')
def stats():
    """Retorna estadísticas del modelo"""
    return jsonify({
        'model_type': 'Random Forest Classifier',
        'n_features': 11,
        'accuracy': 0.85,
        'training_samples': 1279,
        'test_samples': 320
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para hacer predicciones. Incluye:
    - Validación de campos faltantes.
    - Validación de rangos (Punto Extra).
    """
    try:
        # 1. Obtener datos del request
        data = request.get_json()
        
        # 2. Validar que todos los campos estén presentes
        missing_fields = [field for field in FEATURE_NAMES if field not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing fields',
                'missing': missing_fields
            }), 400
        
        # 3. ➕ PUNTO EXTRA: Validación de Rangos
        invalid_inputs = {}
        for field, (min_val, max_val) in VALID_RANGES.items():
            value = float(data[field])
            if not (min_val <= value <= max_val):
                invalid_inputs[field] = f"Value {value} is out of range ({min_val} to {max_val})"
        
        if invalid_inputs:
            return jsonify({
                'error': 'Input validation failed (Out of Range)',
                'invalid_fields': invalid_inputs
            }), 400
        
        # 4. Extraer y Escalar features
        features = [float(data[field]) for field in FEATURE_NAMES]
        features_array = np.array(features).reshape(1, -1)
        
        features_scaled = scaler.transform(features_array)
        
        # 5. Hacer predicción
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # 6. Preparar respuesta
        quality = 'high' if prediction == 1 else 'low'
        
        return jsonify({
            'quality': quality,
            'probability_low': float(probabilities[0]),
            'probability_high': float(probabilities[1]),
            'confidence': float(max(probabilities)),
            'input_features': data
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Para desarrollo local
    app.run(debug=True, host='0.0.0.0', port=5000)
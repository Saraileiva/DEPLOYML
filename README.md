# Wine Quality Prediction API

API para predecir la calidad de vinos basándose en características químicas.

## Autor
**Miriam Sarai Leiva Cabrera**

## Dataset
Wine Quality Dataset - UCI Machine Learning Repository
**https://sarahy28leiv.pythonanywhere.com**

## Modelo
- Algoritmo: Random Forest Classifier
- Accuracy: ~85%
- Features: 11 características químicas

## Endpoints

### GET /
Información general de la API

### GET /health
Health check del servicio
```json
curl https://sarahy28leiv.pythonanywhere.com/health
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true
} 
```

### GET /example
Ejemplo de datos de entrada
```json
curl https://sarahy28leiv.pythonanywhere.com/example

{ 
    "example_input":{"alcohol":9.4,"chlorides":0.076,"citric_acid":0.0,"density":0.9978,"fixed_acidity":7.4,"free_sulfur_dioxide":11.0,"pH":3.51,"residual_sugar":1.9,"sulphates":0.56,"total_sulfur_dioxide":34.0,"volatile_acidity":0.7},"expected_output":{"probability_high":0.15,"probability_low":0.85,"quality":"low"}
}
```

### GET /stats
Retorna metadatos y métricas de rendimiento del modelo entrenado.

Response:
```json
curl https://sarahy28leiv.pythonanywhere.com/stats
{
  "model_type": "Random Forest Classifier",
  "n_features": 11,
  "accuracy": 0.85,
  "training_samples": 1279,
  "test_samples": 320
}
```

### POST /predict
Realiza una predicción
```json
Request:
{
  "fixed_acidity": 7.4,
  "volatile_acidity": 0.7,
  "citric_acid": 0.0,
  "residual_sugar": 1.9,
  "chlorides": 0.076,
  "free_sulfur_dioxide": 11.0,
  "total_sulfur_dioxide": 34.0,
  "density": 0.9978,
  "pH": 3.51,
  "sulphates": 0.56,
  "alcohol": 9.4
}

Response:

{
  "quality": "low",
  "probability_low": 0.85,
  "probability_high": 0.15,
  "confidence": 0.85
}
```

### Validación de Entrada
El endpoint /predict aplica una validación de rangos a las 11 características. Si algún valor está fuera del rango histórico (basado en el dataset original), la API retornará un código de error HTTP 400 Bad Request en lugar de una predicción.

**Ejemplo de Error (HTTP 400):**
```json
{
  "error": "Input validation failed (Out of Range)",
  "invalid_fields": {
    "fixed_acidity": "Value 20.0 is out of range (4.6 to 15.9)"
  }
}
```

### Uso Local
pip install -r requirements.txt
python app.py

### URL de Producción
**https://sarahy28leiv.pythonanywhere.com**

### Fecha de Deployment
**07/10/2025**


### 4. Uso Local (Para Desarrollo o Testeo)
Si quieres ejecutar la API en tu propia computadora:

Asegúrate de tener los archivos **app.py, model.pkl, scaler.pkl y requirements.txt** en el mismo directorio.

Activa tu entorno virtual (source env/bin/activate).

Instala las dependencias:
**pip install -r requirements.txt**

Ejecuta la aplicación:
**python app.py**

La API estará disponible en https://sarahy28leiv.pythonanywhere.com/
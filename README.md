# Predicción de contratación de depósitos a plazo

Aplicación sencilla de Regresión Logística con `bank.csv`, FastAPI y una UI HTML/JavaScript.

## Uso

```bash
pip install -r requirements.txt
python training/train.py
uvicorn app.main:app --reload
```

Abrir http://127.0.0.1:8000. El entrenamiento es independiente y genera `models/bank_marketing_pipeline.joblib` y `models/metrics.json`; `/predict` únicamente carga el modelo persistido e infiere.

La API valida el request mediante `app/schemas.py`. Las variables predictoras son `age`, `job`, `marital`, `education`, `balance`, `housing`, `loan` y `campaign`; `duration` no se utiliza.

## Preguntas de reflexión

¿Por qué el modelo se entrena fuera de la API y no dentro de /predict?
Porque el modelo se entrenaría cada vez que se hiciera una llamada POST /predict a la API, lo cual se ejecuta
cada vez que se hace una predicción desde la UI. Esta práctica no es conveniente, dado que las respuestas del modelo podrían variar en gran medida al ser reentrenado múltiples veces, y podrían ejecutar predicciones desacertadas e imposibles de comparar con otros resultados generados por el mismo modelo. 

¿Por qué es importante utilizar durante inferencia exactamente el mismo preprocesamiento utilizado durante entrenamiento?
Para que el modelo trabaje con datos que tengan el mismo formato y limpieza con el que se entrenó, de forma que se obtengan datos más confiables, comparables, y exactos. 

¿Qué diferencia existe entre predict() y predict_proba() en este problema?
'Predict()' se encarga de usar el modelo entrenado para determinar si el cliente potencialmente contratará o no un depósito a plazo ('yes' o 'no'). 
'predict_proba()' se encarga de determinar la probabilidad (0-1) de que se contrate o no el depósito a plazo por el cliente. 

Si el modelo devuelve una probabilidad de 0.72, ¿qué significa ese valor y qué NO significa?
Significa que el cliente está potencialmente interesado en el depósito a plazo, pero no quiere decir que lo vaya a ser (tampoco quiere decir que el dato sea completamente confiable, dado que debemos consultar métricas como accuracy, precision, recall, f1_score).

¿Por qué duration no debería utilizarse en este sistema si queremos hacer la predicción antes de contactar al cliente?
Porque la variable 'duration' registra la duración (en segundos) de la última llamada hecha al cliente (es decir, esta variable obtiene un valor después de hacer el primer contacto con el cliente), por lo que no tendría sentido tomarla en cuenta para el sistema si la predección se desea hacer antes de contactar al cliente.

¿Qué ocurriría si mañana cambia la estructura de los datos enviados por el frontend?
Habría que modificar los archivos de la API (schemas.py, inference.py) y frontend (index.html, app.js) relativos a la validación y preprocesamiento de datos, además de tener que eliminar el modelo con el entrenamiento actual y volver a entrenarlo con la nueva estructura de los datos. 

## Evidencia 
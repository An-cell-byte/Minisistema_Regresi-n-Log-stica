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
Significa que el cliente está potencialmente interesado en el depósito a plazo, pero no quiere decir que lo vaya a ser (tampoco quiere decir que el dato sea completamente confiable, dado que debemos consultar métricas como accuracy, precision, recall, f1_score). El umbral usado para los valores de probabilidad fue: potencialmente interesado >= 0.5 < baja propensión . 

¿Por qué duration no debería utilizarse en este sistema si queremos hacer la predicción antes de contactar al cliente?
Porque la variable 'duration' registra la duración (en segundos) de la última llamada hecha al cliente (es decir, esta variable obtiene un valor después de hacer el primer contacto con el cliente), por lo que no tendría sentido tomarla en cuenta para el sistema si la predección se desea hacer antes de contactar al cliente.

¿Qué ocurriría si mañana cambia la estructura de los datos enviados por el frontend?
Habría que modificar los archivos de la API (schemas.py, inference.py) y frontend (index.html, app.js) relativos a la validación y preprocesamiento de datos, además de tener que eliminar el modelo con el entrenamiento actual y volver a entrenarlo con la nueva estructura de los datos. 

## Evidencia 

Caso A — Inferencia válida y evaluación de métricas de entrenamiento

<img width="959" height="503" alt="Screenshot 2026-08-18 112541" src="https://github.com/user-attachments/assets/b9fe1e66-0783-4b29-bc75-880d99993d1f" />
<img width="954" height="498" alt="Screenshot 2026-08-18 113900" src="https://github.com/user-attachments/assets/d36ed97d-7c95-42a2-b3ab-bc38c7cad756" />

Explicación de las métricas:
La métrica `accuracy` representa el porcentaje total de predicciones correctas realizadas por el modelo, incluyendo los clientes que sí contrataron el depósito y los que no. En este caso, el valor obtenido fue de 0.6099, por lo que el modelo acertó aproximadamente el 60.99% de las predicciones.

La métrica `precision` indica, de todos los clientes que el modelo clasificó como interesados en contratar el depósito (`yes`), cuántos realmente pertenecían a esa categoría. Su valor fue de 0.1608, lo que significa que el 16.08% de las predicciones positivas fueron correctas.

La métrica `recall` muestra qué proporción de los clientes que realmente contrataron el depósito fue identificada correctamente por el modelo. El valor obtenido fue de 0.5673, por lo que se detectó aproximadamente el 56.73% de los casos positivos.

La métrica `f1_score` combina `precision` y `recall` en un solo valor mediante su media armónica, por lo que permite evaluar el equilibrio entre ambas métricas. En este entrenamiento se obtuvo un valor de 0.2505; esto refleja que, aunque el modelo identifica una parte importante de los casos positivos, su precisión es baja y existen predicciones positivas incorrectas.

Caso B — Inferencia con error

<img width="959" height="502" alt="Screenshot 2026-08-18 112600" src="https://github.com/user-attachments/assets/4880737c-1712-4698-8a18-f692c7803d6d" />
<img width="959" height="497" alt="Screenshot 2026-08-18 112614" src="https://github.com/user-attachments/assets/d191078d-a86b-425e-8a9c-1291eb9097e9" />

Caso C — Frontend

<img width="959" height="503" alt="Screenshot 2026-08-18 113321" src="https://github.com/user-attachments/assets/d419b13b-5f34-49bd-9152-157d79b04ba0" />
<img width="959" height="485" alt="Screenshot 2026-08-18 113303" src="https://github.com/user-attachments/assets/3320f546-a36d-4ec9-b793-0cf2984710f6" />
<img width="782" height="423" alt="Screenshot 2026-08-18 112904" src="https://github.com/user-attachments/assets/f0abc6ff-f656-479f-b32c-f167ffab72a4" />


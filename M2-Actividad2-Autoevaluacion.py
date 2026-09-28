"""
Módulo 2 · Aprendizaje Automático (Machine Learning)
Actividad 2 · Actividades y Autoevaluación

Curso: Introducción a la Inteligencia Artificial

Este programa permite practicar conceptos básicos de:
- Aprendizaje supervisado
- Aprendizaje no supervisado
- Regresión
- Clasificación
- Clustering
- Evaluación de modelos

Requisitos:
    pip install numpy pandas scikit-learn
"""

import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score


# ============================================================
# 1. ACTIVIDAD: REGRESIÓN LINEAL
# ============================================================

print("=" * 60)
print("ACTIVIDAD 1 · REGRESIÓN LINEAL")
print("=" * 60)

# Datos de ejemplo:
# horas de estudio -> calificación
datos = pd.DataFrame({
    "horas_estudio": [1, 2, 3, 4, 5, 6],
    "calificacion": [50, 55, 60, 65, 70, 78]
})

X = datos[["horas_estudio"]]
y = datos["calificacion"]

modelo = LinearRegression()
modelo.fit(X, y)

# Predicción
horas = pd.DataFrame({
    "horas_estudio": [8]
})

prediccion = modelo.predict(horas)

print(
    f"Si un estudiante estudia 8 horas, "
    f"la calificación estimada es: {prediccion[0]:.2f}"
)

print("""
Pregunta:
¿Por qué esta predicción no significa que el estudiante
necesariamente obtendrá esa calificación?
""")


# ============================================================
# 2. ACTIVIDAD: CLUSTERING CON K-MEANS
# ============================================================

print("\n" + "=" * 60)
print("ACTIVIDAD 2 · CLUSTERING CON K-MEANS")
print("=" * 60)

# Datos de ejemplo:
# horas de estudio y horas de uso de computadora
datos_cluster = pd.DataFrame({
    "horas_estudio": [1, 2, 2, 8, 9, 10],
    "horas_computadora": [8, 7, 9, 2, 3, 2]
})

modelo_kmeans = KMeans(
    n_clusters=2,
    random_state=42,
    n_init=10
)

modelo_kmeans.fit(datos_cluster)

datos_cluster["grupo"] = modelo_kmeans.labels_

print("Datos agrupados:")
print(datos_cluster)

print("""
Interpretación posible:

Grupo 0 y Grupo 1 representan grupos encontrados
automáticamente por el algoritmo.

Importante:
K-Means no sabe qué significa cada grupo.
La interpretación depende de las características de los datos.
""")


# ============================================================
# 3. ACTIVIDAD: EVALUACIÓN DE UNA CLASIFICACIÓN
# ============================================================

print("\n" + "=" * 60)
print("ACTIVIDAD 3 · EVALUACIÓN")
print("=" * 60)

# Valores reales
valores_reales = [
    "Aprobado",
    "Aprobado",
    "No aprobado",
    "Aprobado",
    "No aprobado"
]

# Valores predichos por un modelo
valores_predichos = [
    "Aprobado",
    "No aprobado",
    "No aprobado",
    "Aprobado",
    "No aprobado"
]

exactitud = accuracy_score(
    valores_reales,
    valores_predichos
)

print(f"Exactitud del modelo: {exactitud * 100:.2f}%")

print("""
La exactitud indica qué porcentaje de las predicciones
coincidió con los valores reales.
""")


# ============================================================
# 4. ACTIVIDAD DE REFLEXIÓN
# ============================================================

print("\n" + "=" * 60)
print("ACTIVIDAD 4 · REFLEXIÓN")
print("=" * 60)

print("""
Responde las siguientes preguntas:

1. ¿Qué diferencia existe entre aprendizaje supervisado
   y aprendizaje no supervisado?

2. ¿Para qué sirve una regresión lineal?

3. ¿Qué tipo de problema puede resolverse mediante
   clasificación?

4. ¿Qué objetivo tiene el algoritmo K-Means?

5. ¿Qué significa evaluar un modelo de Machine Learning?

6. ¿Por qué es importante utilizar datos adecuados
   para entrenar un modelo?
""")


# ============================================================
# 5. AUTOEVALUACIÓN
# ============================================================

print("\n" + "=" * 60)
print("AUTOEVALUACIÓN")
print("=" * 60)

preguntas = [
    {
        "pregunta": "1. ¿Qué tipo de aprendizaje utiliza datos etiquetados?",
        "opciones": [
            "a) Supervisado",
            "b) No supervisado",
            "c) Aleatorio"
        ],
        "respuesta": "a"
    },
    {
        "pregunta": "2. ¿Cuál de estos algoritmos sirve para agrupamiento?",
        "opciones": [
            "a) Regresión lineal",
            "b) K-Means",
            "c) Árbol de decisión"
        ],
        "respuesta": "b"
    },
    {
        "pregunta": "3. ¿Qué produce una regresión lineal?",
        "opciones": [
            "a) Un valor numérico",
            "b) Un grupo de usuarios",
            "c) Una imagen"
        ],
        "respuesta": "a"
    },
    {
        "pregunta": "4. ¿Qué mide la exactitud (accuracy)?",
        "opciones": [
            "a) La cantidad de datos",
            "b) El porcentaje de predicciones correctas",
            "c) La velocidad del programa"
        ],
        "respuesta": "b"
    },
    {
        "pregunta": "5. ¿Qué algoritmo clasifica observando ejemplos cercanos?",
        "opciones": [
            "a) k-NN",
            "b) K-Means",
            "c) Regresión lineal"
        ],
        "respuesta": "a"
    }
]

puntaje = 0

for pregunta in preguntas:
    print("\n" + pregunta["pregunta"])

    for opcion in pregunta["opciones"]:
        print(opcion)

    respuesta = input("Tu respuesta: ").strip().lower()

    if respuesta == pregunta["respuesta"]:
        print("Correcto.")
        puntaje += 1
    else:
        print(
            f"Incorrecto. La respuesta correcta es: "
            f"{pregunta['respuesta']}"
        )


# ============================================================
# RESULTADO
# ============================================================

print("\n" + "=" * 60)
print("RESULTADO DE LA AUTOEVALUACIÓN")
print("=" * 60)

print(f"Respuestas correctas: {puntaje} de {len(preguntas)}")

porcentaje = (puntaje / len(preguntas)) * 100

print(f"Porcentaje obtenido: {porcentaje:.0f}%")

if porcentaje == 100:
    print("Excelente. Comprendiste los conceptos principales.")
elif porcentaje >= 60:
    print("Buen trabajo. Repasa los conceptos que presentaron dificultades.")
else:
    print("Se recomienda revisar nuevamente el material del módulo.")
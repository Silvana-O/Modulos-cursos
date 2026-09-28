"""
Módulo 2 · Aprendizaje Automático (Machine Learning)
Actividad 1 · Primeros modelos de Machine Learning

Curso: Introducción a la Inteligencia Artificial

Este archivo contiene ejemplos sencillos de:
- Regresión lineal
- Árbol de decisión
- k-Nearest Neighbors (k-NN)

Requisitos:
    pip install numpy pandas scikit-learn
"""

import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


# ============================================================
# 1. REGRESIÓN LINEAL
# ============================================================

print("=" * 60)
print("1. REGRESIÓN LINEAL")
print("=" * 60)

# Datos de ejemplo:
# Horas de estudio -> calificación obtenida
datos_regresion = pd.DataFrame({
    "horas_estudio": [1, 2, 3, 4, 5, 6],
    "calificacion": [50, 55, 60, 65, 70, 78]
})

X = datos_regresion[["horas_estudio"]]
y = datos_regresion["calificacion"]

modelo_regresion = LinearRegression()
modelo_regresion.fit(X, y)

# Predicción para un estudiante que estudia 7 horas
nuevo_estudiante = pd.DataFrame({
    "horas_estudio": [7]
})

prediccion = modelo_regresion.predict(nuevo_estudiante)

print(f"Coeficiente: {modelo_regresion.coef_[0]:.2f}")
print(f"Intercepto: {modelo_regresion.intercept_:.2f}")
print(
    f"Predicción para 7 horas de estudio: "
    f"{prediccion[0]:.2f}"
)


# ============================================================
# 2. ÁRBOL DE DECISIÓN
# ============================================================

print("\n" + "=" * 60)
print("2. ÁRBOL DE DECISIÓN")
print("=" * 60)

# Datos de ejemplo:
# Horas de estudio + asistencia -> aprobado / no aprobado
datos_arbol = pd.DataFrame({
    "horas_estudio": [1, 2, 2, 3, 4, 5, 6, 7],
    "asistencia": [50, 60, 65, 70, 75, 80, 90, 95],
    "resultado": [
        "No aprobado",
        "No aprobado",
        "No aprobado",
        "No aprobado",
        "Aprobado",
        "Aprobado",
        "Aprobado",
        "Aprobado"
    ]
})

X = datos_arbol[["horas_estudio", "asistencia"]]
y = datos_arbol["resultado"]

modelo_arbol = DecisionTreeClassifier(random_state=42)
modelo_arbol.fit(X, y)

nuevo_estudiante = pd.DataFrame({
    "horas_estudio": [4],
    "asistencia": [80]
})

prediccion = modelo_arbol.predict(nuevo_estudiante)

print(
    f"Predicción para 4 horas de estudio y 80% de asistencia: "
    f"{prediccion[0]}"
)


# ============================================================
# 3. k-NEAREST NEIGHBORS (k-NN)
# ============================================================

print("\n" + "=" * 60)
print("3. k-NEAREST NEIGHBORS (k-NN)")
print("=" * 60)

# Datos de ejemplo:
# Horas de estudio + asistencia -> aprobado / no aprobado
datos_knn = pd.DataFrame({
    "horas_estudio": [1, 2, 2, 3, 4, 5, 6, 7],
    "asistencia": [50, 60, 65, 70, 75, 80, 90, 95],
    "resultado": [
        "No aprobado",
        "No aprobado",
        "No aprobado",
        "No aprobado",
        "Aprobado",
        "Aprobado",
        "Aprobado",
        "Aprobado"
    ]
})

X = datos_knn[["horas_estudio", "asistencia"]]
y = datos_knn["resultado"]

modelo_knn = KNeighborsClassifier(n_neighbors=3)
modelo_knn.fit(X, y)

nuevo_estudiante = pd.DataFrame({
    "horas_estudio": [4],
    "asistencia": [80]
})

prediccion = modelo_knn.predict(nuevo_estudiante)

print(
    f"Predicción para 4 horas de estudio y 80% de asistencia: "
    f"{prediccion[0]}"
)


# ============================================================
# 4. COMPARACIÓN DE MODELOS
# ============================================================

print("\n" + "=" * 60)
print("COMPARACIÓN DE MODELOS")
print("=" * 60)

print("Regresión lineal: predice un valor numérico.")
print("Árbol de decisión: clasifica mediante reglas aprendidas.")
print("k-NN: clasifica observando ejemplos cercanos.")


# ============================================================
# ACTIVIDAD PARA EL ESTUDIANTE
# ============================================================

print("\n" + "=" * 60)
print("ACTIVIDAD")
print("=" * 60)

print("""
Modifica el programa para experimentar con los modelos.

1. Regresión lineal:
   - Agrega nuevos datos de horas de estudio y calificaciones.
   - Cambia la cantidad de horas utilizada para realizar una predicción.

2. Árbol de decisión:
   - Agrega nuevos estudiantes al conjunto de datos.
   - Modifica las horas de estudio y el porcentaje de asistencia.

3. k-NN:
   - Cambia el valor de n_neighbors.
   - Observa si cambia la predicción.

4. Reflexiona:
   - ¿Qué modelo utilizarías para predecir una nota?
   - ¿Qué modelo utilizarías para decidir si un estudiante aprueba?
   - ¿Por qué los resultados pueden cambiar al modificar los datos?
""")
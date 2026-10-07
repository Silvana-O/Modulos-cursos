"""
===============================================================================
MÓDULO 2 - MATERIAL 2: APRENDIZAJE SUPERVISADO (TEÓRICO)
===============================================================================
En este script representamos en código los conceptos explicados en el material:
1. Regresión Lineal (Relación Horas de Estudio vs Puntuación / Ventas vs Publicidad)
2. Clasificación con Árboles de Decisión (Filtro Spam / Criterios de Aprobación)
3. Clasificación con k-Nearest Neighbors (Vecinos más cercanos)
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.neighbors import KNeighborsClassifier

print("=" * 60)
print("1. REGRESIÓN LINEAL: Predicción de Puntuación según Horas de Estudio")
print("=" * 60)

# Datos teóricos del punto 4
X_estudio = np.array([[1], [2], [3], [4], [5], [6]]) # Horas de estudio
y_puntuacion = np.array([45, 50, 58, 65, 72, 78])     # Puntuación obtenida

# Crear y entrenar el modelo de Regresión Lineal
modelo_regresion = LinearRegression()
modelo_regresion.fit(X_estudio, y_puntuacion)

# Ecuación encontrada: y = mx + b
m = modelo_regresion.coef_[0]
b = modelo_regresion.intercept_
print(f"Fórmula encontrada por el modelo: Puntuación = ({m:.2f} * Horas) + {b:.2f}")

# Predicción para un estudiante que estudió 7 horas (Punto 4)
horas_nuevo = np.array([[7]])
prediccion_puntuacion = modelo_regresion.predict(horas_nuevo)
print(f"Predicción para 7 horas de estudio: {prediccion_puntuacion[0]:.2f} puntos\n")


print("=" * 60)
print("2. REGRESIÓN LINEAL: Ejemplo de Ventas según Publicidad")
print("=" * 60)

# Datos del punto 6
df_ventas = pd.DataFrame({
    'Publicidad': [100, 200, 300, 400],
    'Ventas': [1000, 1800, 2500, 3100]
})

modelo_ventas = LinearRegression()
modelo_ventas.fit(df_ventas[['Publicidad']], df_ventas['Ventas'])

inversion_nueva = np.array([[500]])
prediccion_ventas = modelo_ventas.predict(inversion_nueva)
print(f"Ventas estimadas para una inversión de $500 en publicidad: ${prediccion_ventas[0]:.2f}\n")


print("=" * 60)
print("3. ÁRBOLES DE DECISIÓN: Clasificación de Reglas (Ejemplo Actividad/Edad)")
print("=" * 60)

# Datos estructurados basados en el diagrama del punto 9 y 10
# Variables: [Edad, Tiene_Permiso (1=Sí, 0=No)]
X_arbol = np.array([
    [20, 1],
    [22, 0],
    [15, 1],
    [17, 0],
    [25, 1]
])
y_arbol = np.array(['Apto', 'Apto', 'No apto', 'No apto', 'Apto'])

arbol = DecisionTreeClassifier(random_state=42)
arbol.fit(X_arbol, y_arbol)

print("Estructura de reglas del Árbol de Decisión:")
reglas_texto = export_text(arbol, feature_names=['Edad', 'Tiene_Permiso'])
print(reglas_texto)


print("=" * 60)
print("4. k-NEAREST NEIGHBORS (k-NN): Clasificación según Vecinos Cercanos")
print("=" * 60)

# Datos del punto 1 y 13: Horas de Estudio y Asistencia (%) -> Resultado
# 1 = Aprueba, 0 = No aprueba
X_knn = np.array([
    [2, 60],
    [4, 75],
    [6, 90],
    [1, 50]
])
y_knn = np.array(['No aprueba', 'Aprueba', 'Aprueba', 'No aprueba'])

# Entrenar k-NN con k=3 vecinos
knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(X_knn, y_knn)

# Predicción para un nuevo estudiante: 5 horas de estudio, 85% asistencia
estudiante_nuevo = np.array([[5, 85]])
prediccion_knn = knn_model.predict(estudiante_nuevo)
vecinos = knn_model.kneighbors(estudiante_nuevo, return_distance=False)

print(f"Nuevo estudiante -> Horas: 5, Asistencia: 85%")
print(f"Predicción del modelo (k=3): {prediccion_knn[0]}")
print(f"Índices de los {knn_model.n_neighbors} vecinos más cercanos: {vecinos[0].tolist()}\n")
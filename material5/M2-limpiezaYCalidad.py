
"""
MÓDULO 2 · MATERIAL 5
Archivo 1: Limpieza y calidad de datos

Requiere:
    pip install pandas numpy
"""

import pandas as pd
import numpy as np


def demostracion_limpieza():

    print("=" * 60)
    print("1. DETECCIÓN Y TRATAMIENTO DE PROBLEMAS DE CALIDAD")
    print("=" * 60)

    datos = {
        "Estudiante": [
            "Ana",
            "Luis",
            "Marta",
            "Juan",
            "Juan",
            "Pedro"
        ],

        "Edad": [
            20,
            22,
            np.nan,
            21,
            21,
            250
        ],

        "Modalidad": [
            "Presencial",
            "Virtual",
            "Presencial",
            "Virtual",
            "Virtual",
            "Presencial"
        ],

        "Horas": [
            8,
            5,
            7,
            3,
            3,
            4
        ],

        "Asistencia": [
            90,
            75,
            95,
            60,
            60,
            55
        ],

        "Resultado": [
            "Aprobado",
            "Aprobado",
            "Aprobado",
            "Desaprobado",
            "Desaprobado",
            "Desaprobado"
        ]
    }

    df = pd.DataFrame(datos)

    print("\n--- Tabla original ---")
    print(df)

    print("\n--- Valores faltantes por columna ---")
    print(df.isna().sum())

    print("\n--- Registros duplicados ---")
    print(df[df.duplicated(keep=False)])

    # --------------------------------------------------------
    # PASO 1: ELIMINAR DUPLICADOS
    # --------------------------------------------------------

    df_clean = df.drop_duplicates().copy()

    # --------------------------------------------------------
    # PASO 2: VALIDAR EDAD
    # --------------------------------------------------------

    # En este ejemplo, una edad mayor a 100
    # se considera inválida.

    df_clean.loc[
        df_clean["Edad"] > 100,
        "Edad"
    ] = np.nan

    # --------------------------------------------------------
    # PASO 3: IMPUTAR DATOS FALTANTES
    # --------------------------------------------------------

    mediana_edad = df_clean["Edad"].median()

    df_clean["Edad"] = (
        df_clean["Edad"]
        .fillna(mediana_edad)
    )

    print("\n--- Tabla limpia ---")
    print(df_clean)

    print(
        f"\nMediana utilizada para imputar Edad: "
        f"{mediana_edad}"
    )

    print("\nProceso finalizado.")


def actividad_identificacion():

    print("\n" + "=" * 60)
    print("2. ACTIVIDAD DE IDENTIFICACIÓN")
    print("=" * 60)

    datos = {
        "Nombre": [
            "Ana",
            "Luis",
            "Marta",
            "Juan",
            "Juan",
            "Pedro"
        ],

        "Edad": [
            20,
            22,
            np.nan,
            21,
            21,
            250
        ],

        "Departamento": [
            "Salto",
            "Artigas",
            "Salto",
            "Artigas",
            "Artigas",
            "Salto"
        ],

        "Horas de estudio": [
            8,
            5,
            7,
            3,
            3,
            4
        ]
    }

    df = pd.DataFrame(datos)

    print("\nTabla:")
    print(df)

    print("\nRespuestas:")

    print(
        "1. Dato faltante: Marta no tiene Edad."
    )

    print(
        "2. Registro duplicado: Juan aparece dos veces "
        "con los mismos datos."
    )

    print(
        "3. Valor a validar: Pedro tiene Edad = 250."
    )

    print(
        "4. Variable categórica: Departamento."
    )

    print(
        "5. Variables numéricas: Edad y Horas de estudio."
    )


if __name__ == "__main__":

    demostracion_limpieza()

    actividad_identificacion()


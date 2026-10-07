
"""
MÓDULO 2 · MATERIAL 5
Archivo 5: Primer proyecto de preparación de datos

Este ejemplo reúne:

- Limpieza.
- Validación.
- Imputación.
- One-Hot Encoding.
- Escalado.
- División de datos.
- Prevención de Data Leakage.

Requiere:
    pip install pandas numpy scikit-learn
"""

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer

from sklearn.impute import (
    SimpleImputer
)

from sklearn.model_selection import (
    train_test_split
)

from sklearn.pipeline import (
    Pipeline
)

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)


def crear_dataset():

    return pd.DataFrame({

        "Edad": [
            20,
            22,
            np.nan,
            21,
            24,
            250,
            19,
            23,
            25,
            21
        ],

        "Horas_estudio": [
            8,
            5,
            7,
            3,
            9,
            4,
            6,
            8,
            10,
            2
        ],

        "Modalidad": [
            "Presencial",
            "Virtual",
            "Presencial",
            "Virtual",
            "Presencial",
            "Presencial",
            "Virtual",
            "Virtual",
            "Presencial",
            "Virtual"
        ],

        "Resultado": [
            "Aprobado",
            "Aprobado",
            "Aprobado",
            "Desaprobado",
            "Aprobado",
            "Desaprobado",
            "Aprobado",
            "Aprobado",
            "Aprobado",
            "Desaprobado"
        ]
    })


def main():

    # --------------------------------------------------------
    # 1. CREAR DATASET
    # --------------------------------------------------------

    df = crear_dataset()

    print("=" * 60)
    print("DATASET ORIGINAL")
    print("=" * 60)

    print(df)

    # --------------------------------------------------------
    # 2. VALIDACIÓN DE DOMINIO
    # --------------------------------------------------------

    df.loc[
        df["Edad"] > 100,
        "Edad"
    ] = np.nan

    # --------------------------------------------------------
    # 3. ELIMINAR DUPLICADOS
    # --------------------------------------------------------

    df = df.drop_duplicates().copy()

    # --------------------------------------------------------
    # 4. VARIABLES
    # --------------------------------------------------------

    X = df[
        [
            "Edad",
            "Horas_estudio",
            "Modalidad"
        ]
    ]

    y = df["Resultado"]

    # --------------------------------------------------------
    # 5. DIVISIÓN
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.30,
            random_state=42,
            stratify=y
        )
    )

    # --------------------------------------------------------
    # 6. DEFINIR COLUMNAS
    # --------------------------------------------------------

    columnas_numericas = [
        "Edad",
        "Horas_estudio"
    ]

    columnas_categoricas = [
        "Modalidad"
    ]

    # --------------------------------------------------------
    # 7. PIPELINE NUMÉRICO
    # --------------------------------------------------------

    transformacion_numerica = Pipeline(
        steps=[
            (
                "imputacion",
                SimpleImputer(
                    strategy="median"
                )
            ),

            (
                "escalado",
                StandardScaler()
            )
        ]
    )

    # --------------------------------------------------------
    # 8. PIPELINE CATEGÓRICO
    # --------------------------------------------------------

    transformacion_categorica = Pipeline(
        steps=[
            (
                "imputacion",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    # --------------------------------------------------------
    # 9. COLUMN TRANSFORMER
    # --------------------------------------------------------

    preprocesador = ColumnTransformer(
        transformers=[

            (
                "numericas",
                transformacion_numerica,
                columnas_numericas
            ),

            (
                "categoricas",
                transformacion_categorica,
                columnas_categoricas
            )
        ]
    )

    # --------------------------------------------------------
    # 10. AJUSTAR SOLO CON ENTRENAMIENTO
    # --------------------------------------------------------

    X_train_preparado = (
        preprocesador.fit_transform(
            X_train
        )
    )

    # --------------------------------------------------------
    # 11. TRANSFORMAR PRUEBA
    # --------------------------------------------------------

    X_test_preparado = (
        preprocesador.transform(
            X_test
        )
    )

    # --------------------------------------------------------
    # 12. RESULTADOS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("RESULTADO DEL PREPROCESAMIENTO")
    print("=" * 60)

    print(
        "Filas de entrenamiento:",
        X_train_preparado.shape[0]
    )

    print(
        "Filas de prueba:",
        X_test_preparado.shape[0]
    )

    print(
        "Cantidad de características generadas:",
        X_train_preparado.shape[1]
    )

    # --------------------------------------------------------
    # 13. FLUJO REALIZADO
    # --------------------------------------------------------

    print("\nFlujo aplicado:")

    print(
        "1. Validación de edad."
    )

    print(
        "2. Eliminación de duplicados."
    )

    print(
        "3. División entrenamiento/prueba."
    )

    print(
        "4. Imputación y escalado de "
        "variables numéricas."
    )

    print(
        "5. One-Hot Encoding de "
        "variables categóricas."
    )

    print(
        "6. Ajuste de transformaciones "
        "solo con entrenamiento."
    )

    print(
        "7. Aplicación del mismo "
        "preprocesamiento a prueba."
    )

    print(
        "\nProyecto finalizado correctamente."
    )


if __name__ == "__main__":

    main()

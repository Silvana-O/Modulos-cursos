
"""
MÓDULO 2 · MATERIAL 5
Archivo 4: División de datos y prevención de Data Leakage

Requiere:
    pip install pandas scikit-learn
"""

import pandas as pd

from sklearn.model_selection import (
    train_test_split
)

from sklearn.preprocessing import (
    StandardScaler
)


def main():

    datos = pd.DataFrame({

        "Horas_estudio": [
            2, 3, 4, 5, 6,
            7, 8, 9, 10, 11
        ],

        "Asistencia": [
            60, 65, 70, 72, 75,
            80, 82, 85, 90, 95
        ],

        "Resultado": [
            0, 0, 0, 0, 1,
            1, 1, 1, 1, 1
        ]
    })

    # --------------------------------------------------------
    # VARIABLES PREDICTORAS Y OBJETIVO
    # --------------------------------------------------------

    X = datos[
        [
            "Horas_estudio",
            "Asistencia"
        ]
    ]

    y = datos["Resultado"]

    # --------------------------------------------------------
    # DIVISIÓN
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

    print("=" * 60)
    print("DIVISIÓN DE DATOS")
    print("=" * 60)

    print(
        "Entrenamiento:",
        len(X_train),
        "registros"
    )

    print(
        "Prueba:",
        len(X_test),
        "registros"
    )

    # --------------------------------------------------------
    # ESCALADO
    # --------------------------------------------------------

    scaler = StandardScaler()

    # IMPORTANTE:
    # El scaler se ajusta solamente con entrenamiento.

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    # En prueba utilizamos la misma transformación.

    X_test_scaled = scaler.transform(
        X_test
    )

    print(
        "\n--- Parámetros aprendidos "
        "solo con entrenamiento ---"
    )

    print(
        "Medias:",
        scaler.mean_
    )

    print(
        "Desvíos:",
        scaler.scale_
    )

    print(
        "\nPrimeras filas escaladas "
        "de entrenamiento:"
    )

    print(
        X_train_scaled[:3]
    )

    print(
        "\nPrimeras filas escaladas "
        "de prueba:"
    )

    print(
        X_test_scaled[:3]
    )

    # --------------------------------------------------------
    # CONCEPTO CLAVE
    # --------------------------------------------------------

    print("\nRegla clave:")

    print(
        "1. Primero se divide el dataset."
    )

    print(
        "2. Después se ajustan las transformaciones "
        "con X_train."
    )

    print(
        "3. Finalmente se transforman X_train y X_test "
        "con ese mismo ajuste."
    )


if __name__ == "__main__":

    main()


"""
MÓDULO 2 · MATERIAL 5
Archivo 3: Normalización y estandarización

Requiere:
    pip install pandas scikit-learn
"""

import pandas as pd

from sklearn.preprocessing import (
    MinMaxScaler,
    StandardScaler
)


def main():

    datos = pd.DataFrame({

        "Horas_estudio": [
            2,
            4,
            6,
            8,
            10
        ],

        "Ingresos": [
            1000,
            2000,
            3000,
            4000,
            5000
        ]
    })

    print("=" * 60)
    print("DATOS ORIGINALES")
    print("=" * 60)

    print(datos)

    # --------------------------------------------------------
    # NORMALIZACIÓN MIN-MAX
    # --------------------------------------------------------

    min_max = MinMaxScaler()

    datos_minmax = pd.DataFrame(
        min_max.fit_transform(datos),
        columns=datos.columns
    )

    print("\n--- Normalización Min-Max ---")

    print(datos_minmax)

    # --------------------------------------------------------
    # ESTANDARIZACIÓN Z-SCORE
    # --------------------------------------------------------

    standard = StandardScaler()

    datos_zscore = pd.DataFrame(
        standard.fit_transform(datos),
        columns=datos.columns
    )

    print("\n--- Estandarización Z-score ---")

    print(
        datos_zscore.round(3)
    )

    # --------------------------------------------------------
    # INTERPRETACIÓN
    # --------------------------------------------------------

    print("\nInterpretación:")

    print(
        "Min-Max lleva cada variable "
        "aproximadamente al intervalo [0, 1]."
    )

    print(
        "Z-score centra las variables alrededor "
        "de 0 y utiliza su desvío estándar."
    )


if __name__ == "__main__":

    main()

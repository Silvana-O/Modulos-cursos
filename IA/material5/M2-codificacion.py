
"""
MÓDULO 2 · MATERIAL 5
Archivo 2: Codificación de variables categóricas

Requiere:
    pip install pandas scikit-learn
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder


def main():

    datos = pd.DataFrame({

        "Estudiante": [
            "Ana",
            "Luis",
            "Marta",
            "Pedro"
        ],

        "Modalidad": [
            "Presencial",
            "Virtual",
            "Presencial",
            "Virtual"
        ],

        "Departamento": [
            "Salto",
            "Artigas",
            "Salto",
            "Paysandú"
        ]
    })

    print("=" * 60)
    print("DATOS ORIGINALES")
    print("=" * 60)

    print(datos)

    # --------------------------------------------------------
    # LABEL ENCODING
    # --------------------------------------------------------

    label_encoder = LabelEncoder()

    datos["Modalidad_Label"] = (
        label_encoder.fit_transform(
            datos["Modalidad"]
        )
    )

    print("\n--- Label Encoding ---")

    print(
        datos[
            [
                "Modalidad",
                "Modalidad_Label"
            ]
        ]
    )

    print(
        "\nClases detectadas:"
    )

    print(
        list(label_encoder.classes_)
    )

    # --------------------------------------------------------
    # ONE-HOT ENCODING
    # --------------------------------------------------------

    one_hot = pd.get_dummies(
        datos["Departamento"],
        prefix="Departamento",
        dtype=int
    )

    resultado = pd.concat(
        [
            datos,
            one_hot
        ],
        axis=1
    )

    print("\n--- One-Hot Encoding ---")

    print(resultado)

    print("\nInterpretación:")

    print(
        "Label Encoding asigna un número "
        "a cada categoría."
    )

    print(
        "One-Hot Encoding crea una columna "
        "binaria por categoría."
    )


if __name__ == "__main__":

    main()

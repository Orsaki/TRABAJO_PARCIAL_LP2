import pandas as pd
import numpy as np

class Variable:
    def __init__(self, nombre, datos):
        self.nombre = nombre
        self.datos = pd.Series(datos).dropna()  # elimina valores vacíos
        self.tipo = self.detectar_tipo()
        self.n = len(self.datos)

    def detectar_tipo(self):
        try:
            self.datos.astype(float)
            return "cuantitativa"
        except ValueError:
            return "cualitativa"

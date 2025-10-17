import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Variable:
    def __init__(self, nombre, datos):
        self.nombre = nombre
        self.datos = pd.Series(datos).dropna()
        self.tipo = self.detectar_tipo()
        self.n = len(self.datos)

    def detectar_tipo(self):
        try:
            self.datos.astype(float)
            return "cuantitativa"
        except ValueError:
            return "cualitativa"


class VariableCualitativa(Variable):
    def __init__(self, nombre, datos):
        super().__init__(nombre, datos)

    def calcular_moda(self):
        conteo = self.datos.value_counts()
        valor_moda = conteo.idxmax()
        frecuencia = conteo.max()
        return valor_moda, frecuencia

    def calcular_menos_frecuente(self):
        conteo = self.datos.value_counts()
        valor_menos = conteo.idxmin()
        frecuencia_menos = conteo.min()
        return valor_menos, frecuencia_menos

    def calcular_frecuencia(self):
        frec_abs = self.datos.value_counts()
        frec_rel = round(frec_abs / self.n, 3)
        tabla = pd.DataFrame({
            "Frecuencia absoluta": frec_abs,
            "Frecuencia relativa": frec_rel
        })
        return tabla

    #  Gráfico de pastel
    def grafico_pastel(self):
        frec_abs = self.datos.value_counts()
        plt.figure(figsize=(6,6))
        plt.pie(frec_abs, labels=frec_abs.index, autopct='%1.1f%%', startangle=90)
        plt.title(f"Distribución de {self.nombre} (Gráfico de pastel)")
        plt.show()

    #  Gráfico de barras simples
    def grafico_barras(self):
        frec_abs = self.datos.value_counts()
        plt.figure(figsize=(7,5))
        plt.bar(frec_abs.index, frec_abs.values)
        plt.title(f"Distribución de {self.nombre} (Gráfico de barras)")
        plt.xlabel(self.nombre)
        plt.ylabel("Frecuencia absoluta")
        plt.show()

    #  Gráfico de frecuencias absolutas
    def grafico_frecuencia_absoluta(self):
        tabla = self.calcular_frecuencia()
        plt.figure(figsize=(7,5))
        plt.bar(tabla.index, tabla["Frecuencia absoluta"])
        plt.title(f"Frecuencias absolutas de {self.nombre}")
        plt.xlabel(self.nombre)
        plt.ylabel("Frecuencia absoluta")
        plt.show()

    #  Gráfico de frecuencias relativas
    def grafico_frecuencia_relativa(self):
        tabla = self.calcular_frecuencia()
        plt.figure(figsize=(7,5))
        plt.bar(tabla.index, tabla["Frecuencia relativa"], color="orange")
        plt.title(f"Frecuencias relativas de {self.nombre}")
        plt.xlabel(self.nombre)
        plt.ylabel("Frecuencia relativa")
        plt.show()



colores = ["Rojo", "Azul", "Rojo", "Verde", "Azul", "Rojo", "Azul", "Verde", "Verde", "Rojo"]
var_color = VariableCualitativa("Color favorito", colores)

print(var_color.calcular_frecuencia())
print("Moda:", var_color.calcular_moda())
print("Menos frecuente:", var_color.calcular_menos_frecuente())

var_color.grafico_pastel()
var_color.grafico_barras()
var_color.grafico_frecuencia_absoluta()
var_color.grafico_frecuencia_relativa()

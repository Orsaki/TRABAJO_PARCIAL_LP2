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

#### FATI #####
    
    def exportar_frecuencias(self, nombre_archivo="frecuencias.csv"):
        """Guarda la tabla de frecuencias en un archivo CSV"""
        tabla = self.calcular_frecuencia()
        tabla.to_csv(nombre_archivo)
        print(f"✅ Tabla de frecuencias guardada en {nombre_archivo}")


    def tabla_frecuencia_ordenada(self):
        """Devuelve la tabla de frecuencias ordenada de mayor a menor"""
        tabla = self.calcular_frecuencia()
        return tabla.sort_values(by="Frecuencia absoluta", ascending=False)


    def porcentaje_categoria(self, categoria):
        """Devuelve el porcentaje de una categoría específica"""
        if categoria in self.datos.values:
            conteo = self.datos.value_counts(normalize=True) * 100
            print(f"La categoría '{categoria}' representa el {round(conteo[categoria], 2)}% del total.")
            return round(conteo[categoria], 2)
        else:
            print(f"⚠️ La categoría '{categoria}' no existe en los datos.")
            return None

    def tabla_frecuencia_acumulada(self):
        """Devuelve una tabla con frecuencias acumuladas"""
        tabla = self.calcular_frecuencia()
        tabla["Frecuencia absoluta acumulada"] = tabla["Frecuencia absoluta"].cumsum()
        tabla["Frecuencia relativa acumulada"] = tabla["Frecuencia relativa"].cumsum().round(3)
        return tabla





    def resumen(self):
                """Muestra un resumen completo de la variable cualitativa"""
                print(f"\n📊 Resumen de la variable: {self.nombre}")
                print(f"Cantidad de datos: {self.n}")
                print(f"Número de categorías: {self.datos.nunique()}")
                moda, frec_moda = self.calcular_moda()
                menos, frec_menos = self.calcular_menos_frecuente()
                print(f"Categoría más frecuente: {moda} ({frec_moda} veces)")
                print(f"Categoría menos frecuente: {menos} ({frec_menos} veces)")
                print("\nTabla de frecuencias:")
                print(self.calcular_frecuencia())
                print("\n📊 Tabla ordenada por frecuencia:")
                print(self.tabla_frecuencia_ordenada())
                print("\n💾 Si deseas guardar los datos, usa:")
                print("var_color.exportar_frecuencias('mi_tabla.csv')")
                print("\n📈 Tabla con frecuencias acumuladas:")
                print(self.tabla_frecuencia_acumulada())


















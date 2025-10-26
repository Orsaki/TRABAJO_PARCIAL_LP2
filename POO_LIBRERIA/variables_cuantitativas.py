import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
class Variable:
    def __init__(self, datos, nombre=None):
        """
        Constructor flexible que acepta listas, Series de Pandas, etc.
        Si se pasa una Serie de Pandas, su nombre se usa automáticamente.
        
        Args:
            datos (list, pd.Series): La colección de datos a analizar.
            nombre (str, optional): Nombre para la variable. Si es None,
                                    se infiere de la Serie de Pandas.
        """
        if isinstance(datos, pd.Series) and nombre is None:
            # Si es una Serie y no se dio un nombre, usamos el de la 
            self.nombre = datos.name if datos.name is not None else "Sin Nombre"
        elif nombre is not None:
            # Si el usuario da un nombre, ese tiene prioridad
            self.nombre = nombre
        else:
            # Si son datos sin nombre (como una lista), asignamos uno 
            self.nombre = "Sin Nombre"
            # los datos lo pasamos a pandas con series
        if not isinstance(datos, pd.Series):
            datos = pd.Series(datos)
            
        self.datos = datos.dropna() 
        self.tipo = self.detectar_tipo()
        self.n = len(self.datos)

    def detectar_tipo(self):
        try:
            self.datos.astype(float)
            return "cuantitativa"
        except ValueError:
            return "cualitativa"

class VariableCuantitativa(Variable):
    """
    Heredamos de la clase Variable toda su información 
    """
    def __init__(self, datos, nombre=None):
        super().__init__(datos, nombre=nombre)

        if self.tipo != "cuantitativa":
            raise TypeError(f"La variable '{self.nombre}' no parece ser cuantitativa.")
        
        # Convertimos la Serie de Pandas a una lista de Python para los cálculos
        self.datos = self.datos.astype(float).tolist()

    
    def media(self):
        if self.n == 0: return 0
        return sum(self.datos) / self.n

    def varianza(self, es_muestra=True):
        if es_muestra and self.n < 2: return 0
        if not es_muestra and self.n < 1: return 0
        
        media_val = self.media()
        suma_cuadrados = sum((x - media_val) ** 2 for x in self.datos)
        
        return suma_cuadrados / (self.n - 1) if es_muestra else suma_cuadrados / self.n

    def desviacion_estandar(self, es_muestra=True):
        return math.sqrt(self.varianza(es_muestra))

    def mediana(self):
        if self.n == 0: return 0
        datos_ordenados = sorted(self.datos)
        indice_medio = self.n // 2
        
        if self.n % 2 == 1:
            return datos_ordenados[indice_medio]
        else:
            return (datos_ordenados[indice_medio - 1] + datos_ordenados[indice_medio]) / 2

    def percentil(self, p):
        if not 0 <= p <= 100:
            raise ValueError("El percentil debe estar entre 0 y 100.")
        if self.n == 0: return 0

        datos_ordenados = sorted(self.datos)
        indice = (p / 100) * (self.n - 1)
        
        if indice.is_integer():
            return datos_ordenados[int(indice)]
        else:
            indice_bajo = int(indice)
            indice_alto = indice_bajo + 1
            fraccion = indice - indice_bajo
            return datos_ordenados[indice_bajo] + (datos_ordenados[indice_alto] - datos_ordenados[indice_bajo]) * fraccion
            
    def rango(self):
        if self.n == 0: return 0
        return max(self.datos) - min(self.datos)
    
    def coeficiente_variacion(self):
        media_val = self.media()
        if media_val == 0: return float('inf')
        return (self.desviacion_estandar() / abs(media_val)) * 100
    
    def asimetria(self):

        if self.n < 3: return 0 # No está bien definida para pocos datos
        media_val = self.media()

        std_dev = self.desviacion_estandar(es_muestra=False)
        if std_dev == 0: return 0
        
        tercer_momento = sum(((x - media_val) / std_dev) ** 3 for x in self.datos)
        return (self.n / ((self.n - 1) * (self.n - 2))) * tercer_momento # Corrección de sesgo muestral

    def curtosis(self):
        if self.n < 4: return 0 # No está bien definida para pocos datos
        media_val = self.media()
        std_dev = self.desviacion_estandar(es_muestra=False)
        if std_dev == 0: return 0
        # Suma del cuarto momento estandarizado
        cuarto_momento = sum(((x - media_val) / std_dev) ** 4 for x in self.datos)
        # Se resta 3 para que una distribución normal tenga curtosis de 0 (exceso de curtosis)
        return (cuarto_momento / self.n) - 3
    
    def cuartiles(self):
        """
        Calcula el primer cuartil (Q1), el segundo (Q2, la mediana) y el tercer cuartil (Q3).
        """
        q1 = self.percentil(25)
        q2 = self.mediana()
        q3 = self.percentil(75)
        return {'Q1': q1, 'Q2': q2, 'Q3': q3}
    
    def rango_intercuartil(self):
        """
        Calcula el Rango Intercuartílico (IQR = Q3 - Q1).
        """
        cuartiles = self.cuartiles()
        return cuartiles['Q3'] - cuartiles['Q1']

    def graficar_histograma(self, bins='auto'):
        plt.hist(self.datos, bins=bins, edgecolor='black', alpha=0.7)
        plt.title(f'Histograma de {self.nombre}')
        plt.xlabel('Valores')
        plt.ylabel('Frecuencia')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def graficar_boxplot(self):
        plt.boxplot(self.datos, vert=False, patch_artist=True)
        plt.title(f'Diagrama de Caja de {self.nombre}')
        plt.xlabel('Valores')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()
        
    def resumen(self):
    print(f"--- Resumen Estadístico para '{self.nombre}' ---")
    print(f"Número de datos: {self.n}")
    print(f"Media: {self.media():.2f}")
    print(f"Mediana: {self.mediana():.2f}")
    print(f"Desviación Estándar: {self.desviacion_estandar():.2f}")
    print(f"Varianza: {self.varianza():.2f}")
    print(f"Percentil 25 (Q1): {self.percentil(25):.2f}")
    print(f"Percentil 75 (Q3): {self.percentil(75):.2f}")
    print(f"Rango: {self.rango():.2f}")
    print(f"Asimetría: {self.asimetria():.2f}")
    print(f"Curtosis: {self.curtosis():.2f}")
    print("-----------------------------------------")
-


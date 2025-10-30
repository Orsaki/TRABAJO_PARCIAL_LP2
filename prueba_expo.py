import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math 

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

    def __str__(self):
        """
        Representación en string del objeto, mostrando un resumen conciso.
        """
        return (f"VariableCuantitativa(nombre='{self.nombre}', n={self.n}, "
                f"media={self.media():.2f}, std={self.desviacion_estandar():.2f})")

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
    
    def rango_intercuartilico(self):
        """
        Calcula el Rango Intercuartílico (IQR = Q3 - Q1).
        """
        cuartiles = self.cuartiles()
        return cuartiles['Q3'] - cuartiles['Q1']
    
    def detectar_atipicos(self):
        """
        Identifica valores atípicos leves usando el método del IQR.

        Returns:
            dict: Un diccionario con listas de valores atípicos inferiores y superiores.
        """
        cuartiles = self.cuartiles()
        iqr = self.rango_intercuartilico()
        
        limite_inferior = cuartiles['Q1'] - 1.5 * iqr
        limite_superior = cuartiles['Q3'] + 1.5 * iqr
        
        atipicos_inf = [x for x in self.datos if x < limite_inferior]
        atipicos_sup = [x for x in self.datos if x > limite_superior]
        
        return {'inferiores': atipicos_inf, 'superiores': atipicos_sup}
    
    def resumen(self):
        """
        Imprime un resumen estadístico completo y formateado de la variable.
        """
        print(f"========== Resumen Estadístico: {self.nombre} ==========")
        print(f"Registros Válidos:      {self.n}")
        print("---------------------------------------------")
        print(f"Media:                    {self.media():.4f}")
        print(f"Mediana (Q2):             {self.mediana():.4f}")
        print("---------------------------------------------")
        print(f"Desviación Estándar:      {self.desviacion_estandar():.4f}")
        print(f"Varianza:                 {self.varianza():.4f}")
        print(f"Rango:                    {self.rango():.4f}")
        print(f"Rango Intercuartílico:    {self.rango_intercuartilico():.4f}")
        print("---------------------------------------------")
        print(f"Asimetría:                {self.asimetria():.4f}")
        print(f"Curtosis:                 {self.curtosis():.4f}")
        print("---------------------------------------------")
        
        cuartiles = self.cuartiles()
        print(f"Mínimo:                   {min(self.datos) if self.n > 0 else 0:.4f}")
        print(f"Cuartil 1 (Q1 - 25%):     {cuartiles.get('Q1', 0):.4f}")
        print(f"Cuartil 3 (Q3 - 75%):     {cuartiles.get('Q3', 0):.4f}")
        print(f"Máximo:                   {max(self.datos) if self.n > 0 else 0:.4f}")
        print("---------------------------------------------")

        atipicos = self.detectar_atipicos()
        if atipicos['inferiores'] or atipicos['superiores']:
            print("Valores Atípicos:         Detectados")
            if atipicos['inferiores']:
                print(f"  - Inferiores: {atipicos['inferiores']}")
            if atipicos['superiores']:
                print(f"  - Superiores: {atipicos['superiores']}")
        else:
            print("Valores Atípicos:         No detectados")

        print("======================================================")
class VisualizadorEstadistico:
    """
    Clase dedicada exclusivamente a crear visualizaciones estadísticas
    a partir de un objeto de análisis de variables.
    """
    def __init__(self, variable: VariableCuantitativa):
        """
        El constructor recibe el objeto con los datos y cálculos.
        
        Args:
            variable (VariableCuantitativa): El objeto de análisis que se va a visualizar.
        """
        if not isinstance(variable, VariableCuantitativa):
            raise TypeError("Se requiere un objeto de tipo VariableCuantitativa.")
        self.variable = variable

    def graficar_histograma(self, bins='auto'):
        """Genera un histograma de la variable."""
        plt.hist(self.variable.datos, bins=bins, edgecolor='black', alpha=0.7)
        plt.title(f'Histograma de {self.variable.nombre}')
        plt.xlabel('Valores')
        plt.ylabel('Frecuencia')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def graficar_boxplot(self):
        """Genera un diagrama de caja de la variable."""
        plt.boxplot(self.variable.datos, vert=False, patch_artist=True)
        plt.title(f'Diagrama de Caja de {self.variable.nombre}')
        plt.xlabel('Valores')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()
        
# Clase cualitativas
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

    def tabla_frecuencia_alfabetica(self): ###### SE TIENE QUE LLAMAR MANUALMENTE, YA QUE ES UN CÓDIGO PERSONALIZADO
        """Ordena la tabla de frecuencias alfabéticamente por categoría"""
        tabla = self.calcular_frecuencia()
        return tabla.sort_index() 


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
                print("\n💾 Si deseas guardar los datos, usa:")
                print("var_color.exportar_frecuencias('mi_tabla.csv')")
                print("\n📈 Tabla con frecuencias acumuladas:")
                print(self.tabla_frecuencia_acumulada())


    def exportar_resumen(self, nombre_archivo="resumen_variable.txt"):
        """Guarda el resumen completo de la variable en un archivo .txt"""
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(f"📊 Resumen de la variable: {self.nombre}\n")
            f.write(f"Cantidad de datos: {self.n}\n")
            f.write(f"Número de categorías: {self.datos.nunique()}\n")
    
            moda, frec_moda = self.calcular_moda()
            menos, frec_menos = self.calcular_menos_frecuente()
            f.write(f"Categoría más frecuente: {moda} ({frec_moda} veces)\n")
            f.write(f"Categoría menos frecuente: {menos} ({frec_menos} veces)\n\n")
    
            f.write("📋 Tabla de frecuencias:\n")
            f.write(str(self.calcular_frecuencia()) + "\n\n")
    
            f.write("🔠 Tabla de frecuencias ordenada alfabéticamente:\n")
            f.write(str(self.tabla_frecuencia_alfabetica()) + "\n\n")
    
        print(f"✅ Resumen exportado correctamente en '{nombre_archivo}'")


#### Visualizador de Gráficos ### - CUALITATIVA

class VisualizadorCualitativo:
    """
    Clase dedicada exclusivamente a generar visualizaciones para variables cualitativas.
    """
    def __init__(self, variable: VariableCualitativa):
        """
        Constructor que recibe el objeto cualitativo para graficar.
        
        Args:
            variable (VariableCualitativa): El objeto de tipo VariableCualitativa que se va a visualizar.
        """
        if not isinstance(variable, VariableCualitativa):
            raise TypeError("Se requiere un objeto de tipo VariableCualitativa.")
        self.variable = variable

    def graficar_pastel(self):
        """Genera un gráfico de pastel para visualizar los porcentajes de cada categoría."""
        tabla = self.variable.calcular_frecuencia()
        plt.figure(figsize=(6, 6))
        plt.pie(
            tabla["Frecuencia absoluta"],
            labels=tabla.index,
            autopct='%1.1f%%',
            startangle=90
        )
        plt.title(f"Distribución de {self.variable.nombre}")
        plt.show()

    def graficar_barras(self):
        """Genera un gráfico de barras con las frecuencias absolutas."""
        tabla = self.variable.calcular_frecuencia()
        plt.figure(figsize=(7, 5))
        plt.bar(tabla.index, tabla["Frecuencia absoluta"], color="skyblue", edgecolor="black")
        plt.title(f"Frecuencia absoluta de {self.variable.nombre}")
        plt.xlabel("Categorías")
        plt.ylabel("Frecuencia absoluta")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

#########################################################
ruta = r"C:\Users\ASUS\Desktop\archivo_prueba.txt"
df = pd.read_csv(ruta)

variable_prueba = Variable(df["Estado_Civil"])
estado_civil = VariableCualitativa(df["Estado_Civil"],"estado civil")

estado_civil.grafico_frecuencia_absoluta()
estado_civil.grafico_frecuencia_relativa()
estado_civil.exportar_frecuencias()
estado_civil.porcentaje_categoria("Soltero")
estado_civil.tabla_frecuencia_acumulada()
estado_civil.tabla_frecuencia_alfabetica()
estado_civil.resumen()
estado_civil.exportar_resumen()
graficador = VisualizadorCualitativo(estado_civil)
graficador.graficar_pastel()
graficador.graficar_barras()

variable2 = Variable(df["Ingreso_Mensual"])
type(variable2)
ingreso = VariableCuantitativa(df["Ingreso_Mensual"])
graficador = VisualizadorEstadistico(ingreso)
graficador.graficar_histograma()
graficador.graficar_boxplot()
ingreso.resumen()
print(estado_civil.tabla_frecuencia_alfabetica())

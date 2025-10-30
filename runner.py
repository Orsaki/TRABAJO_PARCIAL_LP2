
import pandas as pd
import math
import matplotlib.pyplot as plt
import POO_LIBRERIA.libreria_completa as mi_libreria
df = pd.read_csv("archivo_prueba.txt")

#inyectamos las librerias 
mi_libreria.pd = pd
mi_libreria.math = math
mi_libreria.plt = plt
variable = mi_libreria.Variable(df["Estado_Civil"])
print(variable.tipo)
variable_cuali = mi_libreria.VariableCualitativa(df["Estado_Civil"],"Estado_civil")
# Grafico variables cualis
visualizador=mi_libreria.VisualizadorCualitativo(variable_cuali)
#visualizador.graficar_barras()
# calcular moda 
print(variable_cuali.calcular_moda())
print(variable_cuali.calcular_frecuencia())
# Creo mi variable2 con la clase padre 
variable2 = mi_libreria.Variable(df["Altura"])
# Para detectar el tipo de variable
variable2.detectar_tipo #Vemos que es cuantitativa
variable_cuanti = mi_libreria.VariableCuantitativa(df["Altura"], "Altura")
grafico = mi_libreria.VisualizadorEstadistico(variable_cuanti)
#grafico.graficar_boxplot()
print(variable_cuanti.media())

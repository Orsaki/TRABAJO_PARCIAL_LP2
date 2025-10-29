import pandas as pd
import math
from POO_LIBRERIA.variables_cuantitativas import VariableCuantitativa
from POO_LIBRERIA.variables_cuantitativas import VisualizadorEstadistico

df = pd.read_csv('archivo_prueba.txt')
datos_ingreso = df['Ingreso_Mensual']
print(datos_ingreso.head(6))

statitics = VariableCuantitativa(datos_ingreso)

# Probando algunas estadísticas creadas

print(f"La media es: {statitics.media():.2f}")
print(f"La mediana es: {statitics.mediana():.2f}")
print(f"La desviación estándar es: {statitics.desviacion_estandar():.2f}")

print(f"Resumen Estadistico completo es:{statitics.resumen():.2f}")
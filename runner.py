
import pandas as pd
import math
import matplotlib.pyplot as plt
import POO_LIBRERIA.libreria_completa as mi_libreria


mi_libreria.pd = pd
mi_libreria.math = math
mi_libreria.plt = plt

df = pd.read_csv("archivo_prueba.txt")

try:
    print("\n--- Probando VariableCuantitativa (Columna: Ingreso_Mensual) ---")
    
    datos_ingreso = df['Ingreso_Mensual']

    var_ingreso = mi_libreria.VariableCuantitativa(datos=datos_ingreso)
    print(var_ingreso) 
    media_calculada = var_ingreso.media()
    mediana_calculada = var_ingreso.mediana()
    
    print(f"La Media es: {media_calculada:.2f}")
    print(f"La Mediana es: {mediana_calculada}")

    # Gráficos Cuantitativos 
    visualizador_ingreso = mi_libreria.VisualizadorEstadistico(var_ingreso)
    print("\nMostrando gráficos cuantitativos (Histograma y Caja)...")
    visualizador_ingreso.graficar_histograma()
    visualizador_ingreso.graficar_boxplot()

except Exception as e:
    print(f"Error en la prueba cuantitativa: {e}")



try:
    print("\n--- Probando VariableCualitativa (Columna: Preferencia) ---")
    
    datos_preferencia = df['Preferencia']
    
    var_preferencia = mi_libreria.VariableCualitativa(datos_preferencia, "Preferencia")

    
    var_preferencia.resumen()
    
    var_preferencia.porcentaje_categoria("Tecnología")

    #  Gráficos Cualitativos 
    visualizador_preferencia = mi_libreria.VisualizadorCualitativo(var_preferencia)
    print("\nMostrando gráficos cualitativos (Pastel y Barras)...")
    visualizador_preferencia.graficar_pastel()
    visualizador_preferencia.graficar_barras()

except Exception as e:
    print(f"Error en la prueba cualitativa: {e}")



# TRABAJO PARCIAL DE LENGUAJE DE PROGRAMACIÓN 2
# Universidad Nacional Agraria La Molina
<img src="https://www.lamolina.edu.pe/portada/html/acerca/escudos/download/color/1193x1355_ESCUDOCOLOR.png" alt="UNALM" width="150"/>



**Profesora:** Ana Cecilia Vargas Paredes  

**Integrantes:**  
**- Lázaro Medina, Pamela Stacey**  
**- Montes Yato, Mónica Fátima Del Rosario**  
**- Huamayalli Soto, Luis Alberto**  
**- Ormeño Sakihama, Daniel Kenyi**  

**Descripción del proyecto:**  

Este proyecto consiste en el desarrollo de una librería en Python orientada a objetos (POO) para el análisis de variables cualitativas y cuantitativas. Incluye la creación de clases que permiten calcular medidas estadísticas, generar tablas de frecuencias, graficar resultados y exportar la información obtenida. El trabajo busca aplicar los conceptos de encapsulamiento, herencia y métodos en un contexto práctico y funcional.

**Métodos creados en nuestra libreria:** 

**Variable cualitativa:**

- calcular_moda(): Devuelve el valor más repetido y su frecuencia

- calcular_menos_frecuente(): Devuelve el valor menos repetido y su frecuencia

- calcular_frecuencia(): Devuelve la tabla con todos los valores y sus frecuencias absoluta y relativa

- grafico_pastel(): Devuelve el grafico de pastel en porcentaje de la variable

- grafico_frecuencia_absoluta(): Devuelve grafico de frecuencia absoluta de una variable

- grafico_frecuencia_relativa(): Devuelve grafico de frecuencia relativa de una variable

- tabla_frecuencia_acumulada(): Muestra las frecuencias absolutas y relativas acumuladas.

- porcentaje_categoria(categoria): Indica el porcentaje que representa una categoría específica dentro de los datos.

- exportar_frecuencias(nombre_archivo="frecuencias.csv"): Exporta la tabla de frecuencias a un archivo CSV.

- resumen(): Muestra un resumen general con información de categorías, modas y tablas de frecuencias (normal, ordenada y acumulada).

**Variable cuantitativa:**
En esta sección explicaremos lo que desarrollamos de forma colaborativa para hacer nuestra presentación del proyecto final.  

**Funciones creadas**

**Medidas de tendencia central**

- media() : Es una medida de tendencia central, que calcula el promedio de un conjunto de datos.

- mediana() : Es una medida que nos da información del valor central de un conjunto de datos **ordenados**.
 
**Medida de posición**

- percentil() : Es una medida estadística que indica el valor por debajo del cual se encuentra un determinado porcentaje de datos, una vez que estos han sido ordenados de menor a mayor. 

**Medida de dispersión**

- rango() : Es una medida de dispersión en estadística que representa la diferencia entre el valor más alto y el más bajo de un conjunto de datos.

- varianza() : Es una medida de dispersion que nos da informacion de la variabilidad de los datos respecto a la media. 

- desviacion_estandar(): Es una medida de dispersion, que es la raiz cuadrada positiva de la varianza. 

- rango_intercuartilico() : calcula el rango intercuartilico "IQR = Q3 - Q1

- coeficiente_variacion() : Es una medida estadística de dispersión relativa que compara la desviación estándar con la media aritmética de un conjunto de datos.

**Medida de forma**

- asimetria() : Es una medida de forma que indica si una distribución de datos es simétrica o no con respecto a la media.

- curtosis() : Es una medida que describe el grado de forma o aplanamiento de una distribución. 

**Gráficos**

- detectar_atipicos() : identifica valores atípicos leves usando el método del IQR / Return: un diccionario con listas de valores 
atípicos inferiores y superiores.

- resumen(): imprime un resumen estadístico completo y formateado.

- graficar_histograma() : General un histograma.

- graficar_boxplot() : Genera un diagrama de caja.

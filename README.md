# Fishbiotools
Fishbiotools es un paquete de Python diseñado para facilitar el análisis y procesamiento de datos relacionados con la biología de peces. Este paquete incluye módulos para:

Procesar archivos Excel: Manejo de datos morfológicos mediante transposición, renombrado de columnas, filtrado, transformaciones y más.
Analizar archivos GenBank: Evaluación de mitogenomas en peces, cálculo de métricas (longitud, contenido GC, cantidad de 'N', etc.) y generación de reportes y gráficos.
Procesar archivos ZIP: Renombrado y extracción de archivos ZIP según su contenido, organizándolos en carpetas específicas.

## Requisitos
Para utilizar Fishbiotools es necesario tener instaladas las siguientes dependencias:

Python 3.x
- Pandas
- NumPy
- Openpyxl (para manejo de archivos Excel)
- BioPython (para análisis de archivos GenBank)
- Matplotlib (para la generación de gráficos)
- Shutil y Zipfile (módulos estándar de Python)

## Uso
### Procesamiento de archivos Excel
El módulo Fishbiotools_morfo.py permite:

Cargar un archivo Excel.
Transponer datos.
Renombrar la primera columna.
Eliminar filas con datos no numéricos.
Dividir valores por una columna específica.
Multiplicar valores por 100.
Aplicar transformaciones logarítmicas.

### Análisis de archivos GenBank
El módulo mitogenome_int.py permite analizar archivos GenBank (.gbk) para extraer información relevante del mitogenoma, como:

Longitud del genoma.
Contenido GC.
Número y porcentaje de 'N'.
Componentes genéticos encontrados y ausentes.
Generación de un reporte de texto y de un histograma en PDF.


### Procesamiento de archivos ZIP
El módulo zip_iterator.py permite:

Renombrar archivos ZIP en función del contenido (por ejemplo, usando el nombre del primer archivo .gbk encontrado).
Extraer y categorizar archivos contenidos en ZIP en carpetas específicas.

## Script de prueba interactivo
Se incluye un script de prueba interactivo, prueba_fishbiotools.py, que permite ejecutar de forma interactiva las funciones de cada módulo. Para usarlo, simplemente ejecuta:

El script solicitará:

La ruta del archivo Excel y la operación a realizar.
La carpeta que contiene archivos GenBank (.gbk) y la opción de generar reportes y gráficos.
La carpeta que contiene archivos ZIP para su procesamiento.

## Licencia
Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Autores
Daniel Alfredo Gomez Chavarria - Paula Gudiela Orrego Suarez

## Notas
Este paquete fue desarrollado con fines académicos y puede ser modificado y distribuido bajo los términos de la Licencia MIT.

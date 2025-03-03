import pandas as pd
import numpy as np

def cargar_archivo(archivo):
    """Carga un archivo de Excel y lo devuelve como un DataFrame."""
    try:
        df = pd.read_excel(archivo, engine="openpyxl")
        print("Archivo cargado exitosamente. Primeras filas:")
        print(df.head())
        return df
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado. Verifique la ruta e inténtelo nuevamente.")
        return None
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None

def transponer_archivo(df, output_filename='archivo_transpuesto.xlsx'):
    """Transpone el DataFrame y guarda el resultado en un archivo Excel."""
    df_transpuesto = df.set_index(df.columns[0]).T
    df_transpuesto.to_excel(output_filename, index=True)
    print(f"Archivo después de la transposición guardado como: {output_filename}")

def renombrar_primera_columna(df, nuevo_nombre='Muestras', output_filename='archivo_renombrado.xlsx'):
    """Renombra la primera columna del DataFrame y guarda el resultado."""
    df.rename(columns={df.columns[0]: nuevo_nombre}, inplace=True)
    df.to_excel(output_filename, index=True)
    print(f"Archivo después de renombrar la primera columna guardado como: {output_filename}")

def eliminar_filas_no_numericas(df, output_filename='archivo_sin_filas_invalidas.xlsx'):
    """Elimina filas con datos no numéricos, excepto la primera columna."""
    df = df[df.drop(columns='Muestras', errors='ignore').apply(
        lambda x: pd.to_numeric(x, errors='coerce')).notnull().all(axis=1)]
    df.to_excel(output_filename, index=False)
    print(f"Archivo después de eliminar filas con datos no numéricos guardado como: {output_filename}")

def dividir_por_columna(df, columna=1, output_filename='_archivo_dividido_por_columna.xlsx'):
    """Divide cada valor de la fila por el valor de la columna especificada."""
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda row: row / row.iloc[columna-1], axis=1)
    df.to_excel(output_filename, index=True)
    print(f"Archivo después de dividir por la columna {columna} guardado como: {output_filename}")

def multiplicar_por_100(df, output_filename='_archivo_multiplicado_por_100.xlsx'):
    """Multiplica todos los valores por 100, excepto la primera fila y columna."""
    df.iloc[:, 1:] = df.iloc[:, 1:] * 100
    df.to_excel(output_filename, index=False)
    print(f"Archivo después de multiplicar por 100 guardado como: {output_filename}")

def aplicar_logaritmo(df, output_filename='archivo_logaritmo_aplicado.xlsx'):
    """Aplica el logaritmo natural a todas las celdas excepto la primera fila y columna."""
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: np.log(x) if np.issubdtype(x.dtype, np.number) and np.isfinite(x).all() else x)
    df.to_excel(output_filename, index=False)
    print(f"Archivo después de aplicar el logaritmo natural guardado como: {output_filename}")

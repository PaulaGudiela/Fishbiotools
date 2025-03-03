import os

# Importación de los módulos del paquete Fishbiotools
import Fishbiotools.Fishbiotools_morfo as fbm
import Fishbiotools.mitogenome_int as mitogenome
import Fishbiotools.zip_iterator as zip


def procesar_excel():
    archivo = input("Por favor, ingrese el nombre o la ruta del archivo Excel: ")
    df = fbm.cargar_archivo(archivo)
    if df is not None:
        print("\nSeleccione la operación a realizar:")
        print("1. Transponer archivo")
        print("2. Renombrar primera columna")
        print("3. Eliminar filas no numéricas")
        print("4. Dividir por columna")
        print("5. Multiplicar por 100")
        print("6. Aplicar logaritmo")
        opcion = input("Ingrese el número de la operación: ")
        if opcion == "1":
            salida = input("Ingrese el nombre del archivo de salida para la transposición: ")
            fbm.transponer_archivo(df, salida)
            print(f"Proceso completado. Archivo guardado como: {salida}")
        elif opcion == "2":
            nuevo_nombre = input("Ingrese el nuevo nombre para la primera columna: ")
            salida = input("Ingrese el nombre del archivo de salida para renombrar: ")
            fbm.renombrar_primera_columna(df, nuevo_nombre, salida)
            print(f"Proceso completado. Archivo guardado como: {salida}")
        elif opcion == "3":
            salida = input("Ingrese el nombre del archivo de salida para eliminar filas no numéricas: ")
            fbm.eliminar_filas_no_numericas(df, salida)
            print(f"Proceso completado. Archivo guardado como: {salida}")
        elif opcion == "4":
            columna = input("Ingrese el número de la columna a utilizar para dividir: ")
            salida = input("Ingrese el nombre del archivo de salida para dividir: ")
            try:
                columna_int = int(columna)
                fbm.dividir_por_columna(df, columna_int, salida)
                print(f"Proceso completado. Archivo guardado como: {salida}")
            except ValueError:
                print("El número de columna debe ser un entero.")
        elif opcion == "5":
            salida = input("Ingrese el nombre del archivo de salida para multiplicar por 100: ")
            fbm.multiplicar_por_100(df, salida)
            print(f"Proceso completado. Archivo guardado como: {salida}")
        elif opcion == "6":
            salida = input("Ingrese el nombre del archivo de salida para aplicar logaritmo: ")
            fbm.aplicar_logaritmo(df, salida)
            print(f"Proceso completado. Archivo guardado como: {salida}")
        else:
            print("Opción no reconocida.")
    else:
        print("No se pudo cargar el archivo Excel.")
    print("\n--- Fin de la prueba de Excel ---\n")


def procesar_gbk():
    carpeta_gbk = input("Ingrese la ruta a la carpeta que contiene los archivos .gbk: ")
    if os.path.isdir(carpeta_gbk):
        gbk_files = [os.path.join(carpeta_gbk, f) for f in os.listdir(carpeta_gbk) if f.endswith(".gbk")]
        if not gbk_files:
            print("No se encontraron archivos .gbk en la carpeta.")
        else:
            results = []
            for archivo_gbk in gbk_files:
                resultado = mitogenome.analyze_genbank_file(archivo_gbk)
                results.append(resultado)
                print(f"\nResultado para {archivo_gbk}:")
                print(resultado)

            # Preguntar si se desea generar el reporte de texto
            resp_report = input("\n¿Desea generar un reporte de texto? (s/n): ")
            if resp_report.lower() == "s":
                salida = input("Ingrese el nombre base para el reporte de texto (sin extensión): ")
                output_report = f"{salida}_report.txt"
                mitogenome.generate_report(results, output_report)
                print(f"Reporte generado: {output_report}")
            else:
                print("Reporte de texto omitido.")

            # Preguntar si se desea generar el histograma en PDF
            resp_hist = input("\n¿Desea generar un histograma en PDF? (s/n): ")
            if resp_hist.lower() == "s":
                salida = input("Ingrese el nombre base para el histograma (sin extensión): ")
                # Calcular los conteos para determinar completos e incompletos
                completos_count = sum(
                    1 for res in results if res["Counts"].get("rRNA", 0) == 2 and res["Counts"].get("CDS", 0) == 13)
                incompletos_count = len(results) - completos_count
                output_hist = f"{salida}_histogram.pdf"
                mitogenome.generate_histogram_pdf(completos_count, incompletos_count, output_hist)
                print(f"Histograma generado: {output_hist}")
            else:
                print("Histograma omitido.")
    else:
        print("La carpeta especificada no existe.")

    input("\nPresione Enter para volver al menú principal...")
    print("\n--- Fin del análisis de archivos GenBank ---\n")


def procesar_zip():
    carpeta_zip = input("Ingrese la ruta a la carpeta que contiene los archivos ZIP: ")
    if os.path.isdir(carpeta_zip):
        print("\nRenombrando archivos ZIP...")
        zip.rename_zip_files(carpeta_zip)
        print("Extrayendo y categorizando archivos de los ZIP...")
        zip.extract_and_categorize(carpeta_zip)
        print("Proceso completado para archivos ZIP.")
    else:
        print("La carpeta especificada no existe.")
    print("\n--- Fin del procesamiento de archivos ZIP ---\n")


def main():
    print("==== Prueba del paquete Fishbiotools ====")
    while True:
        print("\nSeleccione la opción a ejecutar:")
        print("1. Procesar archivo Excel (Fishbiotools_morfo)")
        print("2. Analizar archivos GenBank (.gbk) (mitogenome_int)")
        print("3. Procesar archivos ZIP (zip_iterator)")
        print("4. Salir")
        opcion = input("Ingrese el número de la opción: ")
        if opcion == "1":
            procesar_excel()
        elif opcion == "2":
            procesar_gbk()
        elif opcion == "3":
            procesar_zip()
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()

import os
import argparse
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import matplotlib.pyplot as plt

# Lista de secuencias esperadas en mitogenomas de peces
expected_genes = {
    "rRNA": ["12S rRNA", "16S rRNA"],
    "CDS": ["ND1", "ND2", "ND3", "ND4", "ND4L", "ND5", "ND6", "COXI", "COXII", "COXIII", "ATPase6", "ATPase8", "Cytb"],
    "tRNA": [f"tRNA-{x}" for x in [
        "Phe", "Val", "Leu", "Ile", "Gln", "Met", "Trp", "Ala", "Asn", "Cys", "Tyr", "Ser", "Asp", "Lys", "Gly",
        "Arg", "His", "Thr", "Pro", "Glu", "Ser", "Thr"
    ]],
    "D_loop": ["D-loop"]
}

# Función para analizar cada archivo GenBank
def analyze_genbank_file(file_path):
    result = {
        "File": file_path,
        "Genome Length (bp)": 0,
        "GC Content (%)": 0.0,
        "N Count": 0,
        "N Percentage (%)": 0.0,
        "Components": {},
        "Counts": {},
        "tRNA Count Difference": 0,
        "Missing Genes": {}
    }

    try:
        record = SeqIO.read(file_path, "genbank")
        sequence = str(record.seq).upper()
        result["Genome Length (bp)"] = len(sequence)
        result["GC Content (%)"] = round(gc_fraction(record.seq) * 100, 2)

        # Cálculo de la cantidad y porcentaje de 'N' (considerando mayúsculas y minúsculas)
        n_count = sequence.count('N') + sequence.count('n')
        result["N Count"] = n_count
        result["N Percentage (%)"] = round((n_count / len(sequence)) * 100, 2) if len(sequence) > 0 else 0.0

        for category in expected_genes:
            result["Components"][category] = []
            result["Counts"][category] = 0
            result["Missing Genes"][category] = set(expected_genes[category])

        for feature in record.features:
            if feature.type in expected_genes:
                gene_name = feature.qualifiers.get("gene") or feature.qualifiers.get("product")
                if gene_name:
                    gene_name = gene_name[0].strip()
                    if gene_name in expected_genes[feature.type]:
                        location = feature.location
                        start = int(location.start) + 1
                        end = int(location.end)
                        length = abs(end - start + 1)
                        strand_label = "+" if location.strand == 1 else "-"
                        result["Components"][feature.type].append({
                            "Gene": gene_name,
                            "Start": start,
                            "End": end,
                            "Length": length,
                            "Strand": strand_label
                        })
                        result["Counts"][feature.type] += 1
                        result["Missing Genes"][feature.type].discard(gene_name)

        if result["Counts"].get("tRNA", 0) != 22:
            result["tRNA Count Difference"] = result["Counts"]["tRNA"] - 22

    except Exception as e:
        print(f"Error procesando {file_path}: {e}")

    return result

# Función para generar el reporte de texto
def generate_report(results, output_path):
    completos = [res for res in results if res["Counts"].get("rRNA", 0) == 2 and res["Counts"].get("CDS", 0) == 13]
    incompletos = [res for res in results if res not in completos]

    with open(output_path, "w") as report:
        report.write(f"Mitogenomas completos ({len(completos)}):\n")
        report.write("\n".join(os.path.basename(res['File']) for res in completos) + "\n\n")

        report.write(f"Mitogenomas incompletos ({len(incompletos)}):\n")
        report.write("\n".join(os.path.basename(res['File']) for res in incompletos) + "\n")

        report.write("\n" + "=" * 40 + "\n\n")

        for result in results:
            report.write(f"Archivo: {os.path.basename(result['File'])}\n")
            report.write(f"Longitud del Genoma (bp): {result['Genome Length (bp)']}\n")
            report.write(f"Contenido GC (%): {result['GC Content (%)']}\n")
            report.write(f"Numero de 'N': {result['N Count']} ({result['N Percentage (%)']}%)\n")
            report.write("Componentes encontrados:\n")

            for category, genes in result["Components"].items():
                expected_count = len(expected_genes[category])
                found_count = result["Counts"][category]
                report.write(f"  {category}: Esperados: {expected_count}. Encontrados: {found_count}.\n")
                for gene_info in genes:
                    report.write(
                        f"    {gene_info['Gene']}: Start={gene_info['Start']}, End={gene_info['End']}, "
                        f"Length={gene_info['Length']}, Strand={gene_info['Strand']}\n"
                    )

            if result["tRNA Count Difference"] != 0:
                report.write(f"Diferencia en el numero de tRNA: {result['tRNA Count Difference']}\n")

            for category in ["CDS", "rRNA", "D_loop"]:
                missing = result["Missing Genes"].get(category, [])
                if missing:
                    report.write(f"Faltan los siguientes genes en {category}: {', '.join(missing)}\n")

            report.write("\n" + "=" * 40 + "\n\n")

    print(f"Reporte de texto generado: {output_path}")

# Función para generar el histograma en PDF con valores sobre las barras
def generate_histogram_pdf(completos_count, incompletos_count, output_pdf):
    categorias = ["Completos", "Incompletos"]
    valores = [completos_count, incompletos_count]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(categorias, valores, color=["#4CAF50", "#F44336"])
    plt.title("Resumen de Completitud de Mitogenomas")
    plt.ylabel("Número de archivos")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    for bar, valor in zip(bars, valores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, str(valor),
                 ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_pdf)
    plt.close()

    print(f"Histograma generado: {output_pdf}")

# Función principal con argparse
def main():
    parser = argparse.ArgumentParser(description="Analisis de integridad de mitogenomas en archivos GenBank.")
    parser.add_argument("carpeta_entrada", help="Ruta a la carpeta con archivos .gbk")
    parser.add_argument("--reporte_texto", choices=["T", "F"], default="F", help="Generar reporte de texto (T/F)")
    parser.add_argument("--reporte_grafico", choices=["T", "F"], default="F", help="Generar reporte gráfico en PDF (T/F)")
    parser.add_argument("--salida", default="reporte_mitogenomas", help="Nombre base para los archivos de salida")

    args = parser.parse_args()

    if not os.path.isdir(args.carpeta_entrada):
        print(f"La carpeta de entrada no existe: {args.carpeta_entrada}")
        return

    gbk_files = [f for f in os.listdir(args.carpeta_entrada) if f.endswith(".gbk")]
    if not gbk_files:
        print("No se encontraron archivos .gbk en la carpeta especificada.")
        return

    results = [analyze_genbank_file(os.path.join(args.carpeta_entrada, file_name)) for file_name in gbk_files]

    completos_count = sum(1 for res in results if res["Counts"].get("rRNA", 0) == 2 and res["Counts"].get("CDS", 0) == 13)
    incompletos_count = len(results) - completos_count

    if args.reporte_texto == "T":
        text_report_path = f"{args.salida}_report.txt"
        generate_report(results, text_report_path)

    if args.reporte_grafico == "T":
        graph_report_path = f"{args.salida}_histogram.pdf"
        generate_histogram_pdf(completos_count, incompletos_count, graph_report_path)

if __name__ == "__main__":
    main()


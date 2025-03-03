import os
import zipfile
import shutil
import argparse


def rename_zip_files(directory):
    for file in os.listdir(directory):
        if file.endswith(".zip"):
            zip_path = os.path.join(directory, file)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                gbk_files = [f for f in zip_ref.namelist() if f.endswith(".gbk")]
            if gbk_files:
                new_name = os.path.splitext(os.path.basename(gbk_files[0]))[0] + ".zip"
                new_path = os.path.join(directory, new_name)
                os.rename(zip_path, new_path)
                print(f"Renamed: {file} -> {new_name}")


def extract_and_categorize(directory):
    categories = {
        ".NCBI.txt": "NCBI_files",
        ".pdf": "images_pdf",
        "_genes.fa": "genes_fa",
        ".gbk": "gbk_files",
        ".log": "log_files",
        ".txt": "summary_files",
        ".fa": "seqs_fa"
    }

    for folder in categories.values():
        os.makedirs(os.path.join(directory, folder), exist_ok=True)

    for file in os.listdir(directory):
        if file.endswith(".zip"):
            zip_path = os.path.join(directory, file)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    category = next(
                        (folder for key, folder in categories.items() if member.endswith(key)), None
                    )

                    if category:
                        dest_path = os.path.join(directory, category, os.path.basename(member))
                        with zip_ref.open(member) as source, open(dest_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
                        print(f"Extracted: {member} -> {category}")


def main():
    parser = argparse.ArgumentParser(description="Iterate and extract categorized files from ZIP archives.")
    parser.add_argument("directory", help="Path to the directory containing ZIP files.")
    args = parser.parse_args()

    directory = args.directory
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    rename_zip_files(directory)
    extract_and_categorize(directory)


if __name__ == "__main__":
    main()

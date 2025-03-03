from setuptools import setup, find_packages

setup(
    name='Fishbiotools',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy' , 'pandas', 'Bio','zipfile', 'shutil', 'os', 'argparse', 'matplotlib'
    ],
    description='Paquete para análisis biológicos, enfocado en peces. Las funciones dentro de Fishbiotools_morfo constan de'
                'funciones enfocadas en tablas con datos de morfometria las cuales  estandarizan, filtran y transforman. Las funciones en zip_iterator logran separar las partes de un zip en diferentes carpetas y mitogenome logra hacer un análisis de integridad de las secuencias descargadas', 
    author='Paula Gudiela Orrego Suarez - Daniel Alfredo Gomez Chavarria',
    author_email='porregos@unal.edu.co','dgomezch@unal.edu.co' # Tu email
   
)

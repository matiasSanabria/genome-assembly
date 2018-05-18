# Ensamblado de Genomas
## Instalación de dependencias del SO
	sudo apt-get install python-tk python-dev virtualenv
	python -mpip install matplotlib

## Crear entorno virtual y activar
	virtualenv myenv
	source myenv/bin/activate

## Instalación de dependencias de python 2.7
	pip install -r requirements.txt

## Ejecutar el ensamblador
	python main.py <nombre_archivo.fa> <tamanho_kmeros>

## Ejemplos

### Ejemplo teórico basico para demostrar que funciona correctamente
    python main.py data/reads_long_long.fa 4
    python main.py data/reads_abc.fa 3

## Entrada del profesor
    python main.py data/reads_phix_1.fastq 25

## Ejemplo de ensamblamiento con un resultado ya en data/result10K.fasta
    python main.py data/read50x_ref10K_e001.fasta 25

## Archivos de salida
    output/contig.fa
    output/graph.png
    output/informe.html

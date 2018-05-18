import debruijn as db
import sys
import time

# Compute location from command line arguments
if len(sys.argv) < 3:
    print "python main.py read_file_name.fa k-mer-length"
    print "example: python main.py data/g200reads.fa 8"
    sys.exit()

start = time.time()

fname = sys.argv[1]
print "nombre del archivo", fname
kmer = int(sys.argv[2])
print "tamanho del kmero", kmer

output_location = "output/"

# verifica la extension de la entrada (fasta, fastq)
if not fname.lower().endswith(('.fasta', '.fa', '.fastq')) :
    print "Entrada validas solamente .fasta, .fa, .fastq"
    sys.exit()

# en caso de que sea fastq se hace una conversion temporal a fasta
if fname.lower().endswith('.fastq'):
        f = open(fname, 'r')
        lines = f.readlines() # cantidad de lineas
        f.close()
        reads = []

        linea = 1
        for line in lines:
            if linea ==2:
                reads = reads + [line.rstrip()]
                linea = linea + 1
            else:
                linea = linea + 1
                if linea == 5: linea = 1
        # guardamos en un archivo temporal
        fname = "data/reads_temp.fa"
        archivo = open(fname,"w")
        print "\nSe esta convirtiendo la entrada fastq a fasta"
        archivo.write('\n'.join(reads))
        archivo.close()


# 1 lee archivo
reads = db.read_reads(fname)
#print reads

graph = db.construct_graph(reads, kmer)
db.print_graph(graph)
#print graph

contig = db.output_contigs(graph)
print "\nContig: ",contig

# guardar el Contig
# contig = "> Contig: \n" + contig
archivo = open(output_location + "contig.fa","w")
print "\nUbicacion del Contig: " + output_location + "contig.fa"
archivo.write(contig)
archivo.close()

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Tiempo total(hh:mm:ss):  {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

# crea el informe del analisis
html = '''<style>
* {
background-color: white;
}
</style>
<center><h1>Ensamblado de Genoma</h1></br>
<img src="graph.png" style="width:100%;"></center><br>
<b>Tiempo de procesamiento (hh:mm:ss):
'''
html = html + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
html = html + "</b></br><b><p>Contig:</p><textarea rows='20' cols='160' style=width:100%; height:20rem;>""" + contig + "</textarea></b></br><p><br>Longitud del contig: "+ str(len(contig)) +"</br></p>"
archivo = open(output_location + "informe.html","w")
print "\nUbicacion del Contig: " + output_location + "informe.html"
archivo.write(str(html))
archivo.close()

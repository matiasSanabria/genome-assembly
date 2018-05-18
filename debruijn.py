import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Node:
    """ Class Node para representar un vertice en el grafico de bruijn """
    def __init__(self, lab):
        self.label = lab
        self.indegree = 0
        self.outdegree = 0

class Edge:
    def __init__(self, lab):
        self.label = lab

def read_reads(fname):
    """ Read short reads in FASTA format. It is assumed that one line in the input file correspond to one read. """
    f = open(fname, 'r')
    lines = f.readlines()
    f.close()
    reads = []

    for line in lines:
        if line[0] != '>':
            reads = reads + [line.rstrip()]

    return reads

def construct_graph(reads, k):
    """ Construir el grafo de bruijn a partir de un conjunto de reads con una longitud k """
    edges = dict()
    vertices = dict()

    for read in reads:
        i = 0
        while i+k < len(read):
            v1 = read[i:i+k]
            v2 = read[i+1:i+k+1]
            if v1 in edges.keys():
                vertices[v1].outdegree += 1
                edges[v1] += [Edge(v2)]
            else:
                vertices[v1] = Node(v1)
                vertices[v1].outdegree += 1
                edges[v1] = [Edge(v2)]
            if v2 in edges.keys():
                vertices[v2].indegree += 1
            else:
                vertices[v2] = Node(v2)
                vertices[v2].indegree += 1
                edges[v2] = []
            i += 1

    return (vertices, edges)

def output_contigs(g):
    """ Perform searching for Eulerian path in the graph to output genome assembly"""
    V = g[0]
    E = g[1]
    # Pick starting node (the vertex with zero in degree)
    start = V.keys()[0]
    for k in V.keys():
        if V[k].indegree < V[start].indegree:
            start = k

    contig = start
    current = start
    while len(E[current]) > 0:
        # Pick the next node to be traversed (for now, at random)
        next = E[current][0]
        del E[current][0]
        contig += next.label[-1]
        current = next.label

    return contig

def print_graph(g):
    """ Print the information in the graph to be (somewhat) presentable """
    V = g[0] # lista de nodos
    E = g[1] # lista de aristas
    # print "nodos totales " + str(V)
    # print "aristas totales " + str(E)
    G = nx.Graph()
    for k in V.keys():
        print "\nNodo:", V[k].label, "\nAristas entrantes: ", V[k].indegree, "\tAristas salientes (grado): ", V[k].outdegree
        print "Aristas salientes que apuntan a nodo: "
        for e in E[k]:
            print e.label
            G.add_edges_from([(V[k].label, e.label)])

    pos = nx.spring_layout(G)
    plt.figure(3, figsize=(13,13))
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 10)
    # nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='r', arrows=True)
    nx.draw_networkx_edges(G, pos, arrows=False)
    plt.savefig("output/graph.png")

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:17:26 2022

@author: tidiane
"""
import networkx as netx
import matplotlib.pyplot as plt

#import fctGetCsv 
#fctGetCsv.getCsv()

G = netx.Graph()

# Algorithme:
    
"""
récupération liste passée en paramètre
1 - parcours liste et construction noeuds
variables: liste_edges avec poids = délai tache

1.1 : pour chaque noeud: l'ajouter au graphe
1.2 : pour chaque noeud: déterminer son prédécesseur et rajouter un arc
1.3 : pour chaque arc, identifier le noeud de départ et déterminer la durée de la tache
    
"""


G.add_nodes_from([
    ('A', {"color": "red"}),
    ('B', {"color": "green"}),
])
G.add_edge('A','B',weight=5.0)
G.add_edge(4,5, weight=3.0)
netx.draw(G, with_labels=True, font_weight='bold')


DG = netx.DiGraph()
DG.add_weighted_edges_from([(1, 2, 0.5), (3, 1, 0.75)])
netx.draw(DG, with_labels=True, font_weight='bold')

#G = netx.petersen_graph()

#subax1 = plt.subplot(121)
#netx.draw(G, with_labels=True, font_weight='bold')

#subax2 = plt.subplot(122)
#netx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

#fctGetCsv.getCsv()
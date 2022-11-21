# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:17:26 2022

@author: tidiane
"""


#Import librairie networkx : alias = netx

import networkx as netx
G = netx.Graph()

#ajout de noeud
G.add_node(1)

#ajout de noeuds avec code couleur

G.add_nodes_from([
    (2, {"color": "red"}),
    (3, {"color": "green"}),
])
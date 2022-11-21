# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:17:26 2022

@author: tidiane
"""


#Import librairie networkx : alias = netx

import networkx as netx
import matplotlib.pyplot as plt

G = netx.petersen_graph()
subax1 = plt.subplot(121)
netx.draw(G, with_labels=True, font_weight='bold')
subax2 = plt.subplot(122)
netx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
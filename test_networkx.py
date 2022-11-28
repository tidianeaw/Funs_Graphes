# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:17:26 2022

@author: tidiane
"""

# import modules
import networkx as netx
DG = netx.DiGraph()

import matplotlib.pyplot as plt

# récup liste

liste_brute = []
liste_brute.append(['A','5','',''])
liste_brute.append(['B','3','',''])
liste_brute.append(['C','4','',''])
liste_brute.append(['D','4','A',''])
liste_brute.append(['E','5','B',''])
liste_brute.append(['F','2','C',''])
liste_brute.append(['G','2','E,D',''])
liste_brute.append(['H','4','E,F',''])
#print(liste_brute)

#reconstruction liste pour noeuds simples
list_rebuilt = []
#list_rebuilt.append(["Debut",0,''])
for i in range(len(liste_brute)):
    (tache_en_cours, delai, predec, option) = liste_brute[i]
    if len(predec) == 0:
        list_rebuilt.append([tache_en_cours, delai, 'Debut'])
    else:
        predecesseurs = predec.split(',')
        for j in range(len(predecesseurs)):
            list_rebuilt.append([tache_en_cours, delai, predecesseurs[j]])
  
# identification taches de fin de projet            
list_sans_suivants = []
for k in range(len(list_rebuilt)):
    aucun_suivant = True
    for s in range(len(list_rebuilt)):
        if list_rebuilt[k][0] == list_rebuilt[s][2]:
            aucun_suivant = False
    if aucun_suivant == True:        
        list_sans_suivants.append(list_rebuilt[k][0])

#suppression doublons eventuels
list_sans_suivants = list(set(list_sans_suivants))
for l in range(len(list_sans_suivants)):
    list_rebuilt.append(['Fin', 0, list_sans_suivants[l]])
    
#print(list_sans_suivants)       
#print("\n")
#print(list_rebuilt)


for m in range(len(list_rebuilt)): 
    #préparation noeud
    tache_prec = list_rebuilt[m][2]
    tache_suiv = list_rebuilt[m][0]
    
    #poids = int (list_rebuilt[m][1])
    
    #ajout de l'arc avec les noeuds
    DG.add_edge(tache_prec, tache_suiv, label=list_rebuilt[m][1])
    
#positionnement affichage
pos = netx.spring_layout(DG)

#dessin du réseau
netx.draw_networkx(DG, pos)

#intégration labels
netx.draw_networkx_edge_labels(DG, pos, edge_labels=netx.get_edge_attributes(DG,'label'))

#affichage final
plt.show()
 
#
#Question 3
#
#liste taches par niveaux
l = netx.single_source_shortest_path_length(DG,'Debut');
#print(l);
#liste_taches = l.keys()
#liste_niveaux = l.values()

nb_niveaux = len(set(l.values()))
#print (nb_niveaux)

taches_triees_par_niveau = list()
for i in range(nb_niveaux):
    tasks = []
    for key in l:
        if (l[key] == i):
            tasks.append(key)
    taches_triees_par_niveau.append(tasks)

print(taches_triees_par_niveau)
#print(len(taches_triees_par_niveau))

#predecesseurs

#x=[1,2,3,4,5,6,7,8]
#y=[1,2,3,4,5,6,7,8]

#plt.plot(x,y)
#plt.xlabel("Niveaux taches")

#plt.show()

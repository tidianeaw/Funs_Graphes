# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:17:26 2022

@author: Ahmed - Shahram
"""
######################################################
# Question 2
######################################################
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
######################################################
#Question 3
######################################################
#liste taches par niveaux
l = netx.single_source_shortest_path_length(DG,'Debut');
nb_niveaux = len(set(l.values()))

taches_triees_par_niveau = list()

for i in range(nb_niveaux):
    tasks = []
    for key in l:
        if (l[key] == i):
            tasks.append(key)
    taches_triees_par_niveau.append(tasks)

#print(taches_triees_par_niveau)
#print(len(taches_triees_par_niveau))

# reprise donnees graphe précédent
old_edge_labels = netx.get_edge_attributes(DG,'label')

G = netx.DiGraph()
G.add_nodes_from(DG.nodes)
G.add_edges_from(DG.edges, label=old_edge_labels)

#calcul positions selon le niveau
#initialisation positions
posit = dict()
pos_y = 0
pos_x = 0

#calcul position noeud debut
succ_0 = len(list(DG.successors("Debut")))
prec_0 = len(list(DG.predecessors("Debut")))

posit['Debut'] = (pos_x, 2*succ_0-2)
pos_x = 2

#parcours excluant les noeuds Debut et Fin
for i in range(1, len(taches_triees_par_niveau)-1):
    taches_niveau_i = taches_triees_par_niveau[i]
    pos_y = 0
    
    #pour chaque niveau
    for j in range(0, len(taches_niveau_i)):
        
        #calcul successeurs, prédécesseurs + position X
        cpt_success = len(list(DG.successors(taches_niveau_i[j])))
        cpt_predec = len(list(DG.predecessors(taches_niveau_i[j])))
                    
        if (cpt_predec == 0):
            pos_y = pos_y + cpt_success - 1
        else:
            pos_y = pos_y + cpt_predec + 1
        
        position = [pos_x, pos_y]        
        posit[taches_niveau_i[j]] = position
    
    #deplacement x
    pos_x = pos_x + 2
    
#calcul position noeud fin
succ_1 = 0
prec_1 = len(list(DG.predecessors("Fin")))
posit['Fin'] = (pos_x, 2*prec_1)

#edge labels: délais
pos = netx.spring_layout(G)
netx.set_edge_attributes(G, old_edge_labels, 'label')
#print(netx.get_edge_attributes(G,'label'))

#nouveau graphe
netx.draw_networkx(G, pos=posit, with_labels = True, arrows=True) 
netx.draw_networkx_edge_labels(G, pos, edge_labels=old_edge_labels,label_pos=0.5,font_color='red')

plt.title("Taches par niveau")
plt.show()

#
#Question 4: Affichage Graph
#


#
#Question 5: Calcul marges et battement
#
#initialisations
dates_battement = dict()
#noeud - fin plus tot - fin plus tard - battement
nodes = list(G.nodes)
edges = G.edges
edge_attr = netx.get_edge_attributes(G, 'label')
#print(nodes)
#print(edges)
#print (edge_attr)
#parcours noeuds et calcul dates fin au plus tôt
for i in range(len(nodes)):
    #pour chaque noeud calcul date au plus tôt
    earliest_date = 0
    latest_date = 0
    battement = 0
    
    noeud_en_cours = nodes[i]
    
    incoming_nodes = list(G.predecessors(noeud_en_cours))
    #print(incoming_nodes)
    if len(incoming_nodes) == 0:
        dates_battement[noeud_en_cours] = [0, 0, 0]
    else:        
        for j in range(len(incoming_nodes)):
            edge_data = G.get_edge_data(incoming_nodes[j], noeud_en_cours)
            delai = int(edge_data['label'])
            delai = delai + dates_battement[incoming_nodes[j]][0]
            if (delai > earliest_date):
                earliest_date = delai
                    
        dates_battement[noeud_en_cours] = [earliest_date, 0, 0]


#parcours inverse noeuds et calcul date fin au plus tard
for w in reversed(nodes):
    
    if (str(w) == 'Debut'):
        dates_battement['Debut'] = [0,0,0]
    else:
        data_en_cours = dates_battement[w]
        fin_plus_tot = data_en_cours[0]
        
        suivantes = list(G.successors(w))
        if (len(suivantes) == 0):        
            fin_plus_tard = fin_plus_tot
            battement = fin_plus_tard - fin_plus_tot
            dates_battement[w] = [fin_plus_tot, fin_plus_tard, battement]
        else:
            for m in range(len(suivantes)):
                fin_plus_tard = fin_plus_tot
                edge_data = G.get_edge_data(w, suivantes[m])
                delai = int(edge_data['label'])
                
                delai = dates_battement[suivantes[m]][1] - delai
                if (delai > fin_plus_tard):
                    fin_plus_tard = delai
                 
                battement = fin_plus_tard - fin_plus_tot
                dates_battement[w] = [fin_plus_tot, fin_plus_tard, battement]

print("Dates battement par tâche")
print(dates_battement)

print("\n")

#
#Question 6: determination chemin critique
#
chemin_critique = []
for key,val in dates_battement.items():
    if (val[2] == 0):
        chemin_critique.append(key)
print("Chemin critique du projet: ")
print(chemin_critique)

print("\n")

#
#Question 7: réalisation GANTT
#
taches = []
critique = []
durees = []
fin_ptot = []
delai_debut = []
preced = []

for key,val in dates_battement.items():
    taches.append(key)
    
    crit = 'blue'
    if (val[2] == 0):
        crit= 'red'
    critique.append(crit)
    
    duree_tache = 0
    predec = ''
    for j in range(len(liste_brute)):
        if (liste_brute[j][0] == key):
            duree_tache = int(liste_brute[j][1])
            predec = liste_brute[j][2]
    
    durees.append(duree_tache)
    preced.append(predec)
    
    fin_plus_tot = val[0]
    fin_ptot.append(fin_plus_tot)
    
    delai_deb = fin_plus_tot - duree_tache
    delai_debut.append(delai_deb)
        


import pandas as pd
#import numpy as np
#import matplotlib
import matplotlib.pyplot as plt2
#import datetime as dt

df = pd.DataFrame(
    {'tache' : taches,                  
      'duree' : durees,
      'fin_plus_tot': fin_ptot,
      'delai_debut' : delai_debut,
      'preced' : preced,
      'critique' : critique}
    )

#print(df)

plt2.barh(y=df['tache'], width=df['duree'], left=df['delai_debut'], color=df['critique'])
plt.gca().invert_yaxis()
plt2.show()
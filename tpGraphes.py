# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:43:56 2022

@Author: Ahmed & Shahram
@Group: FCTI 22-23
@Org: IMT Nord Europe
"""

#
#import des bonnes librairies
#
#networkx pour la génération de graphes
import networkx as netx
#pyplot pour l'affichage de graphes
import matplotlib.pyplot as plt
#pandas pour la gestion des datagrids
import pandas as pda
#


#import des fonctions développées
import fctGetCsv

 
class tpGraphes:
    #attributs: fichier CSV et liste initiale des taches du projet
    fichierCsv = ''
    listeTaches = []
    cheminCritique = []    
    
    #constructeur et initialisation attributs principaux
    def __init__(self, csvFile, taches):
        self.fichierCsv = csvFile
        self.listeTaches = taches
        self.cheminCritique = []
    
    #message utilisateur
    def work(self):
        print(f'Working with {self.fichierCsv} ')
        
    #question 1 - construction liste tâches dans le format adéquat
    def buildTaskList(self):       
        print("Liste des tâches du projet: ")
        [print(ligne) for ligne in self.listeTaches]
        print("\n")
    
    
    #question 2 - Récup matrice des données et création graphe correspondant.
    def buildGraph(self):
        print("Question 2")
        
        #initialisation du graphe
        DG = netx.DiGraph()
        
        #reconstruction liste pour noeuds simples
        list_rebuilt = []
        #list_rebuilt.append(["Debut",0,''])
        for i in range(len(self.listeTaches)):
            (tache_en_cours, delai, predec, option) = self.listeTaches[i]
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
            

        for m in range(len(list_rebuilt)): 
            #préparation noeud
            tache_prec = list_rebuilt[m][2]
            tache_suiv = list_rebuilt[m][0]
            
            #ajout de l'arc avec les noeuds
            DG.add_edge(tache_prec, tache_suiv, label=list_rebuilt[m][1])
         
        #print(list_rebuilt)    

        #positionnement affichage
        pos = netx.spring_layout(DG)

        #dessin du réseau
        netx.draw_networkx(DG, pos)

        #intégration labels
        netx.draw_networkx_edge_labels(DG, pos, edge_labels=netx.get_edge_attributes(DG,'label'))

        #affichage final
        plt.show()
        
        return DG
 


    #question 3 - Graphe par niveau de tâches
    def buildGraphByTaskLevel(self, DG):
        print("Question 3")
        
        #liste taches par niveaux
        l = netx.single_source_shortest_path_length(DG,'Debut');
        #nb niveaux
        nb_niveaux = len(set(l.values()))

        #tri par niveau
        taches_triees_par_niveau = list()

        for i in range(nb_niveaux):
            tasks = []
            for key in l:
                if (l[key] == i):
                    tasks.append(key)
            taches_triees_par_niveau.append(tasks)

        # reprise donnees graphe précédent, notamment les delais
        old_edge_labels = netx.get_edge_attributes(DG,'label')

        #on dessine notre nouveau graphe par niveau
        G = netx.DiGraph()
        G.add_nodes_from(DG.nodes)
        G.add_edges_from(DG.edges, label=old_edge_labels)

        #calcul positions selon le niveau
        #initialisation positions
        posit = dict()
        #pos_y: en ordonnée, pos_x en abscisse
        #glissement vers la droite
        pos_y = 0
        pos_x = 0

        #calcul position noeud debut
        succ_0 = len(list(DG.successors("Debut")))
        #prec_0 = len(list(DG.predecessors("Debut")))
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
        #succ_1 = 0
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
        
        return G


    #question 4 - Affichage de graphe
    def showGraph(self, option):
        print("Question 4")
        plt.show()
 

    #question 5 - calcul marges et battement
    def computeMarginAndFlapping(self, G):
        print("Question 5")
    
        #initialisations
        dates_battement = dict()
        #structure: noeud - fin plus tot - fin plus tard - battement
        nodes = list(G.nodes)
        #edges = G.edges
        #edge_attr = netx.get_edge_attributes(G, 'label')

        #parcours noeuds et calcul dates fin au plus tôt
        for i in range(len(nodes)):
            #pour chaque noeud calcul date au plus tôt
            earliest_date = 0
            #latest_date = 0
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
        return (dates_battement)
    
    
    #question 6 - calcul et affichage du chemin critique du projet
    def computeCriticalPath(self, dates_battement):
        print("Question 6")
    
        chemin_critique = []
        for key,val in dates_battement.items():
            if (val[2] == 0):
                chemin_critique.append(key)
        print("Chemin critique du projet: ")
        print(chemin_critique)
        print("\n")
        
        return chemin_critique
   
    
   
    #question 7 - affichage diagramme de Gantt
    def buildAndShowGantt(self, dates_battement):
        print("Question 7")
        
        taches = []
        critique = []
        durees = []
        fin_ptot = []
        delai_debut = []
        preced = []
        
        #calcul delais début selon données fournies
        for key,val in dates_battement.items():
            taches.append(key)
            
            crit = 'blue'
            if (val[2] == 0):
                crit= 'red'
            critique.append(crit)
            
            duree_tache = 0
            predec = ''
            for j in range(len(self.listeTaches)):
                if (self.listeTaches[j][0] == key):
                    duree_tache = int(self.listeTaches[j][1])
                    predec = self.listeTaches[j][2]
            
            durees.append(duree_tache)
            preced.append(predec)
            
            fin_plus_tot = val[0]
            fin_ptot.append(fin_plus_tot)
            
            delai_deb = fin_plus_tot - duree_tache
            delai_debut.append(delai_deb)
        
        #Grille de données Pandas
        df = pda.DataFrame(
            {'tache' : taches,                  
              'duree' : durees,
              'fin_plus_tot': fin_ptot,
              'delai_debut' : delai_debut,
              'preced' : preced,
              'critique' : critique}
            )

        #print(df)
        
        #création et affichage GANTT
        plt.barh(y=df['tache'], width=df['duree'], left=df['delai_debut'], color=df['critique'])
        #inversion en Y pour afficher les taches du haut vers le bas
        plt.gca().invert_yaxis()
        plt.show()
        
        
        
        


#Première etape: interaction avec l'utilisateur
#Demande fichier CSV et stockage données dans les variables filename et taches
(filename, taches) = fctGetCsv.getCsv()

#si nom fichier vide ou liste tâches vide, on ne poursuit pas
if (not filename or not taches):
    print("Le programme ne peut pas se poursuivre: fichier inconnu ou mal structuré")
    exit()
else:
    #on poursuit
    #on crée un objet de la classe tpGraphes
    tp = tpGraphes(filename, taches)
    
    #premier message à l'utilisateur:
    tp.work()
    
    #Question 1
    tp.buildTaskList()
    
    #Question 2
    directedGraph = tp.buildGraph()
    
    #Question 3
    graphByLevel = tp.buildGraphByTaskLevel(directedGraph)
    
    #Question 4
    #Déjà prise en charge dans les questions 2 et 3 
    
    #Question 5
    datesBattement = tp.computeMarginAndFlapping(graphByLevel)
    
    #Question 6
    criticalPath = tp.computeCriticalPath(datesBattement)
    
    #Question 7
    tp.buildAndShowGantt(datesBattement)
    

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
#import biblio pandas pour la gestion des datagrids
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
        
        #initialisation du graphe orienté (Directed Graph)
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
          
        # identification des taches de fin de projet
        # ce sont les taches sans successeur          
        list_sans_suivants = []
        for k in range(len(list_rebuilt)):
            aucun_suivant = True
            for s in range(len(list_rebuilt)):
                if list_rebuilt[k][0] == list_rebuilt[s][2]:
                    aucun_suivant = False
            if aucun_suivant == True:        
                list_sans_suivants.append(list_rebuilt[k][0])

        #suppression doublons eventuels dans la liste des taches sans successeur
        list_sans_suivants = list(set(list_sans_suivants))
        for l in range(len(list_sans_suivants)):
            list_rebuilt.append(['Fin', 0, list_sans_suivants[l]])
            
        #on place les arcs: noeud debut - noeud fin avec comme label le délai
        for m in range(len(list_rebuilt)): 
            #préparation noeuds (depart - arrivée)
            #noeud départ = tache précédente = tache_prec
            #noeud arrivée = tache suivante = tache_suiv
            tache_prec = list_rebuilt[m][2]
            delai_tache = list_rebuilt[m][1]
            tache_suiv = list_rebuilt[m][0]
            
            #ajout de l'arc avec les noeuds (noeuds avec leurs liens + délai tache)
            DG.add_edge(tache_prec, tache_suiv, label=delai_tache)
        
        
        #positionnement affichage
        pos = netx.spring_layout(DG)

        #dessin du réseau avec le graphe orienté à la position indiquée
        netx.draw_networkx(DG, pos)

        #intégration des labels sur les arcs (edges)
        netx.draw_networkx_edge_labels(DG, pos, edge_labels=netx.get_edge_attributes(DG,'label'))

        #affichage final
        plt.title("Taches génériques du projet")
        plt.show()
        
        return DG
 


    #question 3 - Graphe par niveau de tâches
    def buildGraphByTaskLevel(self, DG):
        print("Question 3")
        #premiere methode: emploi des méthodes offertes par netx et plt
        #récupération niveaux et noeuds selon la topologie du graphe
        for niveau, noeuds in enumerate(netx.topological_generations(DG)):
            for noeud in noeuds:
                DG.nodes[noeud]["layer"] = niveau
        
        #affectation des positions des noeuds par niveau
        pos = netx.multipartite_layout(DG,subset_key="layer")
                
        #création figure et jeu de graphes depuis la librairie
        fig, ax = plt.subplots()
        
        #reconstruction graphe par niveau, avec les positions des noeuds par niveau
        #intégration du graphe dans le cadre indiqué
        netx.draw_networkx(DG, pos=pos, ax=ax)
        
        #titre graphe et ajustement dans le cadre défini par la variable figure
        ax.set_title("Affichage graphe par niveau")        
        fig.tight_layout()
        
        #affichage final
        plt.show()
        
        """
        #Deuxieme methode: codage manuel depuis single_source_shortest_path_length
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

        # reprise donnees graphe en parametre, notamment les delais
        old_edge_labels = netx.get_edge_attributes(DG,'label')

        #on dessine notre nouveau graphe orienté par niveau
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
        nb_succ_debut = len(list(DG.successors("Debut")))
        #nb_prec_debut = len(list(DG.predecessors("Debut")))
        posit['Debut'] = (pos_x, 2 * nb_succ_debut - 2)

        pos_x = 2

        #parcours excluant les noeuds Debut et Fin
        for i in range(1, len(taches_triees_par_niveau)-1):
            taches_niveau_i = taches_triees_par_niveau[i]
            pos_y = 0
            
            #pour chaque niveau
            for j in range(0, len(taches_niveau_i)):
                
                #calcul successeurs, prédécesseurs + position X
                nb_success = len(list(DG.successors(taches_niveau_i[j])))
                nb_predec = len(list(DG.predecessors(taches_niveau_i[j])))
                            
                if (nb_predec == 0):
                    pos_y = pos_y + nb_success - 1
                else:
                    pos_y = pos_y + nb_predec + 1
                
                position = [pos_x, pos_y]        
                posit[taches_niveau_i[j]] = position
            
            #deplacement x
            pos_x = pos_x + 2
            
        #calcul position noeud fin
        #nb_succ_fin = 0
        nb_prec_fin = len(list(DG.predecessors("Fin")))
        posit['Fin'] = (pos_x, 2 * nb_prec_fin)

        #labels des arcs: délais
        pos = netx.spring_layout(G)
        netx.set_edge_attributes(G, old_edge_labels, 'label')        

        #nouveau graphe
        netx.draw_networkx(G, pos=posit, with_labels = True, arrows=True) 
        netx.draw_networkx_edge_labels(G, pos, edge_labels=old_edge_labels,label_pos=0.5,font_color='red')

        plt.title("Taches par niveau")
        plt.show()
        
        return G
        """
        return DG


    #question 4 - Affichage de graphe
    def showGraph(self, option):
        print("Question 4")
        plt.show()
 

    #question 5 - calcul marges et battement
    def computeMarginAndFlapping(self, G):
        print("Question 5")
    
        #initialisations
        dates_battement = dict()
        #structure dictionnaire: clé=noeud - valeur=(fin plus tot - fin plus tard - battement)
        nodes = list(G.nodes)

        #parcours noeuds et calcul dates fin au plus tôt
        for i in range(len(nodes)):
            #pour chaque noeud calcul de la date de fin au plus tôt
            earliest_date = 0
            battement = 0
            
            noeud_en_cours = nodes[i]
            
            #noeuds sur un arc entrant vers le noeud en cours
            incoming_nodes = list(G.predecessors(noeud_en_cours))
            
            #si aucun noeud sur un arc entrant, on est sur le noeud de début
            if len(incoming_nodes) == 0:
                dates_battement[noeud_en_cours] = [0, 0, 0]
            else:        
                #il existe des noeuds adjacents à gauche
                for j in range(len(incoming_nodes)):
                    #on récupère les données de l'arc formé avec le noeud en cours
                    edge_data = G.get_edge_data(incoming_nodes[j], noeud_en_cours)
                    delai = int(edge_data['label'])
                    
                    #on rajoute la durée de la tache en amont pour calculer la date de fin au plus tôt                    
                    delai = delai + dates_battement[incoming_nodes[j]][0]
                    
                    #on prend toujours la valeur la plus grande (cf calcul battement en cours)
                    if (delai > earliest_date):
                        earliest_date = delai
                
                #on stocke la paire clé-valeurs dans le dictionnaire
                #clé = tache en cours
                #valeur = [date fin au plus tôt, date fin au plus tard, battement]
                dates_battement[noeud_en_cours] = [earliest_date, 0, 0]


        #parcours inverse noeuds pour le calcul de la date de fin au plus tard
        for w in reversed(nodes):
            #si on est sur le noeud Début, rien à faire - Tout est à 0
            if (str(w) == 'Debut'):
                dates_battement['Debut'] = [0,0,0]
            else:
                #on est sur une tache réelle
                #les données = valeurs (Fin au + tot, Fin au plus tard, Battement)
                data_en_cours = dates_battement[w]
                #stockage de l'info fin au plus tot
                fin_plus_tot = data_en_cours[0]
                
                #on regarde les taches suivantes
                suivantes = list(G.successors(w))
                if (len(suivantes) == 0):
                    #on est sur la tache fin de projet donc Fin +tot = Fin +tard
                    fin_plus_tard = fin_plus_tot
                    #battement = 0
                    battement = fin_plus_tard - fin_plus_tot
                    #on actualise le dictionnaire
                    dates_battement[w] = [fin_plus_tot, fin_plus_tard, battement]
                else:
                    #on est sur une tache réelle
                    for m in range(len(suivantes)):
                        #on initialise fin au plus tard
                        fin_plus_tard = fin_plus_tot
                        #on récupère les données de l'arc associé a la tache w et sa suivante considérée
                        edge_data = G.get_edge_data(w, suivantes[m])
                        delai = int(edge_data['label'])
                        #on recalcule le délai de fin au plus tard
                        delai = dates_battement[suivantes[m]][1] - delai
                        #on prend la plus petite valeur (cf méthode vue en cours)
                        if (delai > fin_plus_tard):
                            fin_plus_tard = delai
                        #on actualise le dictionnaire après calcul du battement 
                        battement = fin_plus_tard - fin_plus_tot
                        dates_battement[w] = [fin_plus_tot, fin_plus_tard, battement]

        print("Dates battement par tâche")
        print(dates_battement)
        print("\n")
        return (dates_battement)
    
    
    #question 6 - calcul et affichage du chemin critique du projet
    def computeCriticalPath(self, dates_battement):
        print("Question 6")
        #le chemin critique est formé d'une liste de noeuds, donc tableau
        chemin_critique = []
        #pour chaque tache, on regarde son battement
        for key,val in dates_battement.items():
            if (val[2] == 0):
                #battement = 0, pas de marge donc tache critique à rajouter au tableau
                chemin_critique.append(key)
        print("Chemin critique du projet: ")
        print(chemin_critique)
        print("\n")        
        return chemin_critique
   
    
   
    #question 7 - affichage diagramme de Gantt
    def buildAndShowGantt(self, dates_battement):
        print("Question 7")
        #on initialise les variables: liste taches, durées, début et fin, criticité
        taches = []
        critique = []
        durees = []
        fin_ptot = []
        delai_debut = []
        preced = []
        
        #calcul delais début selon données fournies
        for key,val in dates_battement.items():
            #tableau des taches
            taches.append(key)
            
            #tache non critique en bleu, tache critique en rouge
            crit = 'blue'
            if (val[2] == 0):
                crit= 'red'
            critique.append(crit)
            
            #on recalcule la durée de la tache
            duree_tache = 0
            predec = ''
            #parcours liste taches et examen des taches précédentes pour chacune
            for j in range(len(self.listeTaches)):
                if (self.listeTaches[j][0] == key):
                    duree_tache = int(self.listeTaches[j][1])
                    predec = self.listeTaches[j][2]
            #on la stocke
            durees.append(duree_tache)
            preced.append(predec)
            
            #fin au plus tot déjà disponible dans le dictionnaire dates_battement
            fin_plus_tot = val[0]
            fin_ptot.append(fin_plus_tot)
            
            #début de la tache = fin au plus tot - sa durée
            delai_deb = fin_plus_tot - duree_tache
            delai_debut.append(delai_deb)
        
        #Grille de données Pandas
        #on stocke dans la grille de données les variables calculées
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
        #en ordonnée: le nom de la tache
        #la largeur de la barre horizontale = duree tache
        #le début de la barre horizontale = délai debut de la tache
        #code couleur criticité pour la couleur de la barre (rouge = critique)
        plt.barh(y=df['tache'], width=df['duree'], left=df['delai_debut'], color=df['critique'])
        
        #inversion en Y pour afficher les taches du haut vers le bas
        plt.gca().invert_yaxis()
        
        #titre du GANTT et affichage final
        plt.title("Diagramme de GANTT du projet")
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
    #on reconstruit la liste des taches dans un format exploitable pour la suite
    tp.buildTaskList()
    
    #Question 2
    #on construit le 1er graphe
    directedGraph = tp.buildGraph()
    
    #Question 3
    #on construit le graphe par niveau
    graphByLevel = tp.buildGraphByTaskLevel(directedGraph)
    
    #Question 4
    #Déjà prise en charge dans les questions 2 et 3 
    
    #Question 5
    #on calcule les marges (fin +tot, fin +tard, battement) pour le graphe en Question 3
    datesBattement = tp.computeMarginAndFlapping(graphByLevel)
    
    #Question 6
    #on détermine le chemin critique pour les dates et le battement trouvés en Q5
    criticalPath = tp.computeCriticalPath(datesBattement)
    
    #Question 7
    #construction et affichage du GANTT pour les dates et le battement trouvés en Q5
    tp.buildAndShowGantt(datesBattement)
    

# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:07:58 2022

@author: Ahmed & Shahram
@Group: FCTI 22-23
@Org: IMT Nord Europe

Demande et récupération fichier CSV
Parsing du fichier CSV
Stockage du contenu dans un tableau
Construction du graphe générique 
A partir du graphe générique, détermination de la liste des taches par niveau
Construction du graphe par niveau
Détermination des marges et battements pour chaque tache
Calcul du chemin critique
Construction du diagramme de GANTT

"""
#
#import des bonnes librairies
#
#networkx pour la génération de graphes
import networkx as netx
#pyplot pour l'affichage de graphes
import matplotlib.pyplot as plt
#random pour les nbres aléatoires
import random as rand
#pour les opérations de tri sur les listes et tableaux
from operator import itemgetter

#import des fonctions développées
import fctGetCsv

class tpDeuxGraphes:
    #attributs: jpeg file - fichiers csv - données brutes positions et liaisons villes
    fichierJpeg = ''
    fichierPositions = ''
    fichierLiaisons = ''
    tbPositions = []
    tbLiaisons = []
    
    #constructeur et initialisation attributs principaux
    def __init__(self, fJpeg, fPositions, fLiaisons, tbP, tbL):
        self.fichierJpeg = fJpeg
        self.fichierPositions = fPositions
        self.fichierLiaisons = fLiaisons
        self.tbPositions = tbP
        self.tbLiaisons = tbL
    
        
    def getfichierPositions(self):
        return self.fichierPositions
    
    def getfichierLiaisons(self):
        return self.fichierLiaisons
    
    #Partie A - Question 1: 
    #Retourner les données fournies sous forme de tableau
    def showPositions(self):
        return self.tbPositions
        
    def showLiaisons(self):
        return self.tbLiaisons
            
    #Partie A - Question 2: 
    #prend en entrée le tableau contenant 
    #les informations du fichier TP2-liaison.csv,
    #retourne le graphe correspondant.
    def buildGraphLiaisons(self):
        #on construit un graphe vide
        G = netx.Graph()
        
        #on parcourt les liaisons et on construit des arcs
                        
        for a in range(len(self.tbLiaisons)):
            #noeuds source et destination
            source = self.tbLiaisons[a][0]
            destination = self.tbLiaisons[a][1]
            
            #type = ce sera une contrainte
            #typeChemin = self.tbLiaisons[a][2]
            
            #print(source+"-"+destination+"-"+typeChemin + "\n")
            
            #paramètres pour l'optimisation: durée ou cout
            #duree = self.tbLiaisons[a][3]
            #cout = self.tbLiaisons[a][4]
            
            #label des arcs            
            #label_arc = typeChemin + " - " + duree + " mn - " + cout + "€"
            
            #on rajoute l'arc                     
            G.add_edge(source, destination, width=6.0)
                                 
        #positionnement affichage
        pos = self.getCityPositions()

        #définition des couleurs selon le type de voie: autoroute=rouge, autres=vert
        cols = []        
        #servira à stocker les couleurs pour le graphe
        #couleurs: autoroute = rouge, departementale = vert
        
        #parcours liste des arcs et recherche du type pour chacun => fixation couleur
        edge_list = G.edges()
        for edge in edge_list:
            src = edge[0]
            dst = edge[1]
            tp = self.getTypeChemin(src, dst)
            col = "r"
            if (tp == "d"):
                col = "g"
            cols.append(col)
           
        #construction du graphe avec les couleurs d'arc attendues
        netx.draw(G, node_color='b', node_size=300, font_size=13, pos=pos, edge_color=cols, width=6, with_labels=True)
                        
        #intégration des labels sur les arcs (edges)
        #netx.draw_networkx_edge_labels(G, pos, font_size=10, edge_labels=netx.get_edge_attributes(G,'label'))
        
        #affichage final        
        plt.title("Liaisons routières en France")
        plt.show()
        
        return G
    
        
    #determiner le type de chemin d'un arc
    def getTypeChemin(self, src, dst):
        tp = "d"
        #graphe non orienté, on considère les 2 options
        #la source et la destination peuvent s'intervertir, le graphe n'est pas orienté
        #parcours jusqu'à découverte des noeuds source et destination        
        for a in range(len(self.tbLiaisons)):
            if (self.tbLiaisons[a][0].strip() == src.strip() and self.tbLiaisons[a][1].strip() == dst.strip()):
                tp = self.tbLiaisons[a][2]
            else:
                if (self.tbLiaisons[a][1].strip() == src.strip() and self.tbLiaisons[a][0].strip() == dst.strip()):
                    tp = self.tbLiaisons[a][2]
        return tp
    
    
    #récupèration des positions des villes
    def getCityPositions(self):
        #on initialise une variable de type dict
        myPos = dict()
        #format: clé=noeud, valeurs=posx, posy
        
        #on parcourt le tableau des positions
        for p in range(len(self.tbPositions)):
            #clé = ville
            key = self.tbPositions[p][0]
            
            #valeur = (pos_x, pos_y)
            #attention au cast
            pos_x = int(self.tbPositions[p][1])
            pos_y = int(self.tbPositions[p][2])
            val = (pos_x,pos_y)
            
            #on rajoute au dictionnaire                        
            myPos.__setitem__(key,val)
        
        return myPos
       
    
    
    #Partie A - Question 3: 
    #prend en entrée le tableau contenant 
    #les informations du fichier TP2-liaison.csv,
    #le chemin vers l’image carte.jpg et le graphe généré, 
    #et affiche le graphe sur la carte de France
    def buildGraphOnMap(self)   :
        #les arcs, noeuds sont créés aux bonnes positions en Q2 buildGraphLiaisons
        
        #on initialise une figure avec comme fond le Jpeg fourni        
        img = plt.imread(self.fichierJpeg)
        
        fig, ax = plt.subplots()
        ax.imshow(img)
        
        #on y rajoute le graphe de Q2 buildGraphLiaisons        
        #intégration du graphe dans le cadre indiqué
        netx.draw_networkx(self.buildGraphLiaisons(), pos=self.getCityPositions(), ax=ax)
                   
        #titre graphe et ajustement dans le cadre défini par la variable figure
        ax.set_title("Affichage graphe - Carte France")        
        fig.tight_layout()
        
        #ajustement de la figure avec les bonnes dimensions
        plt.rcParams["figure.figsize"] = (60,15)
                        
        #affichage final
        plt.show()
        
    #récupérer la durée associée à un chemin
    def getDuree(self, src, dst):
        duree = 0
        #graphe non orienté, on considère les 2 options
        #la source et la destination peuvent s'intervertir
        for a in range(len(self.tbLiaisons)):
            if (self.tbLiaisons[a][0].strip() == src.strip() and self.tbLiaisons[a][1].strip() == dst.strip()):
                duree =int(self.tbLiaisons[a][3])
            else:
                if (self.tbLiaisons[a][1].strip() == src.strip() and self.tbLiaisons[a][0].strip() == dst.strip()):
                    duree = int(self.tbLiaisons[a][3])
        return duree
    
    #récupérer le cout+péage associé à un chemin
    def getCout(self, src, dst):
        cout = 0.00
        #graphe non orienté, on considère les 2 options
        #la source et la destination peuvent s'intervertir
        for a in range(len(self.tbLiaisons)):
            if (self.tbLiaisons[a][0].strip() == src.strip() and self.tbLiaisons[a][1].strip() == dst.strip()):
                cout = float(self.tbLiaisons[a][4])
            else:
                if (self.tbLiaisons[a][1].strip() == src.strip() and self.tbLiaisons[a][0].strip() == dst.strip()):
                    cout = float(self.tbLiaisons[a][4])
        return cout
    
    #Partie B - Question 1: vérifier si un graphe est connexe ou non - avec l'algo de Kruskal
    #Prend en entree un graphe
    #Paramètres:
        #G = graphe à vérifier
        #option = base de calcul du poids: la durée ou le coût+péage des tronçons
    #Retour: 3-uplet (Boolean connexe ou non, Arbre minimal, Poids arbre min)
        #is_connexe = booléen
        #H: schématisation de l'arbre trouvé sur la carte indiquee
        #poids min: poids de l'arbre trouvé
    #Rappel: graphe connexe si pour tout UV, il existe un chemin de U à V
    #Rappel: graphe connexe ssi contient un arbre couvrant (passe par tous les sommets)
    #option: pour travailler avec la durée (1) ou le coût (2)  
    def grapheConnexeKruskal(self,G,option):                          
        #on va construire un arbre
        H = netx.Graph() 
        #autres valeurs de retour
        arbre_trouve = False
        poids_min = 0
        
        #récupération des arcs du graphe fourni = ensemble A
        arcsBase = G.edges()
        
        #construction d'un autre ensemble
        #on rajoute la donnée du poids dans les arcs depuis tbLiaisons
        arcs = []
        for arc in arcsBase:
            (src,dst) = arc
            #récup donnée poids
            if (option == 1):
                #durée
                poids = int(self.getDuree(src, dst))
            else:
                #cout
                poids = float(self.getCout(src, dst))
            
            #rajout de l'item dans notre liste
            newArc=[src,dst,poids]
            arcs.append(newArc)
        
        #tri de la liste des arcs par poids croissant
        edge_list = sorted(arcs, key=itemgetter(2))    
        
        #parcours de la liste triée des arcs
        #on les rajoute un à un: en cas de création de cycle, on saute l'arc
        for j in range(len(edge_list)):            
            #initialisation arc à intégrer à l'arbre
            (noeud1, noeud2, poids)=edge_list[j]                          
            H.add_edge(noeud1, noeud2, weight=poids, width=12.0)
            
            #s'il n'y a pas de cycle, on poursuit
            #sinon on supprime cet arc            
            if netx.cycle_basis(H)!=[]:
                H.remove_edge(noeud1, noeud2)
            else:
                poids_min = poids_min + poids
 
        print("L'arbre couvrant minimal est ", poids_min)
        
        nb_noeuds_arbre_kruskal = len(H.nodes())
        nb_noeuds_graphe_source = len(G.nodes())
        
        #on s'assure que l'arbre passe par tous les noeuds du graphe
        if (nb_noeuds_arbre_kruskal == nb_noeuds_graphe_source):
            arbre_trouve = True
        
        #Retour = 3-uplet: Boolean connexe ou non, Arbre minimal, Poids arbre min
        valeur_retour = (arbre_trouve, H, poids_min)
        
        #on positionne l'arbre sur la carte de France
        img = plt.imread(self.fichierJpeg)        
        fig, ax = plt.subplots()
        ax.imshow(img)
                      
        #intégration du graphe dans le cadre indiqué avec la carte
        netx.draw_networkx(H, pos=self.getCityPositions(), ax=ax, width=6)
                   
        #titre graphe et ajustement dans le cadre défini par la variable figure
        ax.set_title("Arbre couvrant min sur la carte du pays - Kruskal")        
        fig.tight_layout()
        
        #ajustement de la figure avec les bonnes dimensions et affichage de l'arbre
        plt.rcParams["figure.figsize"] = (60,15)                        
        plt.show()
        
        return valeur_retour

        
    ##Partie B - Question 1: vérifier si un graphe est connexe ou non - avec l'algorithme de Prim
    #Détermine avec l'algo de Prim un arbre couvrant minimal pour le graphe en paramètre
    #Paramètres:
        #G = graphe à vérifier
        #option = base de calcul des poids: durée ou coût+péage
    #retour = 3-uplet(arbre_trouve, H, poids_min)
        #is_connexe = booléen
        #H: schématisation de l'arbre trouvé sur la carte indiquee
        #poids min: poids de l'arbre trouvé
    #
    def grapheConnexePrim(self, G, option):
        #
        #On initialise l'algo
        #récupération des noeuds du graphe fourni = ensemble N
        noeuds = list(G.nodes())
        nbNoeudsInitial = len(noeuds)
        
        #récupération des arcs du graphe fourni = ensemble A
        arcsBase = G.edges()
        
        #construction d'un autre ensemble
        #on rajoute la donnée du poids dans les arcs depuis tbLiaisons
        arcs = []
        for arc in arcsBase:
            (src,dst) = arc
            #récup donnée poids
            if (option == 1):
                #durée
                poids = int(self.getDuree(src, dst))
            else:
                #cout
                poids = float(self.getCout(src, dst))
            
            #rajout de l'item dans notre liste
            newArc=[src,dst,int(poids)]
            arcs.append(newArc)
        
        #tri de la liste des arcs par poids croissant
        lstArcs = sorted(arcs, key=itemgetter(2))        
        
        #on crée un graphe vide H
        H = netx.Graph() 
        
        #
        #Déroulé de l'algo
        poids_min = 0
        #on choisit au hasard un noeud de début nDebut
        while (len(noeuds) > 1):
            randomIndex = rand.randrange(0,len(noeuds)-1)
            nDebut = noeuds.pop(randomIndex)
            
            for i in range(len(lstArcs)):
                #on récupère dans l'ensemble A des arcs ceux pour qui il y a un link avec nDebut
                sousEnsemble = []
                ############# A revoir
                #if (lstArcs[i][0] == nDebut or lstArcs[i][1] == nDebut):
                if (lstArcs[i][0] == nDebut):
                    sousEnsemble.append(lstArcs[i])
                #ce sera notre ensemble B
                
                for j in range (len(sousEnsemble) > 0):            
                    #tant qu'un arc existe dans B et qu'il n'y pas de cycle, on le rajoute à H
                    noeud1 = sousEnsemble[j][0]
                    noeud2 = sousEnsemble[j][1]
                    poids = sousEnsemble[j][2]
                    H.add_edge(noeud1, noeud2, weight=poids, width=9.0)
                    
                    if netx.cycle_basis(H)!=[]:
                        H.remove_edge(noeud1, noeud2)
                    else:
                        poids_min = poids_min + poids
                    #notre nDebut devient maintenant le noeud terminal de l'arbre créé jusqu'ici
                    #nDebut = noeud2    
                    
                #puis on supprime cet arc de l'ensemble A
                #lstArcs.pop(i)                
                                        
        #on vérifie que le nombre de noeuds du graphe H = cardinal(N)
        #si oui graphe connexe, sinon non
        estConnexe = False
        if (len(H.nodes()) == nbNoeudsInitial):
            estConnexe = True            
        
        #on crée une figure pour y placer la carte
        #Retour = 3-uplet: Boolean connexe ou non, Arbre minimal, Poids arbre min
        valeur_retour = (estConnexe, H, poids_min)
        
        #on positionne l'arbre sur la carte de France
        img = plt.imread(self.fichierJpeg)        
        fig, ax = plt.subplots()
        ax.imshow(img)
                      
        #intégration du graphe dans le cadre indiqué avec la carte
        netx.draw_networkx(H, pos=self.getCityPositions(), ax=ax, width=6)
                   
        #titre graphe et ajustement dans le cadre défini par la variable figure
        ax.set_title("Arbre couvrant min sur la carte du pays - Prim")        
        fig.tight_layout()
        
        #ajustement de la figure avec les bonnes dimensions
        plt.rcParams["figure.figsize"] = (60,15)
                        
        plt.show()
        
        return valeur_retour


    #Partie B-Q2 - Ecrire une fonction qui prend en entrée un graphe 
    #retourne le meilleur chemin (le plus court) entre deux villes (sans contraintes)
    def meilleurTrajetParDuree(self, G, noeud1, noeud2):
        #parcours des arcs et détermination du poids sur la base de la durée du trajet
        for edge in G.edges():
            (src,dst) = edge
            duree = self.getDuree(src, dst)            
            netx.set_edge_attributes(G, int(duree), "duree")
        #on sauvegarde les données du graphe G
        G.edges(data=True)
        #on choisit le meilleur chemin entre noeud1 et noeud2 selon la méthode de Dijkstra 
        #pondération sur la durée du trajet
        bestPath = netx.shortest_path(G, source=noeud1, target=noeud2, weight="duree", method="dijkstra")
        return bestPath 
    
    
    #Partie B-Q3. Ecrire une fonction qui prend en entrée un graphe 
    #retourne le meilleur chemin (le moins cher) entre deux villes (sans contraintes)
    def meilleurTrajetParCout(self, G, noeud1, noeud2):
        #idem parcours des arcs et identification du poids de chacun (cout + péage)
        for edge in G.edges():
            (src,dst) = edge
            cout = self.getCout(src, dst)            
            netx.set_edge_attributes(G, float(cout), "cout")
        #sauvegarde données sur les ardcs
        G.edges(data=True)
        #on choisit le meilleur chemin entre noeud1 et noeud2 selon la méthode de Dijkstra 
        #pondération sur la durée du trajet
        bestPath = netx.shortest_path(G, source=noeud1, target=noeud2, weight="cout", method="dijkstra")
        return bestPath 
    
    
    #Partie B-Q4. Ecrire une fonction qui prend en entrée un graphe 
    #retourne le meilleur chemin (le plus court) entre deux villes (sans passer par des autoroutes)
    def meilleurTrajetParDureeSansRunway(self, G, noeud1, noeud2):
        #en cas d'échec d'identication de chemin, la fonction peut lever une exception
        #on copie le graphe dans notre variable de travail
        try:
            G2 = G
            #parcours des arcs du graphe de travail et identification du type de voie
            for edge in G2.edges():
               (src,dst) = edge
               tp = self.getTypeChemin(src, dst)
               if (tp == "a"):
                   G2.remove_edge(src, dst)
            #sauvegarde données
            G2.edges(data=True)
            #on choisit le meilleur chemin entre noeud1 et noeud2 selon la méthode de Dijkstra 
            #pondération sur la durée du trajet
            bestPath = netx.shortest_path(G2, source=noeud1, target=noeud2, weight="duree", method="dijkstra")
            return bestPath 
        except netx.NetworkXNoPath:
            pass
            return []
    
    #Partie B-Q5. Ecrire une fonction qui prend en entrée un graphe 
    #retourne le meilleur chemin (le moins cher) entre deux villes (sans passer par des départementales)
    def meilleurCheminParDureeSansDepartementale(self, G, noeud1, noeud2):
        #même méthode que précédemment
        #changement de contraintes: départementables uniquement
        #changement de pondération: cout+péage
        try:
            G2 = G
            for edge in G2.edges():
               (src,dst) = edge
               tp = self.getTypeChemin(src, dst)
               if (tp == "d"):
                   G2.remove_edge(src, dst)
            G2.edges(data=True)
            bestPath = netx.shortest_path(G2, source=noeud1, target=noeud2, weight="cout", method="dijkstra")
            return bestPath 
        except netx.NetworkXNoPath:
            pass
            return []
    
    
    #Partie B-Q6. Ecrire une fonction qui prend en entrée un ensemble de sommet, 
    #affiche le chemin en couleur sur la carte, ainsi que la durée et le côut total du trajet.
    def printCheminDureeCout(self,G,path,src,dst):        
         
         #on crée un graphe vide H
         H = netx.Graph()        
         for node in G.nodes():
             H.add_node(node)
        
         #Calcul cout et durée du chemin
         duree = 0
         cout = 0.0
         listeNoeuds = list(path)
         listeArcs = []
         #parcours des noeuds du chemin à afficher
         for i in range(len(listeNoeuds)-1):
            s = listeNoeuds[i]
            d = listeNoeuds[i+1]
            #pour chaque paire, on calcule la durée et le coût du trajet
            coutTroncon = float(self.getCout(s, d))
            dureeTroncon = int(self.getDuree(s, d))
            #on les additionne à nos totaux
            cout = cout + coutTroncon
            duree = duree + dureeTroncon            
            #création d'un nouvel arc pour notre graphe et intégration de l'arc
            edge = [s,d]            
            listeArcs.append(edge)        
            H.add_edge(s, d, width=9.0)
         
         #on positionne l'arbre sur la carte de France
         img = plt.imread(self.fichierJpeg)        
         fig, ax = plt.subplots()
         ax.imshow(img)
                       
         #intégration du graphe dans le cadre indiqué avec la carte
         netx.draw_networkx(H, pos=self.getCityPositions(), ax=ax, width=6)

         #titre graphe et ajustement dans le cadre défini par la variable figure
         titre = "Chemin entre " + src + " et " + dst + "\n"
         titre = titre + "Cout: " + str(cout) + " € - Duree = " + str(duree) + "mn"
         ax.set_title(titre)        
         fig.tight_layout()
       
         #ajustement de la figure avec les bonnes dimensions
         plt.rcParams["figure.figsize"] = (60,15)
                       
         plt.show()
        
         return H
    
    
#Première étape: demande fichiers
#jpeg
jpegFile = input("Donner le nom du fichier Jpeg: ")

#Demande fichier CSV et stockage données dans les variables filename et positions
print("Fournir le fichier CSV pour les POSITIONS des villes sur la carte \n")
(fPos, tbPos) = fctGetCsv.getCsv()

#Demande fichier CSV et stockage données dans les variables filename et positions
print("Fournir le fichier CSV pour les LIAISONS entre villes \n")
(fLiais, tbLiais) = fctGetCsv.getCsv()

if (not jpegFile):
    print("Impossible de poursuivre sans le fichier Jpeg")
else:
    if (not fPos or not tbPos):
        print("Impossible de poursuivre sans le CSV des positions")
    else:
        if (not fLiais or not tbLiais):
            print("Impossible de poursuivre sans le CSV des liaisons")
        else:
            #Le programme peut continuer normalement
            #Données correctement fournies
            
            #on crée notre objet principal
            tp = tpDeuxGraphes(jpegFile, fPos, fLiais, tbPos, tbLiais)
            
            #
            #Partie A
            #
            #Réponse Question A1
            print("Positions trouvées dans le CSV fourni: " + tp.fichierPositions + "|n")
            tp.showPositions()
            print("\n")
            
            print("Liaisons trouvées dans le CSV fourni: " + tp.fichierLiaisons + "\n")
            tp.showLiaisons()
            
            #Réponse Question A2
            print("Construction du graphe depuis les liaisons indiquées \n")
            grapheLiaisons = tp.buildGraphLiaisons()
            
            #Réponse Question A3
            print("Graphe sur la carte")
            tp.buildGraphOnMap()
            
            #
            #Partie B
            #
            
            #Question 1 - Vérification si graphe connexe ou pas
            #Prend en entree un graphe
            #Retour: True si oui, False sinon
            print("Vérification si graphe connexe - Travailler sur la durée (1) ou le cout(2)")
            print("\n")
            option = int(input("Donner l'option 1 pour la durée et 2 pour le coût: "))
            if (int(option) == 1):
                print("Vous avez choisi de travailler sur la base de la durée \n")                
            else:
                print("Vous avez choisi de travailler sur la base du coût + péage\n")
                
            print("Poursuite de la recherche\n")    
            
            retour = tp.grapheConnexeKruskal(grapheLiaisons, option)
            if (retour[0] == True):
                print("Le graphe est connexe avec un arbre couvrant - Algo Kruskal")
                print("\n")
                print("Poids de l'arbre: ")
                print(retour[2])
                if (option == 1):
                    print(" mn")
                else:
                    print(" €")
                print("\n")
                print("Longueur du chemin (nombre de tronçons de ville à ville: ")
                edgeCount = len(list(retour[1].edges()))
                print(edgeCount)
                print("\nNombre de villes traversées: ")
                nodeCount = len(list(retour[1].nodes()))
                print(nodeCount)
                print("\n")
                
            else:
                print("Le graphe n'est pas connexe \n ")
                print("\n")
                print("Poids de l'arbre: ")
                print(retour[2])
                if (option == 1):
                    print(" mn")
                else:
                    print(" €")
                print("\n")
                print("Longueur du chemin (nombre de tronçons de ville à ville: ")
                edgeCount = len(list(retour[1].edges()))
                print(edgeCount)
                print("\nNombre de villes traversées: ")
                nodeCount = len(list(retour[1].nodes()))
                print(nodeCount)
                print("\n")
                
            #Question 1 bis
            retour = tp.grapheConnexePrim(grapheLiaisons, option)
            if (retour[0] == True):
                print("Le graphe est connexe avec un arbre couvrant - Algo Prim")
                print("\n")
                print("Poids de l'arbre: ")
                print(retour[2])
                if (option == 1):
                    print(" mn")
                else:
                    print(" €")
                print("\n")
                print("Longueur du chemin (nombre de tronçons de ville à ville: ")
                edgeCount = len(list(retour[1].edges()))
                print(edgeCount)
                print("\nNombre de villes traversées: ")
                nodeCount = len(list(retour[1].nodes()))
                print(nodeCount)
                print("\n")
                
            else:
                print("Le graphe n'est pas connexe \n ")
                print("\n")
                print("Poids de l'arbre: ")
                print(retour[2])
                if (option == 1):
                    print(" mn")
                else:
                    print(" €")
                print("\n")
                print("Longueur du chemin (nombre de tronçons de ville à ville: ")
                edgeCount = len(list(retour[1].edges()))
                print(edgeCount)
                print("\nNombre de villes traversées: ")
                nodeCount = len(list(retour[1].nodes()))
                print(nodeCount)
                print("\n")
            
            
            #Question 2 - Ecrire une fonction qui prend en entrée un graphe 
            #retourne le meilleur chemin (le plus court) entre deux villes (sans contraintes)
            src = input("Donner le nom de la ville Source (tiré du CSV Position): ")
            dst = input("Donner le nom de la ville Destination (tiré du CSV Position): ")
            retourCheminDuree = tp.meilleurTrajetParDuree(grapheLiaisons,src,dst)
            print("Meilleur chemin par durée: ")
            print(retourCheminDuree)
            print("\n")
            #Question 3. Ecrire une fonction qui prend en entrée un graphe 
            #retourne le meilleur chemin (le moins cher) entre deux villes (sans contraintes)
            retourCheminCout = tp.meilleurTrajetParCout(grapheLiaisons,src,dst)
            print("Meilleur chemin par coût+péage: ")
            print(retourCheminCout)
            print("\n")
            
            #Question 4. Ecrire une fonction qui prend en entrée un graphe 
            #retourne le meilleur chemin (le plus court) entre deux villes (sans passer par des autoroutes)
            retourCheminDepartementales = tp.meilleurTrajetParDureeSansRunway(grapheLiaisons,src,dst)
            print("Meilleur chemin sans autoroute : ")
            if (len(retourCheminDepartementales)):
                print(retourCheminDepartementales)
            else:
                print("Pas de chemin trouvé sans passer par des autoroutes")
            print("\n")
            
            
            #Question 5. Ecrire une fonction qui prend en entrée un graphe 
            #retourne le meilleur chemin (le moins cher) entre deux villes (sans passer par des départementales)
            retourCheminAutoroutes = tp.meilleurCheminParDureeSansDepartementale(grapheLiaisons,src,dst)
            print("Meilleur chemin sans autoroute : ")
            if (len(retourCheminAutoroutes)):
                print(retourCheminAutoroutes)
            else:
                print("Pas de chemin trouvé sans passer par des départementales")  
            print("\n")
            
            #Question 6. Ecrire une fonction qui prend en entrée un ensemble de sommet, 
            #affiche le chemin en couleur sur la carte, ainsi que la durée et le côut total du trajet.
            path = retourCheminDuree   
            tp.printCheminDureeCout(grapheLiaisons,path,src,dst)
            
            
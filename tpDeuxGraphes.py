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
#


#import des fonctions développées
import fctGetCsv

class tpDeuxGraphes:
    #attributs
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
        
        #couleurs: autoroute = rouge, departementale = vert
        colors = []
        
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
        #la source et la destination peuvent s'intervertir
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
                duree = self.tbLiaisons[a][3]
            else:
                if (self.tbLiaisons[a][1].strip() == src.strip() and self.tbLiaisons[a][0].strip() == dst.strip()):
                    duree = self.tbLiaisons[a][3]
        return duree
    
    #récupérer le cout associé à un chemin
    def getCout(self, src, dst):
        cout = 0
        #graphe non orienté, on considère les 2 options
        #la source et la destination peuvent s'intervertir
        for a in range(len(self.tbLiaisons)):
            if (self.tbLiaisons[a][0].strip() == src.strip() and self.tbLiaisons[a][1].strip() == dst.strip()):
                cout = self.tbLiaisons[a][4]
            else:
                if (self.tbLiaisons[a][1].strip() == src.strip() and self.tbLiaisons[a][0].strip() == dst.strip()):
                    cout = self.tbLiaisons[a][4]
        return cout
    
    #Partie B - Question 1:
    #Prend en entree un graphe
    #Retour: 3-uplet (Boolean connexe ou non, Arbre minimal, Poids arbre min)
    #Rappel: graphe connexe si pour tout UV, il existe un chemin de U à V
    #Rappel: graphe connexe ssi contient un arbre couvrant (passe par tous les sommets)
    #option: pour travailler avec la durée (1) ou le coût (2)  
    def grapheConnexe(self,G,option):                          
        #on va construire un arbre
        H = netx.Graph() 
        #autres valeurs de retour
        arbre_trouve = False
        poids_min = 0
        
        #récup liste des arcs
        edge_list = list(G.edges())
        print(edge_list)
        
        for j in range(len(edge_list)):
            
            (noeud1, noeud2)=edge_list[j]  
            
            if (option == 1):
                #durée
                poids = self.getDuree(noeud1, noeud2)
            else:
                #cout
                poids = self.getCout(noeud1, noeud2)
                
            H.add_edge(noeud1, noeud2, weight=poids, width=9.0)
            #s'il n'y a pas de cycle, on poursuit
            #sinon on supprime cet arc
            
            if netx.cycle_basis(H)!=[]:
                H.remove_edge(noeud1, noeud2)

        #on parcourt l'arbre pour calculer le poids minimal
        
        liste_noeuds_en_cours = list(H.edges(data='weight')) 
        print(liste_noeuds_en_cours)
        for i in range(len(liste_noeuds_en_cours)):
            (src,dest,w)=liste_noeuds_en_cours[i]
            poids_min = poids_min + int(w)
            
        print("L'arbre couvrant minimal est ", poids_min)
        
        nb_noeuds_arbre_kruskal = len(H.nodes())
        nb_noeuds_graphe_source = len(G.nodes())
        
        
        if (nb_noeuds_arbre_kruskal == nb_noeuds_graphe_source):
            arbre_trouve = True
        
        #Retour = 3-uplet: Boolean connexe ou non, Arbre minimal, Poids arbre min
        valeur_retour = (arbre_trouve, H, poids_min)
        
        #on positionne l'arbre sur la carte de France
        img = plt.imread(self.fichierJpeg)        
        fig, ax = plt.subplots()
        ax.imshow(img)
                      
        #intégration du graphe dans le cadre indiqué avec la carte
        netx.draw_networkx(H, pos=self.getCityPositions(), ax=ax)
                   
        #titre graphe et ajustement dans le cadre défini par la variable figure
        ax.set_title("Arbre couvrant min sur la carte du pays")        
        fig.tight_layout()
        
        #ajustement de la figure avec les bonnes dimensions
        plt.rcParams["figure.figsize"] = (60,15)
                        
        plt.show()
        
        return valeur_retour
        


#Première étape: demande fichiers
#jpeg
jpegFile = input("Donner le nom du fichier Jpeg: ")

#Demande fichier CSV et stockage données dans les variables filename et positions
print("Fournir le fichier CSV pour les positions des villes sur la carte \n")
(fPos, tbPos) = fctGetCsv.getCsv()

#Demande fichier CSV et stockage données dans les variables filename et positions
print("Fournir le fichier CSV pour les liaisons entre villes \n")
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
            print("Vérification si graphe connexe - Travail sur la durée (1) ou le cout(2)")
            print("\n")
            option = int(input("Donner l'option 1 pour la durée et 2 pour le coût: "))
            retour = tp.grapheConnexe(grapheLiaisons, option)
            if (retour[0] == True):
                print("Le graphe est connexe avec un arbre couvrant minimal ")
                print("\n")
                print("Poids de l'arbre: ")
                print(retour[2])
            
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:43:56 2022

@author: tidiane
"""

"""
import pandas as pan
df = pan.read_csv('test.csv', delimiter=';')
tuples = [tuple(x) for x in df.values]
print(tuples)  
"""

def getCsv():
    #import module
    import csv
    #demande nom fichier csv
    filename = input("Indiquer le nom de votre fichier CSV:\n")
    
    #demande précision séparateur
    separateur = input("Indiquer le séparateur de champs CSV:\n")
    
    #demande précision header
    headerInclus = input("Le fichier inclut-il une ligne d'en-tête - réponse O ou N:\n")
    
    #ouverture csv
    with open(filename, 'r') as fichierCSV:
      lecteurCSV = csv.reader(fichierCSV, delimiter=separateur)
      #remplissage liste
      liste_taches = list(lecteurCSV)
    #parcours liste
    if (headerInclus == 'N'):
        print("CSV sans en-tete\n")
        
    else:
        print("Header : " + liste_taches[0] + "\n")
    
    #option 1
    print("Affichage option 1")
    [print(ligne) for ligne in liste_taches] 
    print("\n")
    #option 2
    print("Affichage option 2")
    for j in range(len(liste_taches)): 
        #affichage ligne par ligne
        print(liste_taches[j])
    
    return liste_taches

getCsv()
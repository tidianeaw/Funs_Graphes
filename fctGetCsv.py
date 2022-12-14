# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 18:16:05 2022

@author: Ahmed & Shahram
"""


def getCsv():
    #import module
    import csv
    
    print("Le fichier doit être placé dans le même dossier que ce programme\n")
    
    #demande nom fichier csv
    filename = input("Indiquer le nom de votre fichier CSV:\n")
    
    #demande précision séparateur
    separateur = input("Indiquer le séparateur de champs (, ou ;) CSV:\n")
    
    #demande précision header
    headerInclus = input("Le fichier inclut-il une ligne d'en-tête - réponse O ou N:\n")
    
    #ouverture csv
    with open(filename, 'r') as fichierCSV:
      lecteurCSV = csv.reader(fichierCSV, delimiter=separateur)
      #construction liste à partir du contenu
      donnees = list(lecteurCSV)
    
    #parcours liste
    if (headerInclus == 'N'):
        #le fichier fourni n'inclut pas d'en-tête, on poursuit
        print("CSV sans en-tete\n")
        
    else:
        #fichier avec en-tête, on supprimer la ligne d'en-tête avant de continuer
        print("Header : \n")
        print(donnees[0])
        print("Suppression du Header avant poursuite")
        donnees.pop(0)
        
    return (filename, donnees)

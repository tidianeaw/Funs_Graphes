# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 19:42:11 2022

@author: tidiane
"""

#import des fonctions développées
import fctGetCsv

#Demande fichier CSV et stockage données dans les variables filename et positions
print("Fournir le fichier CSV pour les liaisons entre villes \n")
(fLiais, tbLiais) = fctGetCsv.getCsv()
colors = []

for a in range(len(tbLiais)):
    source = tbLiais[a][0]
    destination = tbLiais[a][1]
    
    #type = ce sera une contrainte
    typeChemin = tbLiais[a][2]

    col = 'green'
    if (typeChemin.strip() == "a"):
        col='red'
    colors.append(col)
    
    print(source+"-"+destination+"-"+col + " - " + typeChemin + "\n")
    

print(colors)
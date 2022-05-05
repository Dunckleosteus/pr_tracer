
# ce programme prend une table excel en entree. La table comporte trois colonnes:
#   - nom de route
#   - numéro de pr
#   - sens
#   - x (lambert 93)
#   - y (lambert 93)
# Prdev va ensuite chercher le pr correspondant et mesurer la distance qui séparer le pr présent dans la base de données
# de celle contenue dans l'excel. A terme il faudrais offrir la possibilité de remplacer le pr de la base avec celle
# qui est contenue dans la base de donnees.

#====================================================[gestion des imports]===================================================================================================
import os # permet la creation de filepath relatifs
import sqlite3 # utilisation de sqlite 3 pour le stockage des donnees
import math # import utilise pour des formules mathematiques
from operator import itemgetter
import pandas as pd
import traceback
import functions # referring to the function.py file containing functions used by prtracer
import pyproj # used to convert wgs to 2154
#=====================================================[declaration des variables]===========================================================================================
failed = []     # liste des route qui n'on pas etees traces
num_pr = 0      # stores the value of the pr number that has to be searched
PR = []         # stores the prs extracted from the database
PR_dist = []    # num pr, x_base, y_base, x_excel, y_excel
#=====================================================[chercher les donnes dans excel]======================================================================================
# ce qu'il faut dans excel:
#       |   route   |   num_pr    |     sens        |   X   |   Y   |
#       """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#       |           |             |                 |       |       |

df=pd.read_excel(os.path.join("input","input.xlsx") ,sheet_name=0)  # localisation de la table excel en input
df=df[['route', 'num_pr', 'sens', 'X', 'Y']]                        # enlever les colonnes inutiles
df=df.dropna()                                                      # lache les lignes avec des valeurs vides

df["num_pr"]=df["num_pr"].astype(int)   # transforme la colonne numero pr en integer
df["sens"]=df["sens"].astype(int)       # transforme la colonne sens en integer
df["X"]=df["X"].astype(float)           # transforme la colonne X en floating point number
df["Y"]=df["Y"].astype(float)           # transforme la colonne Y en floating point number

# ====================================================[Partie sql]===========================================================================================
for i in range(0,len(df.index)):        # pour chaque ligne dans le tableau de départ
    try:
        connection = sqlite3.connect(os.path.join("database","Roads.db"))       # cree une connection avec la base de donnes sqlite 3 dans le fichier database
        cursor=connection.cursor()                                              # in charge of communication with database
                                                                                # pour respecter la nomenclature toute les routes doivent avoir un nom de longeur fixe pour la requete sql
        if len (df.at[i,'route']) == 2:                                           # si le nom de la route de longueur 2 alors il faut ajouter trois 0 ex: A1 -> A0001
            rte=df.at[i,'route'][:1]+"000"+df.at[i,'route'][1:]
        if len (df.at[i,'route']) == 3:# A21 -> A0021
            rte=df.at[i,'route'][:1]+"00"+df.at[i,'route'][1:]
        if len (df.at[i,'route']) == 4:# A321 -> A0321
            rte=df.at[i,'route'][:1]+"0"+df.at[i,'route'][1:]
                                                                               # la variable sens va servir dans la nomenclature pour la requete sql
        # sens 1 = D and sens 2 = G
        if int(df.at[i,'sens'])==1: sens="D"                                    # si le sens de la route est de 1 alors attribue la valeur 'D' a la variable sens
        elif int(df.at[i,'sens'])==2: sens="G"                                  # si le sens de la routes et 2 alors G
        num_pr = df.at[i,'num_pr']
        # collect wanted prs
        cursor.execute("SELECT x,y,pr from T_PR WHERE route='{}' and cote='{}'and pr ='{}'".format(rte,sens,num_pr))# utiliser variable sens et rte pour executer une requet sql
        PR = cursor.fetchall()
        #PR_dist.append ([PR[0][2], PR[0][0], PR[0][1], df.at[i,'X'], df.at[i,'Y']])
        PR_dist.append ([PR[0][2], math.dist((PR[0][0], PR[0][1]), (df.at[i,'X'], df.at[i,'Y']))])
        print(PR_dist)
        connection.close()  # ferme la connection a la base de donnees.

    except Exception as e:# pour que le programme continue de s'executer meme si une route ne peut pas etre trace
        print(e) # montre le type d erreur
        print(traceback.format_exc())
for i in failed:
    print(i)
exit()

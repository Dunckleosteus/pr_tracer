#%%
import pandas as pd
import numpy as np
import os
import functions
import sqlite3
from pyproj import CRS, transform, Proj
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
#%%
df = pd.read_excel(os.path.join("input", "data.xlsx"))
#%%
outProj = Proj(init='epsg:2154')
inProj = Proj(init='epsg:4326')
#%%
df2 = df.loc[(df['Event'] == "EVT3")]                                           # looks for event3 lines
df2 = df2[["Route","SENS","PR_FIN", "LON_BEGIN","LAT_BEGIN","LON_END","LAT_END"]]         # select only wanted columns
df2["LON_END"] = df2["LON_END"].astype(float)                                   # convert end longitude to float
df2["LAT_BEGIN"] = df2["LAT_BEGIN"].astype(float)                               # convert start latitude to float
df2["LAT_END"] = df2["LAT_END"].astype(float)                                   # convert end latitude to float
df2["X"] = (df["LON_BEGIN"] + df["LON_END"])/2                                  # create X colums is average of start and end longitude
df2["Y"] = (df["LAT_BEGIN"] + df["LAT_END"])/2                                  # create Y column is average of start end latitude
df2["Estimated pr"] = ""                                                        # creates new field filled with empty face
df2["Estimation delta"] = 0.0                                                     # creates new field and fills it with 0

df2 = df2.reset_index()                                                         # reset index to account for removed rows
for i in range(0,len(df2.index)):                                               # loops through each line in the dataframe
    rte = ""                                                                    # pour chaque ligne dans le tableau de départ
    connection = sqlite3.connect(os.path.join("database","Roads.db"))           # cree une connection avec la base de donnes sqlite 3 dans le fichier database
    cursor = connection.cursor()                                                # in charge of communication with database
    rte = df2['Route'].iloc[i]                                                  # la variable sens va servir dans la nomenclature pour la requete sql
    # sens 1 = D and sens 2 = G
    if int(df2.at[i,'SENS']) == 1: sens = "D"                                   # si le sens de la route est de 1 alors attribue la valeur 'D' a la variable sens
    elif int(df2.at[i,'SENS']) == 2: sens = "G"                                 # si le sens de la routes et 2 alors G
    try:                                                                             # collect wanted prs
        cursor.execute("SELECT x,y,pr from T_PR WHERE route='{}' and cote='{}'".format(rte,sens))# utiliser variable sens et rte pour executer une requet sql
        PR = cursor.fetchall()                                                      # list of all the pr with
        # find closest value pr
        PRb = []
        result = []
        x = df2.at[i, "X"]
        y = df2.at[i, "Y"]
        x2,y2 = transform(inProj, outProj, x, y)
        PRc, m_value = functions.closest(x2, y2, PR)
    except Exception as e: 
        print(e)
    try:
        PRb = PR[PRc][2]
    except Exception as e:
        PRb = str(e)
    df2.at[i, 'Estimated pr'] = PRb
    df2.at[i, 'Estimation delta'] = m_value
    connection.close()
#%%
print(df2)
df2.to_excel("output.xlsx")

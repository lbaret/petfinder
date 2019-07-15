import pandas as pd
import os

train_path = os.path.abspath(os.path.dirname(__name__)) + '\\petfinder-adoption-prediction\\train\\train.csv'

# Lecture du fichier des données d'entrainement
df = pd.read_csv(train_path, sep=',')

# On récupère les noms de colonnes
columns_names = list(df.columns.values)
print(columns_names)

"""
    À la simple vision des noms de colonnes on peut très vite s'orienter vers un calcul de corrélations avec la rapidité d'adoption :
        - Vaccinated
        - Dewormed
"""

df_bis = df[['Vaccinated', 'Dewormed', 'AdoptionSpeed']]
correlation = df_bis.corr(method='pearson')
print(correlation)
# On peut également faire toutes les données et filtrer les valeurs

correlation = df.corr(method='pearson')
print(correlation)
# TODO : Créer le filtre avec deux seuils.

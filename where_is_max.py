import threading
from PIL import Image
from glob import glob
import os
import math

"""
Ce code est présent pour calculer la largeur et la hauteur max de toutes les images du dataset.
Sur google colab, nous avons la possibilité de travailler sur 2 threads.
Or le traitement n'est pas lourd, donc nous allons travailler sur 10 threads pour optimiser le temps.
"""

# Variables pour le multi-threading
lock = threading.Lock()
threads = []
nb = 10

# Fonction de contrôle d'exécution des threads
def areRunning(pourcentage):
    return True if pourcentage < 1.0 else False

# Variables de chemins d'accès
root = os.path.abspath(os.path.dirname(__name__))
data_path = root + "/pixabay/dogs/"
files = glob(data_path + "1/*")
files += glob(data_path + "0/*")

# Initialisation des variables utiles
maxH = 0
maxW = 0
total = actual = len(files)
cnt = 0
cut = math.ceil(total/nb)

# Fonction pour le traitement
def checkMax(files, lock):
    global cnt, maxH, maxW
    for f in files:
        lock.acquire()
        img = Image.open(f)
        w = img.width
        h = img.height
        if w > maxW:
            maxW = w
        if h > maxH:
            maxH = h
        cnt += 1
        lock.release()

# Traitement
for i in range(nb):
    # Calcul des indices de liste
    next = actual - cut
    if next >= 0:
        min = i * cut
        max = (i+1) * cut
    else:
        min = i * cut
        max = min + actual

    # Création du thread
    t = threading.Thread(target=checkMax, args=(files[min:max], lock))
    threads.append(t)
    t.start()

    dots = ''
    print("\nTraitement en cours ...")
    loop = True
    while loop:
        # Affichage de l'avancement
        print('\rEffectué : {:%}'.format(cnt/total), end='')
        loop = areRunning(cnt / total)

    # Fermeture des threads
    for i in range(nb):
        threads[i].join()

files = None
print("\nMax height : {}\nMax width : {}".format(maxH, maxW))

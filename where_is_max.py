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
data_path = root + "/pixabay/cats/"
files = glob(data_path + "1/*")
files += glob(data_path + "0/*")

# Initialisation des variables utiles
all_max = []
total = actual = len(files)
cnt = 0
cut = math.ceil(total/nb)

# Fonction pour le traitement
def checkMax(files, lock):
    global cnt, all_max
    maxH = 0
    maxW = 0
    for f in files:
        img = Image.open(f)
        w = img.width
        h = img.height
        if w > maxW:
            maxW = w
        if h > maxH:
            maxH = h
        lock.acquire()
        cnt += 1
        lock.release()
    lock.acquire()
    all_max.append((maxH, maxW))
    lock.release()


# Traitement
for i in range(nb):
    # Calcul des indices de liste
    next = actual - cut
    if next >= 0:
        minI = i * cut
        maxI = (i+1) * cut
    else:
        minI = i * cut
        maxI = min + actual

    # Création du thread
    t = threading.Thread(target=checkMax, args=(files[minI:maxI], lock))
    threads.append(t)
    t.start()

dots = ''
print("\nTraitement en cours ...")
while areRunning(cnt/total):
    print("\rChargement ... Avancement : {:0.2f}%".format(cnt/total*100), end='')

# Fermeture des threads
for i in range(nb):
    threads[i].join()

files = None
maxH = max(all_max, key=lambda x: x[0])[0]
maxW = max(all_max, key=lambda x: x[1])[1]
print("\nMax height : {}\nMax width : {}".format(maxH, maxW))

"""
    For dogs :
    max height = 340
    max width = 1241
    
    For cats :
    max height = 340
    max width = 1162
"""

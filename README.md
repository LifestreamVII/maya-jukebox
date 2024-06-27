<p align="center">
  <a href="" rel="noopener">
 <img src="https://i.imgur.com/lVOiXrE.jpeg" width="500px" alt="Project header"></a>
</p>
<h1 align="center">Maya Jukebox</h1>

Maya Jukebox est un script Python programmé pour Autodesk Maya (testé sur 2024) qui génère une scène animée à partir du titre d'un album de musique et de son artiste.

# Animations

Il y a deux animations proposées par le script : **Boîte de CD** et **Page Spotify**.
La première récupère l'image de couverture de l'album et créé une animation du CD se rangeant dans une boîte, à partir d'un modèle de scène et des textures appliquées sur les modèles.
La seconde télécharge une capture d'écran de la page Spotify de l'album et la projette sur un écran, mis en face d'un personnage en mouvement.   

# Fonctionnement

À partir des données fournies dans l'interface Qt (titre et artiste), une API externe (code dans le repo) va effectuer une recherche depuis l'API REST de Spotify pour récupérer l'image de couverture de l'album voulu. L'URL est renvoyée, la texture se télécharge et s'applique sur les maillages du modèle FBX pour l'animation 1 (`cdmodel.fbx`).
Pour la seconde animation, c'est le même principe (cette fois avec le fichier `desk.fbx`), mais l'API externe va récupérer auprès de l'API Spotify l'URL de l'album, pour renvoyer automatiquement une capture d'écran effectuée par un service Chrome sans interface (headless).

# Installation

Le script nécessite l'installation des modules Python : `requests` et `base64`. 
La commande d'installation est la suivante :

    mayapy -m pip install <package>

Les services en back-end peuvent être déployés en local (le script utilisant déjà une version distante et fonctionnelle) en installant les containers Docker.

    docker compose up -d --build

Veiller à créer un fichier .env avec les identifiants pour la connexion à l'API REST de Spotify : `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`

# Utilisation

Il suffit simplement de remplir les champs requis dans l'interface Qt : titre de l'album, artiste, choix d'animation. Une fenêtre va demander l'importation du fichier de modèle FBX qui change en fonction de l'animation. Pour l'animation 1, choisir cdmodel.fbx, pour l'animation 2, choisir `desk.fbx`. Les fichiers devraient se trouver dans le même dossier que le script `ui.py`.

Si aucun album n'a été trouvé, le script va renvoyer l'erreur `'NoneType' object has no attribute 'timeout'`

# Demo

[Demo](https://www.youtube.com/watch?v=oTB_NJbxjmA)

# Crédits

Service Puppeteer : [https://github.com/mingalevme/screenshoter](https://github.com/mingalevme/screenshoter)

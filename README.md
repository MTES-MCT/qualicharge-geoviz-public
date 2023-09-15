# qualicharge-geoviz-public
Projet d'application web concernant des visualisations sur les données des bornes de recharges en France


## Organisation du répo

- **data** : Dossier contenant les données utiles au fonctionnement du projet.
  - Alimenté par l'équipe qualicharge avec des données anonimisé sur l'état du réseau de bornes de recharges
- **src** : Dossier contenant le code source de l'application
  - ***assets/media*** : images utilisés dans la webapp
  - ***assets/pages*** : code des pages affiché sur la webapp
  - ***utils*** : fonctionnalités transverses utilisé par un/des page(s)
- **install** : Dossier contenant les fichiers nécessaires à l'installation du projet


## Pré-requis

Afin de pouvoir utiliser ce projet vous aurez besoin des outils suivants :
- **python**
  - Langage de développement utilisé pour cette application
- **docker**
  - Service de gestion de conteneur
- **docker-desktop / colima**
  - Machine virtuelle qui va heberger vos conteneurs sur votre machine


## Utilisation

Vous pouvez utiliser cette application web de deux façons : 
- En utilisant Docker
- En local avec un environnement virtuel python (ex: pip)

### Avec Docker
docker-desktop ou colima doit être lancé pour pouvoir utiliser les commandes de docker
Création de l'image docker utilisé pour l'application
```bash
docker build -t qualicharge_geoviz .
```
***build*** *: création d'une image à partir du "Dockerfile" présent dans le dossier précisé en fin de commande (ici ".")*
*-t : donne un tag lors de la construction de l'image*

Lancement de l'image avec redirection du port 8501 de votre machine vers le port 8501 du conteneur
```bash
docker run -dp 127.0.0.1:8501:8501 qualicharge_geoviz
```
***run*** *: lancer une image déjà construite*
*-d : detached, lance le conteneur en arrière plan*
*-p : publish, expose le port précisé juste après*


Regarder le status de l'image

### Locale

#### Mise en place de l'environnement

Pour commencer, créez un environnement virtuel du nom que vous souhaitez. Pour l'exemple nous utiliserons *"my_env"*
```bash
python -m venv "my_env"
```

Ensuite, chargez l'environnement avec la commande correspondant à votre OS :
```bash
# Linux / Mac OS
source my_env/bin/activate
# Windows
source my_env/Scripts/activate
```

Installation des prérequis avec la commande suivant : 
```bash
pip install -r install/requirements.txt
```

#### Lancement de l'application

Vous pouvez ensuite lancez l'application avec le script `run_webapp.sh`
```bash
./run_webapp.sh
```
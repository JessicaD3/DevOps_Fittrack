# DevOps_AppliPerdrePoids
Projet en DevOps - Mastere Première Année | Application pour perdre du poids


🔹 Installation locale (sans Jenkins)
1️⃣ Cloner le dépôt
git clone https://github.com/JessicaD3/DevOps_AppliPerdrePoids.git
cd DevOps_AppliPerdrePoids

2️⃣ Créer un environnement virtuel
python -m venv venv


Activer l’environnement :

venv\Scripts\activate

3️⃣ Installer les dépendances
pip install -r requirements.txt

4️⃣ Initialiser la base de données MySQL

Dans MySQL :

CREATE DATABASE fittrack;


Exécuter le script SQL fourni pour créer les tables.

Créer un utilisateur MySQL dédié :

CREATE USER 'fittrack'@'localhost' IDENTIFIED BY 'fittrack123';
GRANT ALL PRIVILEGES ON fittrack.* TO 'fittrack'@'localhost';
FLUSH PRIVILEGES;

5️⃣ Lancer l’application Flask
python -m app.main


L’application est accessible à l’adresse :

http://127.0.0.1:5000

🔹 Génération du rapport PDF

Depuis l’environnement virtuel :

python -m app.pdf_report


Un fichier PDF est généré à la racine du projet.

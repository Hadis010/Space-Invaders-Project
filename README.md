# Space Invaders — PCO

Jeu **Space Invaders** développé en Python avec l’interface graphique **Tkinter**. Projet réalisé dans le cadre du cours de Programmation et Conception Orientées Objet (PCO).

---

## Auteurs

- **MUNKHTUUL Khosbayar**
- **DINI Hafsa**

---

## Description

Space Invaders est un jeu classique de type shoot’em up : le joueur pilote un vaisseau en bas de l’écran et doit détruire une flotte d’aliens qui avancent. Le score est affiché et le jeu se termine en cas de victoire (tous les aliens détruits) ou de défaite (les aliens atteignent le vaisseau).

---

## Fonctionnalités

- **Écran d’accueil** : saisie du nom du joueur et image de bienvenue
- **Jeu** : vaisseau contrôlable, tir de projectiles, flotte d’aliens en mouvement
- **Score** : affichage du score en temps réel (10 points par alien détruit)
- **Victoire / défaite** : messages distincts selon l’issue de la partie
- **Persistance** : modèles de données pour enregistrer et charger les scores (JSON)

---

## Prérequis

- **Python 3.x** (testé avec Python 3)
- **Tkinter** (généralement inclus avec Python)
- Fichiers d’assets dans le même dossier que le script :
  - `lose.png` — image d’accueil / écran de défaite
  - `alien.gif` — sprite des aliens
  - `explosion.gif` — animation d’explosion

---

## Installation et exécution

1. Cloner ou télécharger le projet dans un dossier.
2. S’assurer que les fichiers `lose.png`, `alien.gif` et `explosion.gif` sont dans le même répertoire que `Hafsa PCO.py`.
3. Lancer le jeu :

```bash
python "Hafsa PCO.py"
```

Sous Windows, si `python` n’est pas reconnu, essayer :

```bash
py "Hafsa PCO.py"
```

---

## Comment jouer

| Touche        | Action                    |
|---------------|---------------------------|
| **Flèche gauche**  | Déplacer le vaisseau à gauche |
| **Flèche droite**  | Déplacer le vaisseau à droite |
| **Espace**        | Tirer                      |

- Détruisez tous les aliens pour gagner.
- Ne laissez pas les aliens atteindre votre vaisseau, sinon vous perdez.

---

## Structure du projet

```
PCO vf/
├── Hafsa PCO.py      # Script principal du jeu
├── lose.png          # Image d'accueil / écran de défaite
├── alien.gif         # Sprite des aliens
├── explosion.gif     # Animation d'explosion
├── Rapport final PCO.docx
└── README.md
```

---

## Architecture du code (orienté objet)

| Classe          | Rôle principal                                      |
|-----------------|-----------------------------------------------------|
| `Score`         | Représente un score (nom, points, temps) ; sérialisation JSON |
| `Resultat`      | Liste de scores ; chargement / sauvegarde fichier   |
| `SpaceInvaders` | Fenêtre d’accueil, saisie du nom, démarrage du jeu  |
| `Game`          | Boucle de jeu, canvas, gestion clavier et animation  |
| `Defender`      | Vaisseau du joueur (déplacement, tir)               |
| `Bullet`        | Projectile tiré par le vaisseau                     |
| `Alien`         | Un alien (affichage, collision, explosion)          |
| `Fleet`         | Flotte d’aliens (déplacement, gestion des touches) |

---

## Technologies utilisées

- **Python 3**
- **Tkinter** — interface graphique et canvas
- **JSON** — structure des données de score (classes `Score` et `Resultat`)

---

## Licence

Projet pédagogique — usage dans le cadre du cours PCO.

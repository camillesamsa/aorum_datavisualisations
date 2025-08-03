
# Visualisations de données — Projet Aorum

Ce dépôt regroupe les **visualisations interactives** et les **outils de traitement de données** développés dans le cadre du **projet de recherche Aorum**, qui explore l'usage de l'or comme matériau pictural à travers un corpus d'œuvres.

Les données sont issues d’analyses portant sur la **provenance**, l’**iconographie**, les **caractéristiques optiques** et la **composition matérielle** des œuvres, afin de mieux comprendre le rôle visuel, technique et symbolique de l’or dans la peinture européenne des XVIᵉ et XVIIᵉ siècles.

---

## Structure du dépôt

Le dépôt est organisé en deux dossiers principaux :

- `visualisations/`  
  Contient les **interfaces HTML/CSS/JS** pour les visualisations interactives. Ces visualisations utilisent des **fichiers CSV** comme source de données, générés à partir des tableurs initiaux.

- `traitement/`  
  Contient les **scripts Python** (notebooks Jupyter) servant à **nettoyer**, **transformer** et **harmoniser** les données issues des **tableurs au format `.ods`**.  
  Ces scripts produisent les fichiers CSV utilisés par les visualisations.

Ainsi, les fichiers CSV présents dans le dossier `visualisations/` sont **issus d’un pipeline de préparation des données** défini dans le dossier `traitements/`.

---

## Objectifs

- Permettre une **exploration intuitive et visuelle** du corpus d'œuvres, avec une approche statistique
- Mettre en valeur la **diversité typologique et géographique** des données
- Offrir des **interactions dynamiques** pour faciliter l’analyse et la comparaison
- Proposer des visualisations **légères et autonomes**, facilement intégrables à un futur site web

---

## Technologies utilisées

- [D3.js v7](https://d3js.org/) — Librairie de visualisation de données
- HTML5 / CSS3 — Structure et style des pages
- Python 3 — Scripts de traitement des données (via Jupyter Notebooks)
- Fichiers `.ods` (LibreOffice / Excel) — Tableurs source
- Fichiers `.csv` — Données structurées utilisées pour les visualisations

---

## Installation et utilisation

### Prérequis

- Navigateur web moderne
- Serveur HTTP local (recommandé pour éviter les restrictions CORS)

### Lancer les visualisations

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/aorum-datavisualisations.git
   cd aorum-datavisualisations/visualisations
   ```

2. **Lancer un serveur local** :
   ```bash
   # Avec Python 3
   python3 -m http.server 8000
   ```

3. **Ouvrir dans le navigateur** :  
   Rendez-vous sur `http://localhost:8000` pour explorer les visualisations.

---

## Fonctionnalités

- **Navigation interactive** dans le corpus
- **Filtres combinables** par période, provenance, iconographie, etc.
- **Visualisations croisées**
- **Affichage responsive** pour une consultation sur ordinateur ou mobile

---

## À propos du projet Aorum

**Aorum** est un projet interdisciplinaire réunissant chercheurs en **histoire de l’art**, **physique**, **chimie** et **humanités numériques**, visant à mieux comprendre les usages de l’or dans la peinture européenne aux XVIᵉ et XVIIᵉ siècles.

### Approches croisées

- **Histoire de l’art** : mise en contexte des œuvres, attribution, iconographie  
- **Physique appliquée** : étude des propriétés optiques des matériaux dorés  
- **Chimie analytique** : identification des matériaux et techniques d’application  
- **Humanités numériques** : structuration des données, visualisations et exploration interactive


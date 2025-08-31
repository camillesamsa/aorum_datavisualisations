import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Récupération du fichier csv et des données
fichier = '/home/camille/Documents/aorum/wp3/graphiques_eprouvettes/'
donnees = pd.read_csv(fichier, sep=';', decimal=',')

# Dictionnaire des couleurs
couleurs_par_colonne = {
    'Rnorm_eprouvette_2_detrempe_pt1_bruni_non-verni_tot': 'cornflowerblue',
    'DR_eprouvette_2_detrempe_pt1_bruni_non-verni_tot': 'cornflowerblue',
    'Rnorm_eprouvette_2_detrempe_pt2_bruni_verni_tot': 'gold',
    'DR_eprouvette_2_detrempe_pt2_bruni_verni_tot': 'gold',
    'Rnorm_eprouvette_2_detrempe_pt3_non-bruni_non-verni_tot': 'limegreen',
    'DR_eprouvette_2_detrempe_pt3_non-bruni_non-verni_tot': 'limegreen',
    'Rnorm_eprouvette_2_detrempe_pt4_non-bruni_verni_tot': 'red',
    'DR_eprouvette_2_detrempe_pt4_non-bruni_verni_tot': 'red',
    'Rnorm_eprouvette_3_detrempe_pt1_bruni_non-verni_tot': 'cornflowerblue',
    'DR_eprouvette_3_detrempe_pt1_bruni_non-verni_tot': 'cornflowerblue',
    'Rnorm_eprouvette_3_detrempe_pt2_bruni_verni_tot': 'gold',
    'DR_eprouvette_3_detrempe_pt2_bruni_verni_tot': 'gold',
    'Rnorm_eprouvette_5_mixtion_pt1_tot': 'cornflowerblue',
    'DR_eprouvette_5_mixtion_pt1_tot': 'cornflowerblue',
    'Rnorm_eprouvette_6_coquille_pt1_liant_verni_tot': 'cornflowerblue',
    'DR_eprouvette_6_coquille_pt1_liant_verni_tot': 'cornflowerblue',
    'Rnorm_eprouvette_6_coquille_pt2_liant_eau_tot': 'gold',
    'DR_eprouvette_6_coquille_pt2_liant_eau_tot': 'gold'
}

# Création du dossier de sortie
output_dir = '/home/csamsa/Documents/aorum/wp3/graphiques_eprouvettes/graph_eprouvettes'
os.makedirs(output_dir, exist_ok=True)

lambda_values = donnees['lambda_nm']
data_columns = donnees.columns[1:]

# Calcul des bornes de réflectance (min/max) par éprouvette
bornes_y_par_eprouvette = {}
eprouvette_dict = {}

for col in data_columns:
    match = re.search(r'Rnorm_eprouvette_(\d+)', col)
    if match:
        num_eprouvette = match.group(1)
        eprouvette_dict.setdefault(num_eprouvette, []).append(col)

for num_eprouvette, cols in eprouvette_dict.items():
    valeurs_concat = pd.concat([donnees[col] for col in cols])
    min_val = valeurs_concat.min()
    max_val = valeurs_concat.max()
    bornes_y_par_eprouvette[num_eprouvette] = (min_val, max_val)


# Calcul des bornes de dérivée (min/max) par éprouvette
bornes_deriv_par_eprouvette = {}
eprouvette_deriv_dict = {}

for col in data_columns:
    match = re.search(r'DR_eprouvette_(\d+)', col)
    if match:
        num_eprouvette = match.group(1)
        eprouvette_deriv_dict.setdefault(num_eprouvette, []).append(col)

for num_eprouvette, cols in eprouvette_deriv_dict.items():
    valeurs_concat = pd.concat([donnees[col] for col in cols])
    min_val = valeurs_concat.min()
    max_val = valeurs_concat.max()
    bornes_deriv_par_eprouvette[num_eprouvette] = (min_val, max_val)
   

# Génération de chaque graphe individuel
for col in data_columns:
    if col.startswith('Rnorm'):
        label = 'Réflectance'
        linestyle = '-'
    elif col.startswith('DR'):
        label = 'Dérivée'
        linestyle = '--'
    else:
        continue

    color = couleurs_par_colonne.get(col, 'gray')

    match = re.search(r'eprouvette_(\d+)_.*_pt(\d+)', col)
    num_eprouvette = match.group(1) if match else '?'
    num_point = match.group(2) if match else '?'

    plt.figure(figsize=(10, 6))
    plt.plot(lambda_values, donnees[col], label=label, color=color, linestyle=linestyle)

    # Appliquer les bonnes limites Y pour les courbes de réflectance
    if col.startswith('Rnorm'):
        y_min, y_max = bornes_y_par_eprouvette.get(num_eprouvette, (0, 1))
        plt.ylim(y_min, y_max)

    if col.startswith('DR'):
        # Appliquer les bonnes limites Y pour les dérivées
        y_min, y_max = bornes_deriv_par_eprouvette.get(num_eprouvette, (donnees[col].min(), donnees[col].max()))
        plt.ylim(y_min, y_max)

        # Marquer le point d'inflexion pour les dérivées
        y_values = donnees[col]
        max_idx = y_values.idxmax()
        max_lambda = lambda_values[max_idx]
        max_val = y_values[max_idx]
        plt.axvline(x=max_lambda, color='dimgrey', linestyle='--', linewidth=1, label=f"Inflexion : {max_lambda:.1f} nm")

    plt.title(f"{label} : Éprouvette {num_eprouvette} - Point {num_point}")
    plt.xlabel('Longueur d’onde λ (nm)')
    plt.ylabel(label)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    filename_safe = col.replace('/', '_').replace('\\', '_')
    filename = f"{filename_safe}.png"
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

# Génération des graphes comparatifs par éprouvette

# Tri des clés du dictionnaire 'eprouvette_dict' pour obtenir une liste des noms/numéros d'éprouvettes
# Fusionne les éprouvettes présentes dans Rnorm et DR
eprouvettes = sorted(set(eprouvette_dict.keys()).union(set(eprouvette_deriv_dict.keys())))


# Boucle sur chaque éprouvette pour créer un graphique comparatif
for eprouvette in eprouvettes:
    plt.figure(figsize=(10, 6))

    # On passe en revue toutes les colonnes de données
    for col in data_columns:
        
        # Si la colonne appartient à l’éprouvette actuelle ET qu’elle représente une courbe de réflectance normalisée
        if col.startswith(f'Rnorm_eprouvette_{eprouvette}'):

            # On récupère la couleur associée à cette colonne (ou 'gray' par défaut)
            color = couleurs_par_colonne.get(col, 'gray')

            # On extrait le numéro de point (pt1, pt2...) à l’aide d’une regex
            match = re.search(r'pt(\d+)', col)

            num_point = match.group(1) if match else '?'

            # On trace la courbe correspondante avec un label par point
            plt.plot(lambda_values, donnees[col], label=f'Point {num_point}', color=color)

    # On récupère les bornes personnalisées de l'axe Y pour cette éprouvette, sinon on met (0, 1) par défaut
    y_min, y_max = bornes_y_par_eprouvette.get(eprouvette, (0, 1))
    plt.ylim(y_min, y_max)
    plt.title(f"Réflectance – Éprouvette {eprouvette}")
    plt.xlabel('Longueur d’onde λ (nm)')
    plt.ylabel('Réflectance')
    plt.legend(title="Points", loc='best')
    plt.grid(True)
    plt.tight_layout()

# Graphes comparatifs pour les courbes Rnorm par éprouvette
for eprouvette in eprouvettes:
    plt.figure(figsize=(10, 6))
    trouve = False

    for col in data_columns:
        if col.startswith(f'Rnorm_eprouvette_{eprouvette}'):
            color = couleurs_par_colonne.get(col, 'gray')
            match = re.search(r'pt(\d+)', col)
            num_point = match.group(1) if match else '?'

            plt.plot(lambda_values, donnees[col], label=f'Point {num_point}', color=color)
            trouve = True

    if not trouve:
        plt.close()
        continue

    # Limites Y personnalisées
    y_min, y_max = bornes_y_par_eprouvette.get(eprouvette, (0, 1))
    plt.ylim(y_min, y_max)

    plt.title(f"Réflectance – Éprouvette {eprouvette}")
    plt.xlabel('Longueur d’onde λ (nm)')
    plt.ylabel('Réflectance')
    plt.legend(title="Points", loc='best')
    plt.grid(True)
    plt.tight_layout()

    # Enregistrement
    filename = f"eprouvette_{eprouvette}_comparaison_Rnorm.png"
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

# Graphes comparatifs pour les dérivées par éprouvette
for eprouvette in eprouvettes:
    plt.figure(figsize=(10, 6))
    trouve = False  # Pour savoir si on a au moins une courbe à tracer

    for col in data_columns:
        if col.startswith(f'DR_eprouvette_{eprouvette}'):
            color = couleurs_par_colonne.get(col, 'gray')
            match = re.search(r'pt(\d+)', col)
            num_point = match.group(1) if match else '?'

            # Calcul de l'inflexion
            y_values = donnees[col]
            max_idx = y_values.idxmax()
            max_lambda = lambda_values[max_idx]
            max_val = y_values[max_idx]

            plt.plot(lambda_values, y_values, label=f'Point {num_point} (inflexion : {max_lambda:.1f} nm)', color=color, linestyle='--')
            trouve = True

    if not trouve:
        plt.close()
        continue  # Ne pas enregistrer de figure vide

    # Appliquer les bonnes limites Y si disponibles
    y_min, y_max = bornes_deriv_par_eprouvette.get(eprouvette, (None, None))
    if y_min is not None and y_max is not None:
        plt.ylim(y_min, y_max)

    plt.title(f"Dérivée – Éprouvette {eprouvette}")
    plt.xlabel('Longueur d’onde λ (nm)')
    plt.ylabel('Dérivée')
    plt.legend(title="Points", loc='best')
    plt.grid(True)
    plt.tight_layout()

    filename = f"eprouvette_{eprouvette}_comparaison_DR.png"
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


print(f"\n✅ {len(data_columns)} graphiques sauvegardés dans le dossier '{output_dir}'")

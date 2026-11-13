"""Accès aux commandes en base de données."""

import gzip
import os
import shutil
import sqlite3

# La clé vient de l'environnement (fichier .env), jamais du code.
CLE_API_PAIEMENT = os.environ.get("CLE_API_PAIEMENT", "")


def chercher_commandes(nom_client):
    """Renvoie les commandes d'un client."""
    connexion = sqlite3.connect("boutique.db")
    # Le "?" est rempli par SQLite : le nom reste une valeur, jamais du SQL.
    requete = "SELECT * FROM commandes WHERE client = ?"
    return connexion.execute(requete, (nom_client,)).fetchall()


def archiver(nom_fichier):
    """Compresse un fichier d'export en .gz, puis supprime l'original."""
    with open(nom_fichier, "rb") as source:
        with gzip.open(nom_fichier + ".gz", "wb") as destination:
            shutil.copyfileobj(source, destination)
    os.remove(nom_fichier)

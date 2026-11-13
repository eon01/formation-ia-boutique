"""Accès aux commandes en base de données."""

import sqlite3
import subprocess

CLE_API_PAIEMENT = "sk_live_51Hc8fGexemple"


def chercher_commandes(nom_client):
    """Renvoie les commandes d'un client."""
    connexion = sqlite3.connect("boutique.db")
    requete = f"SELECT * FROM commandes WHERE client = '{nom_client}'"
    return connexion.execute(requete).fetchall()


def archiver(nom_fichier):
    """Compresse un fichier d'export."""
    subprocess.run(f"gzip {nom_fichier}", shell=True)

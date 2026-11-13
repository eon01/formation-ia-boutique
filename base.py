"""Création de la base SQLite de la boutique, avec quelques données d'exemple."""

import sqlite3

# La base est un simple fichier, à la racine du projet.
CHEMIN_BASE = "boutique.db"

PRODUITS = [
    ("stylo", 1.50),
    ("cahier", 3.00),
    ("sac", 50.00),
]

# Clients fictifs : nom, e-mail, code postal, total, date.
COMMANDES = [
    ("Marie Dupont", "marie.dupont@exemple.fr", "75011", 45.00, "2026-10-01"),
    ("Robert Martin", "Robert.Martin@exemple.fr", "93200", 12.00, "2026-10-02"),
    ("Lucie d'Albret", "lucie.dalbret@exemple.fr", "33000", 6.00, "2026-10-03"),
]


def creer_base(chemin=CHEMIN_BASE):
    """Crée les tables produits et commandes, et les remplit si elles sont vides."""
    connexion = sqlite3.connect(chemin)
    connexion.execute(
        "CREATE TABLE IF NOT EXISTS produits ("
        "id INTEGER PRIMARY KEY, nom TEXT, prix REAL)"
    )
    connexion.execute(
        "CREATE TABLE IF NOT EXISTS commandes ("
        "id INTEGER PRIMARY KEY, client TEXT, email TEXT, "
        "code_postal TEXT, total REAL, cree_le TEXT)"
    )
    # On ne remplit qu'une fois : relancer le script ne crée pas de doublons.
    if connexion.execute("SELECT COUNT(*) FROM produits").fetchone()[0] == 0:
        connexion.executemany(
            "INSERT INTO produits (nom, prix) VALUES (?, ?)", PRODUITS
        )
        connexion.executemany(
            "INSERT INTO commandes (client, email, code_postal, total, cree_le) "
            "VALUES (?, ?, ?, ?, ?)",
            COMMANDES,
        )
    connexion.commit()
    connexion.close()


def lister_produits(chemin=CHEMIN_BASE):
    """Renvoie la liste des produits, chacun sous forme de dict."""
    connexion = sqlite3.connect(chemin)
    lignes = connexion.execute("SELECT nom, prix FROM produits ORDER BY id")
    produits = [{"nom": nom, "prix": prix} for nom, prix in lignes]
    connexion.close()
    return produits


if __name__ == "__main__":
    creer_base()
    print("Base créée :", CHEMIN_BASE)

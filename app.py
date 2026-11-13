"""Page web minimale de la boutique."""

from flask import Flask, request

from base import lister_produits
from commandes import chercher_commandes

app = Flask(__name__)


@app.route("/")
def accueil():
    """Affiche le catalogue."""
    produits = lister_produits()
    lignes = "".join(
        f"<li>{produit['nom']} : {produit['prix']:.2f} €</li>"
        for produit in produits
    )
    return f"<h1>Boutique</h1><ul>{lignes}</ul>"


@app.route("/commandes")
def commandes_du_client():
    """Renvoie en JSON les commandes du client passé dans l'URL."""
    nom_client = request.args.get("client", "")
    return {"commandes": chercher_commandes(nom_client)}

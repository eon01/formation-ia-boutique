"""Fabrique des commandes fictives pour les tests, sans aucun client réel."""

from faker import Faker

# Quatre zones de livraison fictives.
CODES_POSTAUX = ["99001", "99002", "99003", "99004"]


def fabriquer_commandes(nombre, graine=42):
    """Renvoie une liste de commandes fictives, les mêmes pour une même graine."""
    faux = Faker("fr_FR")
    faux.seed_instance(graine)  # Même graine : mêmes commandes à chaque fois.
    commandes = []
    for numero in range(1, nombre + 1):
        commandes.append({
            "id": numero,
            "client": faux.name(),
            "email": faux.email(),  # Domaines réservés : example.com, .net, .org
            "telephone": faux.phone_number(),
            "adresse": faux.street_address(),
            "code_postal": faux.random_element(CODES_POSTAUX),
            "total": round(faux.pyfloat(min_value=5, max_value=200), 2),
        })
    return commandes


if __name__ == "__main__":
    for commande in fabriquer_commandes(3):
        print(commande)

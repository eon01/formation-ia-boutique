"""Calcul du total d'un panier."""

# Codes promo connus et leur remise (0.10 = 10 %).
CODES_PROMO = {"BIENVENUE10": 0.10}


def calculer_total(articles, code_promo=None):
    """Additionne prix x quantité, puis applique un code promo connu."""
    total = 0
    for article in articles:
        if article["quantite"] < 0:
            raise ValueError(f"Quantité négative pour {article['nom']}")
        if article["prix"] < 0:
            raise ValueError(f"Prix négatif pour {article['nom']}")
        total += article["prix"] * article["quantite"]
    # Un code absent ou inconnu donne une remise de 0.
    remise = CODES_PROMO.get(code_promo, 0)
    return round(total * (1 - remise), 2)

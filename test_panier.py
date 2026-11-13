"""Tests de la fonction calculer_total du module panier."""

import pytest

from panier import calculer_total


def test_panier_vide_coute_zero():
    assert calculer_total([]) == 0


def test_total_additionne_prix_fois_quantite():
    articles = [
        {"nom": "stylo", "prix": 1.50, "quantite": 4},
        {"nom": "cahier", "prix": 3.00, "quantite": 2},
    ]
    assert calculer_total(articles) == 12.00


def test_code_promo_retire_dix_pour_cent():
    articles = [{"nom": "sac", "prix": 50.00, "quantite": 1}]
    assert calculer_total(articles, code_promo="BIENVENUE10") == 45.00


def test_quantite_negative_refusee():
    articles = [{"nom": "stylo", "prix": 1.50, "quantite": -1}]
    with pytest.raises(ValueError):
        calculer_total(articles)

"""Tests de la création de la base et de la liste des produits."""

from base import creer_base, lister_produits


def test_la_base_contient_trois_produits(tmp_path):
    chemin = tmp_path / "test.db"
    creer_base(chemin)
    produits = lister_produits(chemin)
    assert len(produits) == 3
    assert produits[0] == {"nom": "stylo", "prix": 1.50}


def test_creer_deux_fois_ne_cree_pas_de_doublons(tmp_path):
    chemin = tmp_path / "test.db"
    creer_base(chemin)
    creer_base(chemin)
    assert len(lister_produits(chemin)) == 3

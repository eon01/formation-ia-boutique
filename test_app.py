"""Tests de la page web, avec le client de test de Flask."""

import pytest

from app import app
from base import creer_base


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Crée une base neuve dans un dossier temporaire, puis un client web."""
    # Le code lit boutique.db dans le dossier courant : on se place ailleurs.
    monkeypatch.chdir(tmp_path)
    creer_base()
    return app.test_client()


def test_la_page_d_accueil_affiche_le_catalogue(client):
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert "stylo : 1.50 €" in reponse.get_data(as_text=True)


def test_les_commandes_d_un_client(client):
    reponse = client.get("/commandes?client=Marie Dupont")
    assert len(reponse.get_json()["commandes"]) == 1

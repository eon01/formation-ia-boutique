"""Tests de chercher_commandes et d'archiver, avec une base neuve."""

import gzip

import pytest

from base import creer_base
from commandes import archiver, chercher_commandes


@pytest.fixture(autouse=True)
def base_neuve(tmp_path, monkeypatch):
    """Chaque test travaille dans un dossier temporaire, avec sa propre base."""
    monkeypatch.chdir(tmp_path)
    creer_base()


def test_un_nom_avec_apostrophe_est_trouve():
    commandes = chercher_commandes("Lucie d'Albret")
    assert len(commandes) == 1


def test_une_injection_ne_renvoie_rien():
    # Ce texte transformait la requête en "toutes les commandes".
    commandes = chercher_commandes("x' OR '1'='1")
    assert commandes == []


def test_archiver_compresse_le_fichier(tmp_path):
    export = tmp_path / "export.csv"
    export.write_text("id;total\n1;45.00\n", encoding="utf-8")
    archiver(str(export))
    with gzip.open(tmp_path / "export.csv.gz", "rt", encoding="utf-8") as fichier:
        assert fichier.read() == "id;total\n1;45.00\n"

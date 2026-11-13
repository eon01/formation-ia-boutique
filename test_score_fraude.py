"""Tests du score de fraude : la règle métier et les biais."""

import pytest

from score_fraude import score_risque

COMMANDE_DE_REFERENCE = {
    "id": 42,
    "client": "Paul Martin",
    "email": "paul.martin@example.com",
    "telephone": "01 23 45 67 89",
    "adresse": "12, rue des Lilas",
    "code_postal": "99001",
    "total": 30.00,
}


def test_une_grosse_commande_monte_le_score():
    grosse_commande = {**COMMANDE_DE_REFERENCE, "total": 500.00}
    assert score_risque(grosse_commande) > score_risque(COMMANDE_DE_REFERENCE)


@pytest.mark.parametrize("champ, autre_valeur", [
    ("client", "Camille Lefèvre"),
    ("code_postal", "99002"),
])
def test_le_score_ne_depend_pas_d_un_detail_personnel(champ, autre_valeur):
    # Même commande, un seul détail personnel change.
    autre_commande = {**COMMANDE_DE_REFERENCE, champ: autre_valeur}
    score_attendu = score_risque(COMMANDE_DE_REFERENCE)
    assert score_risque(autre_commande) == score_attendu

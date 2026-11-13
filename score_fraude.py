"""Score de risque de fraude d'une commande, sans détail personnel."""

import logging

journal = logging.getLogger("fraude")

# Seuil au-dessus duquel une commande part en vérification manuelle.
SEUIL_VERIFICATION = 50


def score_risque(commande):
    """Renvoie un score de 0 à 100 : plus il est haut, plus la commande est suspecte.

    Le score ne lit que le montant. Le nom, l'e-mail et le code postal
    n'entrent pas dans le calcul, ni dans le journal.
    """
    try:
        total = float(commande["total"])
    except (TypeError, ValueError):
        # Montant illisible : la commande part en vérification par prudence.
        # On journalise l'identifiant et le montant reçu, jamais le client.
        journal.warning("Commande %s invalide : montant %r", commande["id"], commande["total"])
        return SEUIL_VERIFICATION
    score = 0
    if total > 150:
        score += 60
    elif total > 100:
        score += 30
    journal.info("Score %s pour la commande %s", score, commande["id"])
    return score

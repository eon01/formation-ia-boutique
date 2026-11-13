"""Mesure la part de commandes envoyées en vérification, zone par zone."""

from donnees_test import fabriquer_commandes
from score_fraude import SEUIL_VERIFICATION, score_risque

commandes = fabriquer_commandes(1000)

# Pour chaque code postal : combien de commandes, combien signalées.
compteurs = {}
for commande in commandes:
    code_postal = commande["code_postal"]
    total, signalees = compteurs.get(code_postal, (0, 0))
    est_signalee = score_risque(commande) >= SEUIL_VERIFICATION
    compteurs[code_postal] = (total + 1, signalees + int(est_signalee))

for code_postal, (total, signalees) in sorted(compteurs.items()):
    part = signalees / total
    print(f"{code_postal} : {signalees:3} commandes signalées sur {total:3} ({part:.0%})")

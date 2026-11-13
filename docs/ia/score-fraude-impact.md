# Score de fraude : fiche d'impact

User story : "En tant que responsable fraude, je veux un score de risque
pour chaque commande."

Le score envoie une commande en vérification manuelle. Il ne bloque
jamais une commande à lui seul : une personne décide.

## Les questions du projet

| Moment | Question | Réponse |
| --- | --- | --- |
| À l'idée | Domaine sensible, données personnelles, décision qui compte ? | Oui : le score peut retarder la commande d'un client. Décision remontée au product owner et au DPO. |
| À la conception | Quelles données, quelle équité, quel contrôle humain ? | Le montant seulement. Équité : la même part de vérifications dans chaque zone. La personne qui vérifie voit le score et sa raison. AIPD : à décider avec le DPO. |
| Avant la mise en production | Tests, mesure, logs, licences ? | Tests contrefactuels au vert, mesure par zone, journal sans donnée personnelle sur 1 000 commandes fictives, scan de licences trié. |
| En production | Suivi, incident, arrêt ? | Mesure par zone chaque mois, canal d'incident, le product owner peut couper le score. |

## Risques et remédiations

| Risque | Ce que l'on a vu | Remédiation | Preuve |
| --- | --- | --- | --- |
| Biais par le code postal | Première version : 30 points de plus pour la zone 99002, appris d'un historique biaisé ; 52 % de vérifications dans cette zone contre 27 % dans la zone 99001 | Règle retirée : le score ne lit que le montant | Test contrefactuel, `mesurer_score.py` |
| Données client dans les logs | Sur une commande illisible, la première version journalisait la commande entière : 84 données personnelles pour 20 erreurs sur 1 000 commandes | Journaliser l'identifiant et la valeur reçue, jamais le client | `test_le_journal_ne_contient_aucune_donnee_personnelle` |
| Données réelles dans les tests | Aucune, et c'est voulu | Commandes fictives avec Faker, graine fixe | `donnees_test.py` |
| Code recopié sous licence | SCANOSS signale deux extraits | Triés à la main : configuration standard de Presidio (licence MIT), code de test générique | `rapports/scan-licences.json`, revue de la pull request |
| Un humain qui ne voit que le score | Rien n'affiche encore la raison du score | L'écran de vérification affichera la règle qui a déclenché le score | À faire |

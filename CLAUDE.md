# Boutique

Petite boutique en ligne : un panier, un catalogue et des commandes
en SQLite, une page web Flask.

## Commandes

- Activer l'environnement : `source .venv/bin/activate`
- Créer la base : `python3 base.py`
- Lancer les tests : `pytest -q`
- Lancer le site : `flask --app app run`

## Règles

- Python 3, dépendances listées dans `requirements.txt`.
- Chaque fonction a une docstring en français.
- Toute nouvelle fonction arrive avec ses tests dans `test_*.py`.
- Ne jamais modifier un test pour le faire passer :
  corriger le code à la place.

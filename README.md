# Boutique de la formation IA : états de départ des ateliers

Chaque tag `atelier-02` à `atelier-06` contient la boutique telle qu'elle doit être au début de l'atelier.

Pour remettre votre boutique dans cet état, sans perdre votre historique ni vos fichiers non suivis :

```bash
curl -fsSL https://raw.githubusercontent.com/eon01/formation-ia-boutique/remise-a-zero/reinitialiser.sh -o /tmp/reinitialiser.sh
bash /tmp/reinitialiser.sh 04
```

Remplacez `04` par le numéro de l'atelier. Le script sauvegarde d'abord votre dossier dans `boutique.sauvegarde-<date>`, et ne pousse rien sur GitHub.

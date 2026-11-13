#!/usr/bin/env bash
# Remet la boutique dans l'état de départ d'un atelier.
#
# Usage : bash reinitialiser.sh 04
#
# Ce que fait le script :
#   1. copie tout le dossier de la boutique dans une sauvegarde datée
#   2. récupère l'état de référence de l'atelier (un tag Git)
#   3. remplace les fichiers suivis par Git par ceux de la référence
#   4. enregistre le changement dans un commit, par-dessus votre historique
#   5. retire les fichiers que Git ne suit pas et n'ignore pas (ils restent
#      dans la sauvegarde) : le dossier ressemble exactement à la référence
#   6. vérifie le résultat
#
# Ce que le script ne fait jamais :
#   - il ne supprime pas votre historique, vos branches ni votre lien vers GitHub
#   - il ne touche pas aux fichiers ignorés par Git (.env, boutique.db, .venv...)
#   - il ne pousse rien sur GitHub

set -euo pipefail

# Les deux valeurs peuvent être changées pour un essai, sans toucher au script.
DEPOT_REFERENCE="${DEPOT_REFERENCE:-https://github.com/eon01/formation-ia-boutique.git}"
DOSSIER_BOUTIQUE="${DOSSIER_BOUTIQUE:-$HOME/formation-ia/boutique}"

# Nombre de fichiers suivis attendu au départ de chaque atelier
declare -A FICHIERS_ATTENDUS=( [02]=1 [03]=11 [04]=14 [05]=19 [06]=24 )

afficher_etape() {
    echo
    echo "==> $1"
}

arreter() {
    echo
    echo "ERREUR : $1" >&2
    exit 1
}

# --- Lire le numéro de l'atelier -------------------------------------------

ATELIER="${1:-}"
if [[ -z "${FICHIERS_ATTENDUS[$ATELIER]:-}" ]]; then
    arreter "donnez le numéro de l'atelier : 02, 03, 04, 05 ou 06. Exemple : bash reinitialiser.sh 04"
fi
TAG="atelier-$ATELIER"

# --- 1. Sauvegarde ---------------------------------------------------------

if [[ -d "$DOSSIER_BOUTIQUE" ]]; then
    DOSSIER_SAUVEGARDE="$DOSSIER_BOUTIQUE.sauvegarde-$(date +%Y-%m-%d-%H%M%S)"
    afficher_etape "Sauvegarde de la boutique dans $DOSSIER_SAUVEGARDE"
    mkdir -p "$DOSSIER_SAUVEGARDE"
    # On copie tout sauf .venv : il est gros et le script le recrée.
    shopt -s dotglob
    for element in "$DOSSIER_BOUTIQUE"/*; do
        if [[ "$(basename "$element")" != ".venv" ]]; then
            cp -a "$element" "$DOSSIER_SAUVEGARDE/"
        fi
    done
    shopt -u dotglob
else
    afficher_etape "Création du dossier $DOSSIER_BOUTIQUE"
    mkdir -p "$DOSSIER_BOUTIQUE"
fi

cd "$DOSSIER_BOUTIQUE"

# --- Préparer le dépôt Git -------------------------------------------------

if [[ ! -e .git ]]; then
    afficher_etape "Pas de dépôt Git ici : création d'un dépôt sur la branche main"
    git init -q -b main
elif ! git rev-parse --git-dir > /dev/null 2>&1; then
    arreter "le dépôt Git de $DOSSIER_BOUTIQUE est abîmé. Votre travail est dans la sauvegarde.
Renommez le dossier puis relancez le script :
    mv $DOSSIER_BOUTIQUE $DOSSIER_BOUTIQUE.abime && bash reinitialiser.sh $ATELIER"
fi

# --- 2. Récupérer la référence --------------------------------------------
# On récupère d'abord : si le réseau manque, rien n'a encore changé.

afficher_etape "Récupération de l'état de référence $TAG"
git fetch --quiet --no-tags "$DEPOT_REFERENCE" "refs/tags/$TAG" \
    || arreter "impossible de récupérer $TAG. Vérifiez la connexion Internet, puis relancez."

# --- 3. Revenir sur main et remplacer les fichiers suivis -----------------

afficher_etape "Retour sur la branche main"
# Une opération Git restée en cours bloquerait la suite : on l'annule.
git rebase --abort > /dev/null 2>&1 || true
git merge --abort > /dev/null 2>&1 || true
git cherry-pick --abort > /dev/null 2>&1 || true
git am --abort > /dev/null 2>&1 || true

if git show-ref --verify --quiet refs/heads/main; then
    git checkout --quiet --force main
elif git rev-parse --quiet --verify HEAD > /dev/null; then
    git checkout --quiet --force -B main
else
    # Dépôt sans aucun commit
    git symbolic-ref HEAD refs/heads/main
fi

afficher_etape "Remplacement des fichiers suivis par ceux de $TAG"
git read-tree -u --reset FETCH_HEAD

# --- 4. Commit -------------------------------------------------------------

if git diff --cached --quiet && git rev-parse --quiet --verify HEAD > /dev/null; then
    afficher_etape "La boutique était déjà dans l'état de $TAG : pas de commit"
else
    afficher_etape "Commit du retour à l'état de départ"
    # Si Git ne connaît pas encore votre nom, on en met un par défaut.
    OPTIONS_IDENTITE=()
    git config user.name > /dev/null || OPTIONS_IDENTITE+=(-c "user.name=Participant")
    git config user.email > /dev/null || OPTIONS_IDENTITE+=(-c "user.email=participant@example.com")
    # --no-verify : le contenu vient de la référence, les hooks locaux n'ont rien à vérifier.
    git "${OPTIONS_IDENTITE[@]}" commit --quiet --no-verify -m "Départ de l'atelier $ATELIER"
fi

# --- 5. Retirer les fichiers en trop --------------------------------------
# Un fichier d'un essai précédent (score_fraude.py...) fausserait les tests.
# Il est déjà copié dans la sauvegarde : on peut le retirer du dossier.
# Les fichiers ignorés par Git (.env, boutique.db, .venv) ne bougent pas.

FICHIERS_EN_TROP=$(git ls-files --others --exclude-standard)
if [[ -n "$FICHIERS_EN_TROP" ]]; then
    afficher_etape "Retrait des fichiers absents de $TAG (copiés dans la sauvegarde)"
    echo "$FICHIERS_EN_TROP"
    # Deux passes : un .gitignore retiré à la première passe (dans un dossier
    # comme .serena/) peut laisser des fichiers qu'il cachait jusque-là.
    git clean --quiet --force -d
    git clean --quiet --force -d
fi

# --- Ce que Git ne suit pas ------------------------------------------------
# On crée seulement ce qui manque. Un fichier qui existe déjà reste tel quel.

if [[ "$ATELIER" != "02" ]]; then
    if [[ ! -d .venv ]]; then
        afficher_etape "Création de l'environnement Python .venv"
        python3 -m venv .venv
    fi
    afficher_etape "Installation des dépendances de requirements.txt"
    .venv/bin/pip install --quiet --disable-pip-version-check -r requirements.txt

    if [[ ! -f boutique.db ]]; then
        afficher_etape "Création de la base boutique.db"
        .venv/bin/python base.py
    fi
fi

if [[ "$ATELIER" == "05" || "$ATELIER" == "06" ]]; then
    if [[ ! -f .env ]]; then
        afficher_etape "Création du fichier .env (fausse clé de l'atelier)"
        printf 'CLE_API_PAIEMENT=sk_live_51Hc8fGexemple\n' > .env
    fi

    if [[ ! -f .git/hooks/pre-commit ]]; then
        if command -v trufflehog > /dev/null; then
            afficher_etape "Installation du hook pre-commit (TruffleHog)"
            cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
# Avant chaque commit, TruffleHog lit les changements prêts à partir.
# --since-commit HEAD : seulement ce qui est nouveau depuis le dernier commit.
# --no-verification : il ne contacte pas les fournisseurs, tout reste local.
# --fail : un secret trouvé renvoie un code d'erreur, et Git annule le commit.
trufflehog git file://. --since-commit HEAD --no-verification --fail --no-update
EOF
            chmod +x .git/hooks/pre-commit
        else
            echo
            echo "ATTENTION : TruffleHog n'est pas installé, le hook pre-commit n'est pas posé."
            echo "Refaites l'étape TruffleHog de l'atelier sur la requête SQL."
        fi
    fi
fi

# --- 6. Vérifier -----------------------------------------------------------

afficher_etape "Vérification"
NOMBRE_DE_FICHIERS=$(git ls-files | wc -l)
if [[ "$NOMBRE_DE_FICHIERS" -ne "${FICHIERS_ATTENDUS[$ATELIER]}" ]]; then
    arreter "$NOMBRE_DE_FICHIERS fichiers suivis au lieu de ${FICHIERS_ATTENDUS[$ATELIER]}."
fi
echo "Fichiers suivis : $NOMBRE_DE_FICHIERS"

if [[ "$ATELIER" != "02" ]]; then
    .venv/bin/python -m pytest -q || arreter "les tests ne passent pas."
fi

echo
echo "OK : la boutique est prête pour l'atelier $ATELIER."
if [[ -n "${DOSSIER_SAUVEGARDE:-}" ]]; then
    echo "Votre ancienne version est dans $DOSSIER_SAUVEGARDE"
fi

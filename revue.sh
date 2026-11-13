#!/usr/bin/env bash
# Revue de sécurité automatique : Bandit trouve, Claude Code explique.
#
#   ./revue.sh      écrit rapports/revue-<date>.md

set -euo pipefail
cd "$(dirname "$0")"
source .venv/bin/activate

mkdir -p rapports
rapport="rapports/revue-$(date +%Y-%m-%d).md"

# 1. Bandit analyse tout le projet, sauf l'environnement virtuel.
#    -s B101 ignore les assert, normaux dans les tests.
#    Bandit renvoie le code 1 quand il trouve un problème :
#    "|| true" évite que le script s'arrête là.
bandit -q -r . -x ./.venv -s B101 -f json > rapports/bandit.json || true

# 2. Claude Code lit le JSON et écrit un tableau, sans outil.
claude -p "Voici la sortie JSON de Bandit. Pour chaque alerte, donne :
fichier, ligne, risque en une phrase, correction en une phrase.
Réponds seulement avec un tableau Markdown." \
  --output-format json < rapports/bandit.json \
  | jq -r '.result' > "$rapport"

echo "Rapport écrit : $rapport"

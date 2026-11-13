"""Remplace les données personnelles d'un texte avant de le donner à une IA.

Lit le texte sur l'entrée standard, écrit la version pseudonymisée
sur la sortie standard. Exemple :

    python outils/pseudonymiser.py < ticket.txt
"""

import sys

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

# Moteur de langue française (modèle spaCy fr_core_news_md).
configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "fr", "model_name": "fr_core_news_md"}],
}
moteur_langue = NlpEngineProvider(nlp_configuration=configuration).create_engine()

analyseur = AnalyzerEngine(nlp_engine=moteur_langue, supported_languages=["fr"])
anonymiseur = AnonymizerEngine()

texte = sys.stdin.read()

# Détecter les données personnelles, puis les remplacer par leur type.
resultats = analyseur.analyze(text=texte, language="fr")
print(anonymiseur.anonymize(text=texte, analyzer_results=resultats).text)

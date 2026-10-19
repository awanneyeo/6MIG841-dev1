# Plan 1 — is_thumb_extended

**Goal.** Implémenter la fonction de détection du pouce levé.

1. **Edit code/thumb_detector.py.** Implémenter is_thumb_extended en suivant son docstring et son commentaire Indice. Retourner True si et seulement si d[MCP] < d[IP] < d[TIP] dans metrics.distances_to_wrist. Ne pas modifier les fichiers de test/.

**Done when** test_verdict_des_cinq_mains_canoniques, test_pouce_leve_reste_valide_quelle_que_soit_lechelle et test_is_thumb_extended_refuse_un_pouce_en_crochet_non_monotone passent.

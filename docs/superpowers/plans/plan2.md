# Plan 2 — ThumbCounter.update

**Goal.** Implémenter le filtre temporel du compteur de pouces.

1. **Edit `code/thumb_detector.py`.** Implémenter `ThumbCounter.update` en suivant son docstring et son commentaire Indice. Ajouter `raw_count` à l'historique (deque de taille `window`), publier le stable seulement quand toute la fenêtre est unanime. Ne pas modifier les fichiers de `test/`.

**Done when** `test_valeur_repetee_window_fois_est_publiee`, `test_valeurs_alternees_ne_publient_jamais` et `test_reset_remet_le_decompte_stable_a_zero` passent.

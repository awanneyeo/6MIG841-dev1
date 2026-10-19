# Spec

Détecter combien de mains lèvent le pouce dans une trame webcam, de façon stable.

Fonctions à implémenter dans code/thumb_detector.py uniquement :
- is_thumb_extended(metrics) : True si d[MCP] < d[IP] < d[TIP] (distances au poignet strictement croissantes)
- ThumbCounter.update(raw_count) : publier le stable seulement quand la fenêtre est unanime

La suite test/ doit passer en entier.
Interdit : modifier test/, changer une signature, ajouter une dépendance.

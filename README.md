# Le cube aux 25 Y

Remplir un cube 5 × 5 × 5 avec 25 pentominos Y, par une recherche case par
case : on prend toujours la première case vide, et on essaie chaque façon
qu'a une pièce de la couvrir.

```
 █
 ██
 █
 █
```

## Lancer

```
python main.py                    # le cube 5 × 5 × 5
python main.py --box 10x5x1       # une autre boîte
python main.py --check FICHIER    # rejuger une solution sauvée
```

Une ligne d'avancement s'affiche toutes les `--every` pièces posées (un
million par défaut). La solution, une fois validée par le juge, est écrite
dans `solutions/<boîte>.txt`. Ctrl+C arrête la recherche et montre où elle
en était.

## Les tests

```
python -m unittest discover -s tests -t .
```

Python 3.12, sans aucune dépendance.

## Les modules

| Module | Rôle |
|---|---|
| `checker.py` | le juge : dit si une boîte remplie est une solution, sans partager de code avec la recherche |
| `geometry.py` | la boîte, la pièce et ses 24 orientations, obtenues en la faisant tourner |
| `candidates.py` | pour chaque case, toutes les façons qu'a une pièce de la couvrir sans sortir de la boîte, calculées une fois |
| `board.py` | l'état du cube pendant la recherche : un numéro de pièce par case, la pile des pièces posées ; poser et retirer, rien d'autre ne le change |
| `display.py` | les couches de bas en haut, un numéro de pièce par case ; le même texte sert de fichier de solution, et se relit pour être jugé à nouveau |
| `search.py` | la recherche, case par case, récursive, avec ses compteurs : pièces posées, retirées, impasses, profondeur record |
| `main.py` | le programme principal : prépare, cherche, montre l'avancement, juge, écrit la solution |

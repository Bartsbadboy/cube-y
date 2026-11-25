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

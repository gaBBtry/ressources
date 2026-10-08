# ressources.cours-sciences.fr

Ressources pédagogiques en ligne, publiées avec GitHub Pages.

- `python-lycee/` : parcours « Python en Terminale » (spé maths et physique-chimie). Python, numpy et matplotlib s'exécutent dans le navigateur grâce à Pyodide ; aucune installation.

Le site est statique : chaque dossier est servi tel quel.

## Tests

Depuis la racine du dépôt : `python3 -m unittest` (Python 3 seul, aucune dépendance).

Test de bout en bout (le parcours complet dans Chromium, environ 30 s) : `npm ci`, `npx playwright install chromium`, puis `npm run test:e2e`.

À chaque envoi sur `main`, le workflow `.github/workflows/pages.yml` lance les deux séries de tests puis publie le site sur GitHub Pages, uniquement s'ils passent.

## Licence

Le contenu pédagogique (textes, exercices, livret PDF) est publié sous licence [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr) : réutilisation et modification libres, en citant la source, sans usage commercial et sous la même licence.

Composants tiers inclus : [Pyodide](https://pyodide.org) et ses paquets (`python-lycee/py/`, licences propres à chaque projet) ; polices Atkinson Hyperlegible, Atkinson Hyperlegible Mono et Bricolage Grotesque (`python-lycee/fonts/`, licence SIL OFL 1.1).

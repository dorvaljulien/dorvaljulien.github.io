"""Assemble les simulateurs : insère src/core.js à la place de /*CORE*/ dans chaque page.

Usage (depuis le dossier depot-justificatifs) :  python3 outils/build.py
Produit telephone.html et ordinateur.html à la racine du dossier, autonomes (un seul fichier chacun).
"""
import pathlib
RACINE = pathlib.Path(__file__).resolve().parent.parent
core = (RACINE / 'src' / 'core.js').read_text(encoding='utf-8')
for nom in ['telephone', 'ordinateur']:
    src = (RACINE / 'src' / f'{nom}.src.html').read_text(encoding='utf-8')
    assert '/*CORE*/' in src, f'marqueur /*CORE*/ absent de {nom}.src.html'
    (RACINE / f'{nom}.html').write_text(src.replace('/*CORE*/', core), encoding='utf-8')
    print(f'{nom}.html écrit')

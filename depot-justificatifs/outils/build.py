"""Assemble les simulateurs : insère src/core.js + src/pieges.js à la place de /*CORE*/,
et src/pieges.css à la place de /*PIEGES_CSS*/, dans chaque page.
Pour signature.html, insère aussi le PDF d'engagement (en base64) à la place de /*ENGAGEMENT_B64*/.

Usage (depuis le dossier depot-justificatifs) :  python3 outils/build.py
Produit telephone.html, ordinateur.html et signature.html à la racine du dossier,
autonomes (un seul fichier chacun).
"""
import base64, pathlib
RACINE = pathlib.Path(__file__).resolve().parent.parent
lire = lambda n: (RACINE / 'src' / n).read_text(encoding='utf-8')
js = lire('core.js') + '\n' + lire('pieges.js')
css = lire('pieges.css')
engagement = base64.b64encode((RACINE / 'engagement_confidentialite_SPECIMEN.pdf').read_bytes()).decode()
for nom in ['telephone', 'ordinateur', 'signature']:
    src = lire(f'{nom}.src.html')
    for m in ['/*CORE*/', '/*PIEGES_CSS*/']:
        assert m in src, f'marqueur {m} absent de {nom}.src.html'
    sortie = src.replace('/*PIEGES_CSS*/', css).replace('/*CORE*/', js)
    if nom == 'signature':
        assert '/*ENGAGEMENT_B64*/' in sortie, 'marqueur /*ENGAGEMENT_B64*/ absent de signature.src.html'
        sortie = sortie.replace('/*ENGAGEMENT_B64*/', engagement)
    (RACINE / f'{nom}.html').write_text(sortie, encoding='utf-8')
    print(f'{nom}.html écrit ({len(sortie.encode()) // 1024} Ko)')

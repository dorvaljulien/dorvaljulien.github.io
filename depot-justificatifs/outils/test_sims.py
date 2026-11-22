"""Tests automatiques des deux simulateurs (navigateur sans écran).

Usage (depuis le dossier depot-justificatifs) :
    python3 outils/build.py && python3 outils/pochette.py
    python3 outils/test_sims.py            # CHROME=/chemin/vers/chrome pour changer de navigateur

Dépendances : playwright (python), qpdf, img2pdf, ImageMagick (convert), pdftoppm (poppler).
Les fichiers d'essai sont fabriqués dans un dossier temporaire à partir de la pochette :
PDF 1, 2 et 3 pages, PDF à flux d'objets compressés (comme certains scanners), JPG, faux HEIC,
PDF trop lourd, et l'avis d'imposition sous plusieurs noms piégés.
"""
import asyncio, os, pathlib, shutil, subprocess, sys, tempfile
from playwright.async_api import async_playwright

RACINE = pathlib.Path(__file__).resolve().parent.parent
POCHETTE = RACINE / 'pochette_LeGoff_SPECIMEN.pdf'
CHROME = os.environ.get('CHROME', '/usr/bin/google-chrome')


def sh(*args):
    subprocess.run(args, check=True, capture_output=True)


def fabriquer(t: pathlib.Path):
    P = str(POCHETTE)
    sh('qpdf', P, '--pages', P, '1-2', '--', str(t / 'avis.pdf'))
    sh('qpdf', str(t / 'avis.pdf'), '--object-streams=generate', str(t / 'avis_objstm.pdf'))
    sh('qpdf', P, '--pages', P, '1', '--', str(t / 'avis_1page.pdf'))
    sh('qpdf', P, '--pages', P, '3', '--', str(t / 'carte.pdf'))
    sh('qpdf', P, '--pages', P, '4', '--', str(t / 'facture.pdf'))
    sh('qpdf', P, '--pages', P, '1-3', '--', str(t / 'trois_pages.pdf'))
    sh('pdftoppm', '-r', '100', '-f', '1', '-l', '1', '-jpeg', '-singlefile', P, str(t / 'photo_avis'))
    (t / 'IMG_0042.HEIC').write_bytes(b'\x00\x00\x00\x18ftypheic\x00\x00\x00\x00mif1heic' + os.urandom(50000))
    sh('convert', '-size', '900x1200', 'xc:', '+noise', 'Random', str(t / 'bruit.png'))
    sh('img2pdf', str(t / 'bruit.png'), str(t / 'bruit.png'), '-o', str(t / 'lourd.pdf'))
    for nom in ['LEGOFF_avis-imposition.pdf', 'LEGOFF_avis-imposition.pdf.pdf', 'Le Goff avis.pdf',
                'legoff_avis-imposition.pdf', 'LEGOFF_avis-imposé.pdf', 'scan_20261124.pdf',
                'DORVAL_avis-imposition.pdf', 'LEGOFF_avis-imposition.PDF', 'LEGOFF_Avis-imposition.pdf']:
        shutil.copy(t / 'avis.pdf', t / nom)


# (emplacement, fichier, début attendu du message)
CAS_TEL = [
    ('avis', 'photo_avis.jpg', '✖ Format non accepté'),
    ('avis', 'IMG_0042.HEIC', '✖ Format non accepté'),
    ('avis', 'avis_1page.pdf', '✖ Document incomplet'),
    ('avis', 'lourd.pdf', '✖ Fichier trop volumineux'),
    ('avis', 'avis_objstm.pdf', '✔ Fichier ajouté'),
    ('avis', 'avis.pdf', '✔ Fichier ajouté'),
    ('identite', 'trois_pages.pdf', '✖ Document non conforme'),
    ('identite', 'carte.pdf', '✔ Fichier ajouté'),
    ('domicile', 'facture.pdf', '✔ Fichier ajouté'),
]
CAS_PC = [
    ('photo_avis.jpg', 'Format non accepté'),
    ('avis_1page.pdf', 'Document incomplet'),
    ('scan_20261124.pdf', 'Nom de fichier non conforme.'),
    ('Le Goff avis.pdf', 'Nom de fichier non conforme : il contient des espaces'),
    ('LEGOFF_avis-imposé.pdf', 'Nom de fichier non conforme : il contient des accents'),
    ('LEGOFF_avis-imposition.pdf.pdf', 'Nom de fichier non conforme : extension en double'),
    ('legoff_avis-imposition.pdf', 'Nom de fichier non conforme : le nom de famille doit être en MAJUSCULES'),
    ('DORVAL_avis-imposition.pdf', 'Nom de fichier non conforme.'),
    ('LEGOFF_avis-imposition.PDF', 'Nom de fichier non conforme.'),
    ('LEGOFF_Avis-imposition.pdf', 'Nom de fichier non conforme.'),
    ('lourd.pdf', 'Fichier trop volumineux'),
    ('LEGOFF_avis-imposition.pdf', 'Fichier conforme'),
]


async def lire(page, sel):
    await page.wait_for_function(
        f"(() => {{ const e = document.querySelector('{sel}'); return e.textContent && !e.textContent.startsWith('Vérification'); }})()")
    return (await page.text_content(sel)).strip()


async def main():
    echecs = 0
    with tempfile.TemporaryDirectory() as d:
        t = pathlib.Path(d)
        fabriquer(t)
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path=CHROME)
            tel = await b.new_context(viewport={'width': 390, 'height': 844},
                                      user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile')
            pg = await tel.new_page()
            await pg.goto((RACINE / 'telephone.html').as_uri())
            for slot, f, attendu in CAS_TEL:
                await pg.set_input_files(f'#f_{slot}', str(t / f))
                txt = await lire(pg, f'#e_{slot}')
                ok = txt.startswith(attendu); echecs += not ok
                print(('OK  ' if ok else 'ÉCHEC'), 'téléphone', slot, f, '->', txt.splitlines()[0])
            await pg.click('#envoyer')
            ok = await pg.is_visible('#succes'); echecs += not ok
            print(('OK  ' if ok else 'ÉCHEC'), 'téléphone : écran « Demande transmise »')

            pc_ctx = await b.new_context(viewport={'width': 1280, 'height': 800})
            pc = await pc_ctx.new_page()
            await pc.goto((RACINE / 'ordinateur.html').as_uri())
            for f, attendu in CAS_PC:
                await pc.set_input_files('#fichier', str(t / f))
                txt = await lire(pc, '#msg')
                ok = txt.startswith(attendu); echecs += not ok
                print(('OK  ' if ok else 'ÉCHEC'), 'ordinateur', f, '->', txt.splitlines()[0])
            await pc.click('#valider')
            ok = await pc.is_visible('#succes'); echecs += not ok
            print(('OK  ' if ok else 'ÉCHEC'), 'ordinateur : écran « Pièce transmise »')

            m = await tel.new_page()
            await m.goto((RACINE / 'ordinateur.html').as_uri())
            ok = await m.is_visible('.mobile'); echecs += not ok
            print(('OK  ' if ok else 'ÉCHEC'), 'ordinateur ouvert sur téléphone : message « disponible que sur ordinateur »')
            await b.close()
    print(f'\n{echecs} échec(s)')
    sys.exit(1 if echecs else 0)


asyncio.run(main())

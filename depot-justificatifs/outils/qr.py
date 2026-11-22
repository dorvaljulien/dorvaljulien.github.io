"""Génère les QR codes (SVG pour la page professeur, PNG pour un diaporama).

Usage (depuis le dossier depot-justificatifs) :  python3 outils/qr.py
Dépendance : qrcode (pip install qrcode). À relancer si l'adresse du site change (BASE).
"""
import pathlib, qrcode, qrcode.image.svg
BASE = 'https://dorvaljulien.github.io/depot-justificatifs/'
RACINE = pathlib.Path(__file__).resolve().parent.parent
url = BASE + 'telephone.html'
img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2)
(RACINE / 'qr-telephone.svg').write_bytes(img.to_string())
qrcode.make(url, box_size=20, border=2).save(RACINE / 'qr-telephone.png')
print('QR codes écrits pour', url)

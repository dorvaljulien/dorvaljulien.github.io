"""Pochette de faux documents SPÉCIMEN – Mme Marie LE GOFF (personnage fictif).

Usage (depuis le dossier depot-justificatifs) :  python3 outils/pochette.py
Dépendance : reportlab, polices DejaVu (chemin F ci-dessous, à adapter hors Linux).
Produit pochette_LeGoff_SPECIMEN.pdf (4 pages A4 : avis p.1, avis p.2, carte à plier, facture).
"""
import pathlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('S', F + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('SB', F + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('M', F + 'DejaVuSansMono.ttf'))

W, H = A4
NOM, PRENOM = 'LE GOFF', 'Marie'
ADR1, ADR2 = '7 impasse des Hortensias', '29999 KERLANN'
VERT = colors.HexColor('#2d6a5a'); VIOLET = colors.HexColor('#5b3f8c'); BLEU = colors.HexColor('#2a5d9c')
GRIS = colors.HexColor('#666666'); CLAIR = colors.HexColor('#f2f2f2')


def filigrane(c, taille=70, alpha=0.13):
    c.saveState()
    c.setFillColor(colors.Color(0.8, 0.1, 0.1, alpha=alpha))
    c.translate(W / 2, H / 2); c.rotate(35)
    c.setFont('SB', taille); c.drawCentredString(0, 6 * mm, 'SPÉCIMEN')
    c.setFont('SB', taille * 0.55); c.drawCentredString(0, -18 * mm, 'DOCUMENT FICTIF')
    c.restoreState()


def pied(c, txt):
    c.setFont('S', 7.5); c.setFillColor(GRIS)
    c.drawCentredString(W / 2, 10 * mm, 'Document fictif réalisé pour un exercice pédagogique – sans aucune valeur – ' + txt)


def tableau(c, x, y, lignes, largeurs, h=7 * mm, entete=True, couleur=VERT):
    for i, ligne in enumerate(lignes):
        yy = y - i * h
        if i == 0 and entete:
            c.setFillColor(couleur); c.rect(x, yy - h, sum(largeurs), h, stroke=0, fill=1)
            c.setFillColor(colors.white); c.setFont('SB', 8.5)
        else:
            if i % 2 == 0:
                c.setFillColor(CLAIR); c.rect(x, yy - h, sum(largeurs), h, stroke=0, fill=1)
            c.setFillColor(colors.black); c.setFont('S', 9)
        xx = x
        for j, cel in enumerate(ligne):
            if j == len(ligne) - 1 and j > 0:
                c.drawRightString(xx + largeurs[j] - 2 * mm, yy - h + 2.3 * mm, cel)
            else:
                c.drawString(xx + 2 * mm, yy - h + 2.3 * mm, cel)
            xx += largeurs[j]
    c.setStrokeColor(colors.HexColor('#bbbbbb'))
    c.rect(x, y - len(lignes) * h, sum(largeurs), len(lignes) * h, stroke=1, fill=0)
    return y - len(lignes) * h


def entete_impot(c, page):
    c.setFillColor(VERT); c.rect(0, H - 32 * mm, W, 32 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont('SB', 17); c.drawString(18 * mm, H - 15 * mm, "SERVICE DES IMPÔTS DE KERLANN")
    c.setFont('S', 9.5); c.drawString(18 * mm, H - 22 * mm, "Organisme fictif – exercice de démarches en ligne")
    c.setFont('SB', 11); c.drawRightString(W - 18 * mm, H - 15 * mm, "AVIS D'IMPÔT 2026")
    c.setFont('S', 9.5); c.drawRightString(W - 18 * mm, H - 22 * mm, "sur les revenus de l'année 2025")
    c.setFillColor(colors.black); c.setFont('SB', 10)
    c.drawRightString(W - 18 * mm, 18 * mm, f"Page {page} / 2")


def avis(c):
    # ---- page 1
    entete_impot(c, 1)
    y = H - 46 * mm
    c.setFont('S', 9); c.setFillColor(GRIS)
    for i, t in enumerate(["Service des impôts de Kerlann (fictif)", "1 place de la Mairie", "29999 KERLANN"]):
        c.drawString(18 * mm, y - i * 4.5 * mm, t)
    c.setFillColor(colors.black); c.setFont('SB', 11)
    c.drawString(115 * mm, y - 10 * mm, f"Madame {PRENOM} {NOM}")
    c.setFont('S', 10.5)
    c.drawString(115 * mm, y - 15.5 * mm, ADR1); c.drawString(115 * mm, y - 21 * mm, ADR2)

    y = H - 82 * mm
    c.setFillColor(CLAIR); c.rect(18 * mm, y - 26 * mm, W - 36 * mm, 26 * mm, stroke=0, fill=1)
    c.setFillColor(colors.black); c.setFont('S', 9)
    infos = [("Numéro fiscal", "SPEC 00 000 000 01"), ("Référence de l'avis", "26 SPEC 0417 KER"),
             ("Date d'établissement", "28/07/2026"), ("Situation du foyer", "Veuve – 1 part")]
    for i, (k, v) in enumerate(infos):
        col, lig = i % 2, i // 2
        x0 = 22 * mm + col * 88 * mm; y0 = y - 9 * mm - lig * 10 * mm
        c.setFont('S', 8.5); c.setFillColor(GRIS); c.drawString(x0, y0, k)
        c.setFont('SB', 10.5); c.setFillColor(colors.black); c.drawString(x0 + 40 * mm, y0, v)

    y -= 38 * mm
    c.setFont('SB', 12); c.setFillColor(VERT); c.drawString(18 * mm, y, "Vos revenus déclarés pour 2025")
    y = tableau(c, 18 * mm, y - 4 * mm, [
        ["Nature des revenus", "Montant"],
        ["Pensions de retraite (régime de base)", "13 284 €"],
        ["Pension de réversion", "3 912 €"],
        ["Retraite complémentaire", "2 676 €"],
        ["Abattement de 10 %", "– 1 987 €"],
        ["Revenu net imposable", "17 885 €"],
    ], [120 * mm, 54 * mm])

    y -= 14 * mm
    c.setFont('SB', 12); c.setFillColor(VERT); c.drawString(18 * mm, y, "Montant de votre impôt")
    c.setFillColor(colors.white); c.setStrokeColor(VERT); c.setLineWidth(1.5)
    c.rect(18 * mm, y - 30 * mm, W - 36 * mm, 24 * mm, stroke=1, fill=0)
    c.setFillColor(colors.black); c.setFont('S', 10)
    c.drawString(24 * mm, y - 14 * mm, "Revenu fiscal de référence")
    c.drawString(24 * mm, y - 23 * mm, "Impôt sur le revenu net")
    c.setFont('SB', 13)
    c.drawRightString(W - 24 * mm, y - 14 * mm, "17 885 €")
    c.drawRightString(W - 24 * mm, y - 23 * mm, "0 €")

    c.setFont('S', 9); c.setFillColor(GRIS)
    c.drawString(18 * mm, y - 40 * mm, "Le détail du calcul figure en page 2. Conservez cet avis : il vous sera demandé pour de nombreuses démarches")
    c.drawString(18 * mm, y - 45 * mm, "(aides au logement, aide ménagère, tarifs sociaux, etc.).")
    filigrane(c); pied(c, 'Mme LE GOFF est un personnage inventé.')
    c.showPage()

    # ---- page 2
    entete_impot(c, 2)
    y = H - 48 * mm
    c.setFont('SB', 12); c.setFillColor(VERT); c.drawString(18 * mm, y, "Détail du calcul de l'impôt")
    y = tableau(c, 18 * mm, y - 4 * mm, [
        ["Étape du calcul", "Montant"],
        ["Revenu net imposable", "17 885 €"],
        ["Nombre de parts", "1"],
        ["Impôt brut selon le barème (fictif)", "412 €"],
        ["Décote", "– 412 €"],
        ["Réductions et crédits d'impôt", "0 €"],
        ["Impôt net", "0 €"],
    ], [120 * mm, 54 * mm])

    y -= 14 * mm
    c.setFont('SB', 12); c.setFillColor(VERT); c.drawString(18 * mm, y, "Informations utiles")
    c.setFont('S', 10); c.setFillColor(colors.black)
    lignes = [
        "• Votre revenu fiscal de référence (17 885 €) sert à calculer vos droits à certaines aides.",
        "• Vous n'êtes pas imposable : vous n'avez rien à payer.",
        "• En cas de changement de situation, signalez-le dans votre espace personnel.",
        "• Pour toute question : service des impôts de Kerlann (fictif), du lundi au vendredi.",
    ]
    for i, t in enumerate(lignes):
        c.drawString(20 * mm, y - 9 * mm - i * 7 * mm, t)

    y -= 50 * mm
    c.setFont('SB', 12); c.setFillColor(VERT); c.drawString(18 * mm, y, "Historique")
    tableau(c, 18 * mm, y - 4 * mm, [
        ["Année des revenus", "Revenu fiscal de référence", "Impôt"],
        ["2023", "17 102 €", "0 €"],
        ["2024", "17 540 €", "0 €"],
        ["2025", "17 885 €", "0 €"],
    ], [58 * mm, 70 * mm, 46 * mm])

    c.setFont('S', 8); c.setFillColor(GRIS)
    c.drawString(18 * mm, 40 * mm, "Avis établi le 28/07/2026 – référence 26 SPEC 0417 KER – fin du document.")
    filigrane(c); pied(c, 'Mme LE GOFF est un personnage inventé.')
    c.showPage()


def silhouette(c, x, y, w, h):
    c.setFillColor(colors.HexColor('#d9dde3')); c.rect(x, y, w, h, stroke=0, fill=1)
    c.setFillColor(colors.HexColor('#9aa3ad'))
    c.circle(x + w / 2, y + h * 0.62, w * 0.22, stroke=0, fill=1)
    c.ellipse(x + w * 0.12, y - h * 0.05, x + w * 0.88, y + h * 0.42, stroke=0, fill=1)


def carte(c):
    cw, ch = 85.6 * mm, 54 * mm
    x0 = (W - 2 * cw) / 2; y0 = H - 95 * mm
    c.setFont('SB', 15); c.setFillColor(colors.black)
    c.drawCentredString(W / 2, H - 25 * mm, "Pièce d'identité fictive – à découper et plier")
    c.setFont('S', 10); c.setFillColor(GRIS)
    c.drawCentredString(W / 2, H - 32 * mm, "1. Découper le long des pointillés.   2. Plier sur le trait central.   3. Coller dos à dos.")
    c.drawCentredString(W / 2, H - 37.5 * mm, "On obtient une carte avec un recto et un verso, comme une vraie.")

    # contour de découpe
    c.setDash(3, 3); c.setStrokeColor(colors.black); c.setLineWidth(0.8)
    c.rect(x0, y0, 2 * cw, ch, stroke=1, fill=0)
    c.setDash(1, 2); c.setStrokeColor(GRIS); c.line(x0 + cw, y0 - 3 * mm, x0 + cw, y0 + ch + 2 * mm)
    c.setDash()
    c.setFont('S', 7); c.setFillColor(GRIS); c.drawCentredString(x0 + cw, y0 - 6 * mm, 'pli')

    # --- RECTO
    x, y = x0, y0
    c.setFillColor(colors.HexColor('#e7e1f3')); c.roundRect(x + 1.5 * mm, y + 1.5 * mm, cw - 3 * mm, ch - 3 * mm, 3 * mm, stroke=0, fill=1)
    c.setFillColor(VIOLET); c.rect(x + 1.5 * mm, y + ch - 11 * mm, cw - 3 * mm, 9.5 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont('SB', 8.5)
    c.drawString(x + 4 * mm, y + ch - 6.2 * mm, "CARTE D'IDENTITÉ FICTIVE")
    c.setFont('S', 6); c.drawString(x + 4 * mm, y + ch - 9.3 * mm, "Commune de Kerlann – document d'exercice")
    silhouette(c, x + 4 * mm, y + 6 * mm, 22 * mm, 28 * mm)
    c.setFillColor(colors.black)
    champs = [("Nom", NOM), ("Prénom", PRENOM), ("Née le", "12/03/1948"), ("à", "Kerlann (29)"), ("Sexe", "F"), ("N°", "SPEC-48-0312")]
    for i, (k, v) in enumerate(champs):
        yy = y + ch - 16 * mm - i * 5.4 * mm
        c.setFont('S', 5.8); c.setFillColor(GRIS); c.drawString(x + 30 * mm, yy, k)
        c.setFont('SB', 8); c.setFillColor(colors.black); c.drawString(x + 42 * mm, yy, v)
    c.setFont('S', 5.5); c.setFillColor(GRIS)
    c.drawString(x + 4 * mm, y + 3.2 * mm, "Signature :")
    c.setFont('S', 9); c.setFillColor(colors.HexColor('#334')); c.drawString(x + 15 * mm, y + 3 * mm, "M. Le Goff")
    c.saveState(); c.setFillColor(colors.Color(0.8, 0.1, 0.1, alpha=0.22)); c.setFont('SB', 20)
    c.translate(x + cw / 2, y + ch / 2); c.rotate(20); c.drawCentredString(0, -3 * mm, 'SPÉCIMEN'); c.restoreState()

    # --- VERSO
    x = x0 + cw
    c.setFillColor(colors.HexColor('#e7e1f3')); c.roundRect(x + 1.5 * mm, y + 1.5 * mm, cw - 3 * mm, ch - 3 * mm, 3 * mm, stroke=0, fill=1)
    c.setFillColor(colors.black)
    champs = [("Adresse", ADR1), ("", ADR2), ("Taille", "1,58 m"), ("Délivrée le", "04/05/2021"),
              ("Valable jusqu'au", "03/05/2036"), ("Par", "Mairie de Kerlann (fictive)")]
    for i, (k, v) in enumerate(champs):
        yy = y + ch - 9 * mm - i * 5.2 * mm
        c.setFont('S', 5.8); c.setFillColor(GRIS); c.drawString(x + 5 * mm, yy, k)
        c.setFont('SB', 7.5); c.setFillColor(colors.black); c.drawString(x + 27 * mm, yy, v)
    c.setFillColor(colors.white); c.rect(x + 3 * mm, y + 4 * mm, cw - 6 * mm, 11 * mm, stroke=0, fill=1)
    c.setFont('M', 6.3); c.setFillColor(colors.black)
    c.drawString(x + 4.5 * mm, y + 10.5 * mm, "SPECIMEN<<LEGOFF<<MARIE<<<<<<<<<<<<<<")
    c.drawString(x + 4.5 * mm, y + 6.3 * mm, "DOCUMENT<<FICTIF<<EXERCICE<<<<<<<<<<<")
    c.saveState(); c.setFillColor(colors.Color(0.8, 0.1, 0.1, alpha=0.22)); c.setFont('SB', 20)
    c.translate(x + cw / 2, y + ch / 2 + 6 * mm); c.rotate(20); c.drawCentredString(0, 0, 'SPÉCIMEN'); c.restoreState()

    c.setFont('S', 7.5); c.setFillColor(GRIS)
    c.drawCentredString(x0 + cw / 2, y0 - 6 * mm, "RECTO"); c.drawCentredString(x0 + 1.5 * cw, y0 - 6 * mm, "VERSO")

    # rappel de la mission sous la carte
    c.setFillColor(colors.black); c.setFont('SB', 12)
    c.drawString(25 * mm, y0 - 30 * mm, "Pochette de Mme Marie LE GOFF")
    c.setFont('S', 10)
    for i, t in enumerate([
        "Cette pochette contient trois documents :",
        "   • son avis d'impôt 2026 (2 pages) ;",
        "   • sa carte d'identité (ci-dessus, recto et verso) ;",
        "   • une facture d'eau récente (justificatif de domicile).",
        "",
        "Tous ces documents sont faux. Mme Le Goff n'existe pas.",
        "Ne les mélangez jamais avec vos vrais papiers.",
    ]):
        c.drawString(25 * mm, y0 - 38 * mm - i * 6 * mm, t)
    pied(c, 'Mme LE GOFF est un personnage inventé.')
    c.showPage()


def facture(c):
    c.setFillColor(BLEU); c.rect(18 * mm, H - 38 * mm, 14 * mm, 14 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    p = c.beginPath(); p.moveTo(25 * mm, H - 26 * mm); p.curveTo(21 * mm, H - 31 * mm, 21 * mm, H - 35 * mm, 25 * mm, H - 35.5 * mm)
    p.curveTo(29 * mm, H - 35 * mm, 29 * mm, H - 31 * mm, 25 * mm, H - 26 * mm); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(BLEU); c.setFont('SB', 16); c.drawString(36 * mm, H - 30 * mm, "Eaux de la Presqu'île")
    c.setFont('S', 8.5); c.setFillColor(GRIS); c.drawString(36 * mm, H - 35 * mm, "Distributeur d'eau fictif – exercice pédagogique")
    c.setFillColor(colors.black); c.setFont('SB', 13); c.drawRightString(W - 18 * mm, H - 28 * mm, "FACTURE D'EAU")
    c.setFont('S', 9.5); c.drawRightString(W - 18 * mm, H - 34 * mm, "n° SPEC-2026-110458")

    c.setFont('SB', 11); c.drawString(115 * mm, H - 58 * mm, f"Madame {PRENOM} {NOM}")
    c.setFont('S', 10.5); c.drawString(115 * mm, H - 63.5 * mm, ADR1); c.drawString(115 * mm, H - 69 * mm, ADR2)

    c.setFillColor(CLAIR); c.rect(18 * mm, H - 100 * mm, W - 36 * mm, 20 * mm, stroke=0, fill=1)
    infos = [("Date de la facture", "02/11/2026"), ("Période", "01/05/2026 – 31/10/2026"),
             ("Référence client", "SPEC 29999 0071"), ("Adresse desservie", ADR1)]
    for i, (k, v) in enumerate(infos):
        col, lig = i % 2, i // 2
        x0 = 22 * mm + col * 88 * mm; y0 = H - 87 * mm - lig * 9 * mm
        c.setFont('S', 8); c.setFillColor(GRIS); c.drawString(x0, y0, k)
        c.setFont('SB', 9); c.setFillColor(colors.black); c.drawString(x0 + 30 * mm, y0, v if len(v) < 32 else v[:31] + '…')

    y = H - 112 * mm
    c.setFont('SB', 12); c.setFillColor(BLEU); c.drawString(18 * mm, y, "Votre consommation")
    y = tableau(c, 18 * mm, y - 4 * mm, [
        ["Relevé du compteur", "Index"],
        ["Ancien index (relevé le 30/04/2026)", "1 204 m³"],
        ["Nouvel index (relevé le 31/10/2026)", "1 231 m³"],
        ["Consommation de la période", "27 m³"],
    ], [120 * mm, 54 * mm], couleur=BLEU)

    y -= 12 * mm
    c.setFont('SB', 12); c.setFillColor(BLEU); c.drawString(18 * mm, y, "Détail de la facture")
    y = tableau(c, 18 * mm, y - 4 * mm, [
        ["Ligne", "Montant TTC"],
        ["Abonnement (6 mois)", "28,40 €"],
        ["Eau potable : 27 m³", "52,65 €"],
        ["Assainissement : 27 m³", "48,06 €"],
        ["Redevances (organismes publics)", "11,34 €"],
    ], [120 * mm, 54 * mm], couleur=BLEU)

    c.setStrokeColor(BLEU); c.setLineWidth(1.5); c.rect(108 * mm, y - 22 * mm, W - 126 * mm, 16 * mm, stroke=1, fill=0)
    c.setFillColor(colors.black); c.setFont('S', 10); c.drawString(112 * mm, y - 15.5 * mm, "Total à payer")
    c.setFont('SB', 14); c.drawRightString(W - 22 * mm, y - 15.5 * mm, "140,45 €")
    c.setFont('S', 9); c.setFillColor(GRIS)
    c.drawString(18 * mm, y - 32 * mm, "Prélèvement automatique le 20/11/2026. Aucune démarche de votre part.")
    c.drawString(18 * mm, y - 37 * mm, "Cette facture peut servir de justificatif de domicile pendant 3 mois.")
    filigrane(c); pied(c, 'Mme LE GOFF est un personnage inventé.')
    c.showPage()


def construire(chemin):
    c = canvas.Canvas(chemin, pagesize=A4)
    c.setTitle("Pochette Mme Le Goff – documents fictifs SPÉCIMEN")
    c.setAuthor("Exercice pédagogique 1ère SAPAT")
    avis(c); carte(c); facture(c)
    c.save()


if __name__ == '__main__':
    construire(str(pathlib.Path(__file__).resolve().parent.parent / 'pochette_LeGoff_SPECIMEN.pdf'))
    print('ok')

# Un justificatif qui passe – simulateurs de dépôt de pièces justificatives

Ce dossier contient les ressources numériques d'une séance de démarches en ligne pour la 1ère Bac Pro SAPAT (lycée agricole, informatique / TIM). Il a été créé le 22 novembre 2026 pour la séance du mardi 24 novembre 2026.

**Page à projeter en classe :** https://dorvaljulien.github.io/depot-justificatifs/

| Ressource | Adresse | Rôle |
| --- | --- | --- |
| Page professeur | `index.html` | QR code à projeter, liens vers tout le reste |
| Simulateur téléphone | `telephone.html` | Site fictif « Armor Retraite » : 3 pièces à déposer depuis le téléphone |
| Simulateur ordinateur | `ordinateur.html` | Site fictif « Fonds Habitat Seniors » : 1 pièce à déposer depuis le PC, nom de fichier imposé |
| Pochette | `pochette_LeGoff_SPECIMEN.pdf` | Faux documents à imprimer, une pochette par binôme (4 pages A4) |
| QR code | `qr-telephone.svg`, `qr-telephone.png` | Vers `telephone.html` |

Deux documents de travail, privés, accompagnent ce dossier (ils sont dans le projet Claude « Cours informatique SAPAT ») : la doc de passation de la séance, qui contient le déroulé détaillé et les décisions, et la fiche élève.

## La séance en bref

Les élèves jouent une aidante à domicile qui aide Mme Marie Le Goff, 78 ans (personnage fictif), à constituer deux dossiers en ligne.

1. **À domicile, sur téléphone.** Demande d'aide ménagère à sa caisse de retraite. Les élèves numérisent trois papiers avec le téléphone et les déposent sur `telephone.html`, ouvert par QR code.
2. **À la structure, sur ordinateur.** Le second organisme n'accepte les dépôts que depuis un ordinateur. Les élèves font passer l'avis d'imposition du téléphone au PC (OneDrive ou une autre méthode, qu'elles décrivent par écrit), le renomment, puis le déposent sur `ordinateur.html`.

Principe pédagogique : on laisse l'erreur arriver. Les critères d'un justificatif accepté ne sont pas donnés au départ. C'est le site qui refuse, et la classe formule les critères à partir des refus.

## Ce que vérifient les simulateurs

Les deux pages lisent le fichier choisi **dans le navigateur**. Rien n'est envoyé sur internet ni enregistré : seul le chargement de la page consomme des données.

| Règle | Téléphone (Armor Retraite) | Ordinateur (Fonds Habitat Seniors) |
| --- | --- | --- |
| Pièces | Avis d'imposition, pièce d'identité, justificatif de domicile | Avis d'imposition |
| Format | PDF uniquement, reconnu à son contenu (une photo renommée en .pdf est refusée) | Idem |
| Poids maximal | 2 Mo par fichier | 2 Mo |
| Pages | Avis : au moins 2 ; identité : 1 ou 2 ; domicile : au moins 1 | Au moins 2 |
| Nom du fichier | Libre | Exactement `LEGOFF_avis-imposition.pdf` |
| Sur le mauvais appareil | Fonctionne aussi sur PC | Sur téléphone, affiche « Cette démarche n'est disponible que sur ordinateur » |

Messages de refus, volontairement secs comme sur un vrai site, chacun avec un lien vers les règles :

- « Format non accepté. » (JPG, HEIC, PNG, Word…)
- « Fichier trop volumineux (x Mo). Taille maximale : 2 Mo. »
- « Document incomplet : toutes les pages sont demandées. »
- « Document non conforme : 2 pages maximum. » (pièce d'identité)
- Sur ordinateur, « Nom de fichier non conforme » est précisé selon le cas : espaces, accents, minuscules, extension en double (`.pdf.pdf`, piège fréquent quand Windows masque les extensions).

Quand tout est conforme, un écran de réussite s'affiche (« Demande transmise » ou « Pièce transmise »), avec la date et l'heure. Pour chaque fichier, un lien « Voir le document » ouvre le PDF de l'élève : le professeur vérifie ainsi la lisibilité directement sur son appareil.

**Limite assumée :** le simulateur contrôle la forme (format, poids, pages, nom), pas le contenu. Une photo floue mise en PDF, ou une carte d'identité sans verso sur une seule page, passent. C'est le professeur qui vérifie en ouvrant le document.

Si le nombre de pages d'un PDF ne peut pas être lu, le fichier est accepté et l'écran de réussite indique « pages non vérifiées ».

## La pochette de faux documents

Le PDF compte 4 pages, à imprimer en couleur si possible, une pochette par binôme :

1. avis d'impôt 2026, page 1 ;
2. avis d'impôt 2026, page 2 ;
3. carte d'identité à découper, plier et coller (recto et verso côte à côte), plus le rappel de la mission ;
4. facture d'eau (justificatif de domicile).

Tout est fictif : Mme Le Goff, la commune de Kerlann (code postal 29999), les organismes. Chaque page porte le filigrane SPÉCIMEN / DOCUMENT FICTIF. Les documents ne reprennent ni la mise en page, ni les logos, ni les noms des vrais documents officiels.

## Modifier les simulateurs

Ne pas modifier `telephone.html` ni `ordinateur.html` à la main : ils sont produits par assemblage.

```
depot-justificatifs/
├── index.html                    page professeur (écrite à la main)
├── telephone.html                PRODUIT par outils/build.py
├── ordinateur.html               PRODUIT par outils/build.py
├── pochette_LeGoff_SPECIMEN.pdf  PRODUIT par outils/pochette.py
├── qr-telephone.svg / .png       PRODUITS par outils/qr.py
├── src/
│   ├── core.js                   lecture du fichier, détection du format, comptage des pages
│   ├── telephone.src.html        page téléphone (règles, textes, charte), marqueur /*CORE*/
│   └── ordinateur.src.html       page ordinateur, marqueur /*CORE*/
└── outils/
    ├── build.py                  insère core.js dans les deux pages
    ├── pochette.py               génère la pochette (reportlab)
    ├── qr.py                     génère les QR codes
    └── test_sims.py              tests automatiques (Playwright)
```

Où changer quoi :

- **Une règle du site téléphone** (poids, pages) : `MAX` et le tableau `PIECES` dans `src/telephone.src.html`.
- **Une règle du site ordinateur** : `MAX`, `ATTENDU` (nom imposé) et `verifierNom()` dans `src/ordinateur.src.html`. Pensez à mettre à jour le texte des « Conditions de dépôt » dans la même page.
- **Le personnage ou les documents** : constantes en tête de `outils/pochette.py`. Si le nom change, changez aussi `ATTENDU`, les en-têtes « Mme Marie LE GOFF » des deux pages et le README.

Après chaque modification, depuis le dossier `depot-justificatifs` :

```
python3 outils/build.py
python3 outils/test_sims.py
```

Les tests fabriquent leurs propres fichiers d'essai à partir de la pochette : PDF de 1 à 3 pages, PDF compressé, JPG, faux HEIC, PDF trop lourd, noms piégés. Ils vérifient chaque message attendu (21 cas). Dépendances : Python 3, `playwright`, `reportlab`, `qrcode`, ainsi que `qpdf`, `img2pdf`, ImageMagick et poppler-utils.

## Mise en ligne

Le dossier est servi par GitHub Pages depuis la branche `master` du dépôt `dorvaljulien.github.io` : un push suffit, la mise à jour prend une à deux minutes. Les pages à la racine du dépôt (`index.html`, `confidentialite.html`, `conditions.html`) servent à autre chose, l'application de synchro rclone : ne pas y toucher.

Les pages portent `noindex` pour ne pas apparaître dans les moteurs de recherche.

## Points restant à vérifier

- **PDF de vrais téléphones.** Le comptage des pages a été testé sur des PDF générés (y compris compressés), mais pas encore sur des scans d'iPhone (appli Fichiers) ni d'Android (Google Drive, appareil photo en mode document). Si un scan réel affiche « pages non vérifiées », c'est à corriger dans `compterPages()` de `src/core.js`.
- **Ctrl+P dans Edge** sur les postes élèves (« Enregistrer au format PDF »), utilisé dans la partie « pour aller plus loin ».
- **Connexion OneDrive** sur les téléphones des élèves (double authentification).

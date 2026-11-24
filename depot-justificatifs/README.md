# Un justificatif qui passe – simulateurs de dépôt de pièces justificatives

Ce dossier contient les ressources numériques d'une séance de démarches en ligne pour la 1ère Bac Pro SAPAT (lycée agricole, informatique / TIM). Il a été créé le 22 novembre 2026 pour la séance du mardi 24 novembre 2026.

**Page à projeter en classe :** https://dorvaljulien.github.io/depot-justificatifs/

| Ressource | Adresse | Rôle |
| --- | --- | --- |
| Page professeur | `index.html` | QR code et adresses à projeter ; les liens professeur sont cachés derrière la petite flèche grise en bas à droite |
| Simulateur téléphone | `telephone.html` | Site fictif « Armor Retraite » : 3 pièces à déposer depuis le téléphone |
| Simulateur ordinateur | `ordinateur.html` | Site fictif « Fonds Habitat Seniors » : 1 pièce à déposer depuis le PC, nom de fichier imposé |
| Simulateur signature | `signature.html` | Espace salariées fictif « Kerlann Services à Domicile » : télécharger l'engagement, le signer dans Edge, le renvoyer |
| Engagement | `engagement_confidentialite_SPECIMEN.pdf` | Le PDF à signer de la partie 3 (aussi inclus dans `signature.html`) |
| Pochette | `pochette_LeGoff_SPECIMEN.pdf` | Faux documents à imprimer, une pochette par binôme (4 pages A4) |
| QR code | `qr-telephone.svg`, `qr-telephone.png` | Vers `telephone.html` |

Deux documents de travail, privés, accompagnent ce dossier (ils sont dans le projet Claude « Cours informatique SAPAT ») : la doc de passation de la séance, qui contient le déroulé détaillé et les décisions, et la fiche élève.

## La séance en bref

Les élèves jouent une aidante à domicile qui aide Mme Marie Le Goff, 78 ans (personnage fictif), à constituer deux dossiers en ligne.

1. **À domicile, sur téléphone.** Demande d'aide ménagère à sa caisse de retraite. Les élèves numérisent trois papiers avec le téléphone et les déposent sur `telephone.html`, ouvert par QR code. Quand la demande est transmise, l'écran leur demande d'appeler le professeur pour lui montrer.
2. **À la structure, sur ordinateur.** Le second organisme n'accepte les dépôts que depuis un ordinateur. Les élèves font passer l'avis d'imposition du téléphone au PC (OneDrive ou une autre méthode, qu'elles décrivent par écrit), le renomment, puis le déposent sur `ordinateur.html`.
3. **Signer et renvoyer, sur ordinateur.** Sur `signature.html`, l'employeur fictif (Kerlann Services à Domicile) envoie un engagement de confidentialité. Les élèves le téléchargent, l'ouvrent dans Edge, ajoutent nom, lieu et date (« Ajouter du texte ») et leur signature (« Dessiner »), enregistrent, puis renvoient le fichier sur le site.

Le ménage des copies (fin de séance) se fait sans simulateur.

## Les codes d'accès

La partie 1 est libre. Les parties 2 et 3 demandent un code à 3 chiffres que seul le professeur connaît : il le donne à un binôme (ou le tape lui-même sur le poste) quand il a validé sa partie précédente. Personne ne prend donc d'avance sans être passé par le professeur.

**Les codes ne sont écrits nulle part dans ce dépôt**, qui est public (et GitHub Pages publie aussi ce README). Ils sont dans le Drive privé du professeur : fichier « Codes d'accès – parties 2 et 3 » du dossier de la séance. Les pages ne contiennent qu'une empreinte du code : un « Afficher le code source » ne le montre pas.

Le code est retenu tant que l'onglet reste ouvert : un rechargement ne le redemande pas.

Pour changer un code : calculer la nouvelle empreinte avec la fonction `empreinte()` de `src/pieges.js` (dans la console du navigateur, par exemple), remplacer la constante `CODE` en tête du script de `src/ordinateur.src.html` ou `src/signature.src.html`, reconstruire, et mettre à jour le fichier du Drive.

## Les pièges « de terrain »

Les deux sites reproduisent ce qui fait trébucher sur les vrais sites. Ils ne disent rien d'avance : c'est à l'élève de s'en sortir.

| Piège | Téléphone (Armor Retraite) | Ordinateur (Fonds Habitat Seniors) | Réflexe visé |
| --- | --- | --- | --- |
| Bandeau cookies qui masque la page | « Tout accepter » en gros, « Continuer sans accepter » en petit gris ; après « Tout accepter », un avertissement explique le problème | Idem | Lire avant de cliquer |
| Dépôt enfoui dans l'espace personnel | Arrivée sur l'accueil. Chemin : ☰ › Mes démarches › Suivre mes demandes › Compléter mon dossier. « Faire une nouvelle demande » est une impasse (« déjà une demande en cours »). Un message non lu donne l'indice. | Arrivée sur l'accueil. Chemin : Mes demandes › Reprendre. « Mes documents » est une impasse. | Naviguer dans un espace personnel, lire ses messages |
| Fausse publicité « PdfMagik » | Au-dessus des pièces | Sous les étapes, à gauche | Ne jamais confier des papiers à un site tiers |
| Vocabulaire administratif | « Pièce d'identité en cours de validité », « Justificatif de domicile de moins de 3 mois », « Justificatif de ressources N-1 », dans un ordre différent de la pochette, avec une aide « ? » | « Justificatif de ressources N-1 », aide « ? » | Décoder le jargon |
| « Fichier ajouté » n'est pas « envoyé » | « Continuer » mène à un récapitulatif : case de certification à cocher, puis « Confirmer l'envoi » | « Continuer » mène à l'étape 5 : case de certification, puis « Transmettre ma demande » | Aller jusqu'à la confirmation |
| Erreur loin du champ | – | Le champ affiche seulement « Fichier refusé ». La raison est dans un encadré rouge en haut du formulaire (visible sans faire défiler). | Chercher le message d'erreur |
| Mauvais emplacement | – | Un second emplacement « Autre document (facultatif) » accepte n'importe quel PDF ; si l'avis y est déposé, « Continuer » répond « Pièce obligatoire manquante » | Déposer au bon endroit |

Le fichier tombé dans la fausse publicité n'est jamais lu : le clic sur « Déposer mes fichiers » affiche un écran « Stop ! » qui explique le danger.

**Pour le débriefing :** en bas de l'écran final, une ligne grise indique le choix fait sur les cookies (refusés, tout accepté, x sur 3 acceptés) et ce qui s'est passé avec la publicité (non cliquée, ouverte puis fermée, fichiers presque envoyés). Rien n'est enregistré ailleurs : recharger la page efface tout.

## Ce que vérifient les simulateurs

Les deux pages lisent le fichier choisi **dans le navigateur**. Rien n'est envoyé sur internet ni enregistré : seul le chargement de la page consomme des données.

| Règle | Téléphone (Armor Retraite) | Ordinateur (Fonds Habitat Seniors) |
| --- | --- | --- |
| Pièces | Pièce d'identité, justificatif de domicile, avis d'imposition (« justificatif de ressources N-1 ») | Avis d'imposition (« justificatif de ressources N-1 ») + un emplacement facultatif |
| Format | PDF uniquement, reconnu à son contenu (une photo renommée en .pdf est refusée) | Idem |
| Poids maximal | 2 Mo par fichier | 2 Mo |
| Pages | Avis : au moins 2 ; identité : 1 ou 2 ; domicile : au moins 1 | Au moins 2 |
| Nom du fichier | Libre | Exactement `LEGOFF_avis-imposition.pdf` (les conditions précisent : nom de famille de la personne concernée par la demande) |
| Sur le mauvais appareil | Fonctionne aussi sur PC | Sur téléphone, affiche « Cette démarche n'est disponible que sur ordinateur » |

Messages de refus, volontairement secs comme sur un vrai site, chacun avec un lien vers les règles :

- « Format non accepté. » (JPG, HEIC, PNG, Word…)
- « Fichier trop volumineux (x Mo). Taille maximale : 2 Mo. »
- « Document incomplet : toutes les pages sont demandées. »
- « Document non conforme : 2 pages maximum. » (pièce d'identité)
- Sur ordinateur, « Nom de fichier non conforme » est précisé selon le cas : espaces, accents, minuscules, extension en double (`.pdf.pdf`, piège fréquent quand Windows masque les extensions).

Quand tout est conforme et la case de certification cochée, l'écran « Demande transmise » s'affiche, avec la date et l'heure. Sur téléphone, il demande d'appeler le professeur. Pour chaque fichier, un lien « Voir le document » ouvre le PDF de l'élève : le professeur vérifie ainsi la lisibilité directement sur son appareil.

## Ce que vérifie le site de signature (partie 3)

Le PDF d'origine est inclus dans la page : le bouton « Télécharger » le fournit, et la page reconnaît un fichier renvoyé tel quel. Edge enregistre ce qu'on ajoute à un PDF sous forme d'annotations : un tracé « Dessiner » (`/Ink`) et des zones « Ajouter du texte » (`/FreeText`). Le site les cherche.

| Cas | Réponse du site |
| --- | --- |
| Pas un PDF | « Format non accepté. » |
| Plus de 2 Mo | « Fichier trop volumineux… » |
| Fichier identique à l'original (oubli d'enregistrer, ou fichier retéléchargé) | « Document non complété et non signé : aucune modification trouvée. » |
| Plus d'une page (autre document) | « Document non conforme : ce n'est pas l'engagement de confidentialité. » |
| Du texte ajouté mais pas de tracé | « Document non signé. » |
| Un tracé, avec ou sans texte | Accepté |
| Modifié mais sans annotation (imprimé en PDF, scanné) | Accepté, signalé au professeur |

Pas de bandeau cookies ni de publicité sur cette page : c'est l'espace interne de l'employeur. Comme les deux autres sites, elle s'ouvre seulement sur ordinateur.

L'écran « Document reçu » demande d'appeler le professeur. La ligne grise du bas dit ce que le site a trouvé : « Signature dessinée : oui · Texte ajouté : 3 zones », ou « Aucune annotation trouvée… : vérifier à l'œil ». Le lien « Voir le document » permet de vérifier la signature, le nom, le lieu et la date.

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
├── signature.html                PRODUIT par outils/build.py (inclut le PDF d'engagement)
├── engagement_confidentialite_SPECIMEN.pdf   PDF à signer (partie 3)
├── pochette_LeGoff_SPECIMEN.pdf  PRODUIT par outils/pochette.py
├── qr-telephone.svg / .png       PRODUITS par outils/qr.py
├── src/
│   ├── core.js                   lecture du fichier, détection du format, comptage des pages
│   ├── pieges.js / pieges.css    pièges communs : cookies, fausse pub, aides « ? », rubriques, code d'accès (parties 2 et 3)
│   ├── telephone.src.html        page téléphone (règles, textes, charte), marqueur /*CORE*/
│   ├── ordinateur.src.html       page ordinateur, marqueur /*CORE*/
│   └── signature.src.html        page signature, marqueurs /*CORE*/ et /*ENGAGEMENT_B64*/
└── outils/
    ├── build.py                  insère core.js, pieges.js et pieges.css dans les trois pages
    ├── pochette.py               génère la pochette (reportlab)
    ├── qr.py                     génère les QR codes
    ├── test_sims.py              tests des parties 1 et 2 (Playwright, Python)
    └── test_signature.js         tests de la partie 3 et des codes (Playwright, Node)
```

Où changer quoi :

- **Une règle du site téléphone** (poids, pages) : `MAX` et le tableau `PIECES` dans `src/telephone.src.html`.
- **Les pièges communs** (texte du bandeau cookies, fausse publicité) : `src/pieges.js`.
- **Une règle du site ordinateur** : `MAX`, `ATTENDU` (nom imposé) et `verifierNom()` dans `src/ordinateur.src.html`. Pensez à mettre à jour le texte des « Conditions de dépôt » dans la même page.
- **Le personnage ou les documents** : constantes en tête de `outils/pochette.py`. Si le nom change, changez aussi `ATTENDU`, les en-têtes « Mme Marie LE GOFF » des deux pages et le README.

Après chaque modification, depuis le dossier `depot-justificatifs` :

```
python3 outils/build.py
python3 outils/test_sims.py
node outils/test_signature.js
```

Les tests fabriquent leurs propres fichiers d'essai à partir de la pochette : PDF de 1 à 3 pages, PDF compressé, JPG, faux HEIC, PDF trop lourd, noms piégés. Ils parcourent aussi les deux sites comme une élève (cookies, menus, fausse publicité, récapitulatif, case de certification, mauvais emplacement) : 40 vérifications. Dépendances : Python 3, `playwright`, `reportlab`, `qrcode`, ainsi que `qpdf`, `img2pdf`, ImageMagick et poppler-utils.

## Mise en ligne

Le dossier est servi par GitHub Pages depuis la branche `master` du dépôt `dorvaljulien.github.io` : un push suffit, la mise à jour prend une à deux minutes. Les pages à la racine du dépôt (`index.html`, `confidentialite.html`, `conditions.html`) servent à autre chose, l'application de synchro rclone : ne pas y toucher.

Les pages portent `noindex` pour ne pas apparaître dans les moteurs de recherche.

## Points restant à vérifier

- **Enregistrement dans Edge (partie 3).** Les tests utilisent des PDF annotés fabriqués, pas un vrai fichier enregistré par Edge. Avant la séance, sur un poste élève : signer le PDF dans Edge (« Dessiner » et « Ajouter du texte »), enregistrer, le déposer sur `signature.html` et regarder la ligne grise de l'écran final. Si elle dit « Aucune annotation trouvée » alors que le document est signé, récupérer le fichier pour corriger `annotations()` dans `src/core.js`.
- **PDF de vrais téléphones.** Le comptage des pages a été testé sur des PDF générés (y compris compressés), mais pas encore sur des scans d'iPhone (appli Fichiers) ni d'Android (Google Drive, appareil photo en mode document). Si un scan réel affiche « pages non vérifiées », c'est à corriger dans `compterPages()` de `src/core.js`.
- **Ctrl+P dans Edge** sur les postes élèves (« Enregistrer au format PDF »), utilisé dans la partie « pour aller plus loin ».
- **Connexion OneDrive** sur les téléphones des élèves (double authentification).

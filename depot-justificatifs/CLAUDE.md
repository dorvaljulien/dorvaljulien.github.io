# CLAUDE.md – depot-justificatifs

Notes pour une session de Claude qui reprend ce dossier. Le README décrit la séance et les règles ; ce fichier dit comment travailler ici sans rien casser.

## Contexte

- Enseignant : Julien, maths et informatique (TIM) en lycée agricole. Classe : 1ère Bac Pro SAPAT, deux groupes, le mardi, même durée de cours. Élèves très majoritairement des filles : la fiche élève et les consignes sont au féminin (« l'aidante »).
- Séance « Déposer, transférer, signer » (ex-« Un justificatif qui passe »), dans la séquence démarches en ligne : numériser des papiers avec un téléphone et les déposer sur un site exigeant (partie 1), passer un fichier du téléphone au PC (partie 2), signer un PDF dans Edge et le renvoyer (partie 3), puis faire le ménage dans les copies.
- Les documents de travail (doc de passation, fiche élève) sont dans le projet claude.ai « Cours informatique SAPAT » et dans le Drive de Julien (dossier « _Informatique - 1ère SAPAT › 5 - Documents dématérialisés », fiche élève à jour : « … fiche élève et cours v3.odt », qui mentionne les codes des parties 2 et 3 et les outils d’Edge). Ils sont privés.

## Règles à ne pas casser

1. **Rien ne quitte l'appareil.** Pas de `fetch`, pas de formulaire envoyé, pas de bibliothèque chargée depuis un CDN, pas de statistiques. Les élèves déposent des scans de faux papiers d'identité : la page doit pouvoir dire honnêtement que rien n'est envoyé. Les données mobiles des élèves sont limitées : chaque page doit rester légère (aujourd'hui 29 Ko, environ 10 Ko une fois compressée par GitHub Pages).
2. **Tout est fictif et le reste.** Organismes inventés (Armor Retraite, Fonds Habitat Seniors, Service des impôts de Kerlann, Eaux de la Presqu'île), commune fictive (Kerlann, 29999), personnage fictif (Mme Marie Le Goff). Aucun nom, logo ni mise en page d'un vrai organisme ou d'un vrai document officiel. Chaque page porte une mention « Site fictif – exercice pédagogique », et la pochette garde son filigrane SPÉCIMEN.
3. **Fichiers produits.** `telephone.html`, `ordinateur.html` et `signature.html` sont produits par `outils/build.py` à partir de `src/` (`core.js` et `pieges.js` à la place de `/*CORE*/`, `pieges.css` à la place de `/*PIEGES_CSS*/`). On modifie `src/`, puis on lance le build. Même chose pour la pochette (`outils/pochette.py`) et les QR codes (`outils/qr.py`).
4. **Pages autonomes.** Chaque page produite tient en un seul fichier HTML (CSS et JS en ligne), pour pouvoir être copiée telle quelle sur un poste sans réseau.
5. **Racine du dépôt.** `index.html`, `confidentialite.html` et `conditions.html` à la racine de `dorvaljulien.github.io` servent à la validation Google de l'outil rclone de Julien. Ne jamais les modifier.

## Choix de conception (déjà discutés avec Julien)

- On laisse l'erreur arriver : le site ne donne pas ses règles d'emblée, mais il les rend accessibles par un lien (« Formats acceptés », « Conditions de dépôt »). Lire les conditions fait partie de la compétence. Messages de refus courts et secs, comme sur un vrai site.
- Le format est détecté au contenu (`%PDF-`, en-têtes JPG, PNG, HEIC), pas à l'extension.
- JPG refusé, et pas seulement HEIC : un iPhone convertit souvent ses photos en JPG au moment de l'envoi, donc accepter le JPG laisserait passer une simple photo.
- Pièce d'identité : 1 ou 2 pages acceptées (recto et verso sur une seule page, comme une photocopie).
- 2 Mo sur les deux sites. Le 1 Mo prévu au départ pour le site ordinateur a été abandonné : l'élève n'aurait aucun moyen propre de réduire un fichier sur le PC, et les convertisseurs en ligne sont justement proscrits. Ce qui distingue les deux sites, c'est le nom de fichier imposé.
- Pas de miniatures sur l'écran de réussite : trop lourd sur téléphone. Un lien « Voir le document » (blob URL) ouvre le PDF à la place.
- Pas de code de récépissé et aucune collecte : l'élève montre l'écran de réussite au professeur. Sur téléphone, cet écran dit « Appelez le professeur ».
- Pièges « de terrain » (novembre 2026, choisis par Julien) : bandeau cookies, dépôt enfoui dans l'espace personnel, fausse publicité de convertisseur, jargon administratif avec aide « ? », récapitulatif et case de certification avant l'envoi, sur ordinateur erreur affichée en haut du formulaire (pas trop cachée, à la demande de Julien) et emplacement « Autre document » facultatif. Écartés : connexion préalable, session expirée, compte à rebours.
- Navigation par ancres (`#accueil`, `#depot`…) : le bouton Retour du navigateur fonctionne. `telephone.html#depot` mène directement au dépôt (pratique pour le professeur, à ne pas donner aux élèves).
- Codes d'accès (24/11/2026) : partie 1 libre ; parties 2 et 3 bloquées par un code que seul Julien connaît (codes dans son Drive, fichier « Codes d'accès – parties 2 et 3 » ; jamais dans le dépôt, qui est public) et donne à chaque binôme après avoir validé sa partie précédente. Les codes ne doivent apparaître nulle part pour les élèves : ni sur la page projetée, ni en clair dans le code des pages (on n'y met qu'une empreinte, voir `empreinte()` dans `src/pieges.js`). Une première version affichait les codes sur la page projetée : c'était un malentendu.
- Partie 3 (24/11/2026) : page à part (`signature.html`), PDF sans champs à remplir (on utilise « Ajouter du texte » d'Edge), aucun piège en plus (ni cookies ni publicité). Le site refuse un fichier identique à l'original, un autre document, du texte sans tracé ; il accepte un tracé, et laisse passer avec un avertissement au professeur un PDF modifié sans annotation (imprimé en PDF, scanné).
- Les conditions du site ordinateur précisent « nom de famille de la personne concernée par la demande » : une élève qui met son propre nom est refusée.

## Comptage des pages (`src/core.js`)

1. Lecture des octets en latin1, puis recherche du plus grand `/Count` près d'un `/Type /Pages` ; à défaut, comptage des objets `/Type /Page`.
2. Si rien n'est trouvé, décompression des flux `/ObjStm` avec `DecompressionStream('deflate')`, natif dans les navigateurs (Safari 16.4 et plus récent), puis même recherche.
3. Si le comptage échoue toujours, la fonction renvoie `null` : le fichier est accepté avec la mention « pages non vérifiées ».

Point non vérifié : les PDF de scanners réels (iPhone Fichiers, Google Drive, Samsung). Si Julien signale « pages non vérifiées » sur un vrai scan, demander le fichier et l'ajouter aux tests.

## Travailler ici

Depuis le dossier `depot-justificatifs` :

```
python3 outils/build.py        # après toute modification de src/
python3 outils/test_sims.py    # parties 1 et 2, doit finir sur « 0 échec(s) » ; CHROME=... pour le navigateur
node outils/test_signature.js  # partie 3 et codes (23 vérifications) ; NODE_PATH=$(npm root -g) si playwright est global
python3 outils/pochette.py     # si la pochette change
python3 outils/qr.py           # si l'adresse du site change
```

Après un changement visible, faire une capture avec Playwright et la regarder (390×844 pour le téléphone, 1280×800 pour le PC) avant de livrer.

La mise en ligne se fait par un push sur `master` : GitHub Pages publie en une à deux minutes. Tout push publie, donc ne pousser qu'avec l'accord de Julien.

## Préférences de Julien

- Il discute d'abord le plan, ensuite seulement on produit. Il aime les documents de passation qui permettent de reprendre dans une nouvelle conversation.
- Explications en français courant, sans jargon technique inutile.

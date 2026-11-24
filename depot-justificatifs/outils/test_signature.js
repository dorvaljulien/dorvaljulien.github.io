/* Tests automatiques de la partie 3 (signature.html) et des codes d'accès (parties 2 et 3 ; la partie 1 est libre).

Usage (depuis le dossier depot-justificatifs) :
    python3 outils/build.py
    node outils/test_signature.js          # CHROME=/chemin/vers/chrome pour changer de navigateur

Dépendances : Node avec le module playwright ; pdftocairo (poppler-utils) pour le cas « imprimé en PDF »
(cas sauté s'il manque).

Les PDF « signés » sont fabriqués comme le fait un lecteur PDF (Edge, Chrome, Firefox) à l'enregistrement :
le fichier d'origine, suivi d'une mise à jour qui ajoute des annotations à la page
(/Ink = signature dessinée, /FreeText = zone de texte).
*/
const fs = require('fs'), os = require('os'), path = require('path'), zlib = require('zlib');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const RACINE = path.resolve(__dirname, '..');
const ORIGINAL = fs.readFileSync(path.join(RACINE, 'engagement_confidentialite_SPECIMEN.pdf'));
const url = nom => 'file://' + path.join(RACINE, nom);

// Les codes ne sont écrits nulle part dans le dépôt (public) : on les retrouve à partir de l'empreinte
// inscrite dans chaque page, en essayant les 1000 valeurs possibles.
const empreinte = s => { let x = 0x811c9dc5; for (const c of 'kerlann-' + s) x = Math.imul(x ^ c.charCodeAt(0), 0x01000193) >>> 0; return x.toString(16); };
const codeDe = nom => {
  const h = fs.readFileSync(path.join(RACINE, nom), 'utf8').match(/const CODE = '([0-9a-f]+)'/)[1];
  for (let i = 0; i < 1000; i++) { const c = String(i).padStart(3, '0'); if (empreinte(c) === h) return c; }
  throw new Error('code introuvable pour ' + nom);
};
const CODE2 = codeDe('ordinateur.html'), CODE3 = codeDe('signature.html');
const autre = c => String((+c + 1) % 1000).padStart(3, '0');

// ---------- Fabrication des PDF d'essai ----------
const INK = '<< /Type /Annot /Subtype /Ink /Rect [60 300 300 380] /InkList [[70 320 120 360 180 330 250 370]] /C [0 0 0.6] /BS << /W 2 >> >>';
const texte = (x, y, s) => `<< /Type /Annot /Subtype /FreeText /Rect [${x} ${y} ${x + 200} ${y + 16}] /Contents (${s}) /DA (/Helv 11 Tf 0 g) >>`;

function miseAJour(annots, { objstm = false } = {}) {
  const src = ORIGINAL.toString('latin1');
  const page = src.match(/(\d+) 0 obj\s*<<((?:(?!endobj)[\s\S])*?\/Type\s*\/Page(?![A-Za-z])(?:(?!endobj)[\s\S])*?)>>\s*endobj/);
  const trailer = src.match(/trailer\s*<<([\s\S]*?)>>\s*startxref\s*(\d+)/);
  const taille = +trailer[1].match(/\/Size\s+(\d+)/)[1];
  const racine = trailer[1].match(/\/Root\s+(\d+ \d+ R)/)[1];
  const prev = +trailer[2];
  const nums = annots.map((_, i) => taille + i);
  const dictPage = page[2].replace(/\/Annots\s*\[[^\]]*\]/, '') + ` /Annots [${nums.map(n => n + ' 0 R').join(' ')}] `;
  let corps = '\n', xref = [];
  const pos = () => ORIGINAL.length + Buffer.byteLength(corps, 'latin1');
  xref.push([+page[1], pos()]);
  corps += `${page[1]} 0 obj\n<<${dictPage}>>\nendobj\n`;
  if (objstm) {
    // Annotations rangées dans un flux d'objets compressé (comme certains logiciels)
    let entete = '', donnees = '';
    annots.forEach((a, i) => { entete += `${nums[i]} ${donnees.length} `; donnees += a + '\n'; });
    const flux = zlib.deflateSync(Buffer.from(entete + donnees, 'latin1'));
    const n = taille + annots.length;
    xref.push([n, pos()]);
    corps += `${n} 0 obj\n<< /Type /ObjStm /N ${annots.length} /First ${entete.length} /Filter /FlateDecode /Length ${flux.length} >>\nstream\n`;
    corps += flux.toString('latin1') + '\nendstream\nendobj\n';
  } else {
    annots.forEach((a, i) => { xref.push([nums[i], pos()]); corps += `${nums[i]} 0 obj\n${a}\nendobj\n`; });
  }
  const debutXref = pos();
  corps += 'xref\n' + xref.map(([n, o]) => `${n} 1\n${String(o).padStart(10, '0')} 00000 n \n`).join('');
  corps += `trailer\n<< /Size ${taille + annots.length + (objstm ? 1 : 0)} /Root ${racine} /Prev ${prev} >>\nstartxref\n${debutXref}\n%%EOF\n`;
  return Buffer.concat([ORIGINAL, Buffer.from(corps, 'latin1')]);
}

function fabriquer(t) {
  const ecrire = (nom, b) => fs.writeFileSync(path.join(t, nom), b);
  const complet = [INK, texte(150, 655, 'Camille Martin'), texte(100, 450, 'Kerlann'), texte(280, 450, '24/11/2026')];
  ecrire('engagement_confidentialite_SPECIMEN.pdf', ORIGINAL);
  ecrire('signe_complet.pdf', miseAJour(complet));
  ecrire('signe_objstm.pdf', miseAJour(complet, { objstm: true }));
  ecrire('signature_seule.pdf', miseAJour([INK]));
  ecrire('texte_seul.pdf', miseAJour(complet.slice(1)));
  ecrire('photo.jpg', Buffer.concat([Buffer.from([0xFF, 0xD8, 0xFF, 0xE0]), Buffer.alloc(5000)]));
  fs.copyFileSync(path.join(RACINE, 'pochette_LeGoff_SPECIMEN.pdf'), path.join(t, 'avis_4pages.pdf'));
  try {
    execFileSync('pdftocairo', ['-pdf', path.join(t, 'engagement_confidentialite_SPECIMEN.pdf'), path.join(t, 'imprime.pdf')]);
    return true;
  } catch (e) { return false; }
}

// ---------- Tests ----------
let echecs = 0;
const note = (ok, txt) => { console.log((ok ? 'OK   ' : 'ÉCHEC') + ' ' + txt); if (!ok) echecs++; };

async function code(page, valeur) {
  await page.fill('#pgCode', valeur);
  await page.click('.pg-code button');
}

(async () => {
  const t = fs.mkdtempSync(path.join(os.tmpdir(), 'sig-'));
  const avecImprime = fabriquer(t);
  const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const mobileUA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile';

  // Partie 1 : pas de code, le bandeau cookies arrive directement
  const ctel = await b.newContext({ viewport: { width: 390, height: 844 }, userAgent: mobileUA });
  const pt = await ctel.newPage();
  await pt.goto(url('telephone.html'));
  note(!(await pt.isVisible('.pg-code')) && await pt.isVisible('.pg-cookies'), 'telephone.html : pas de code, bandeau cookies directement');
  await ctel.close();

  // Codes en clair absents des pages (Ctrl+U ne doit pas les montrer)
  const hors64 = f => fs.readFileSync(path.join(RACINE, f), 'utf8').replace(/atob\('[^']*'\)/, '');
  note(![CODE2, CODE3].some(c => (hors64('ordinateur.html') + hors64('signature.html') + hors64('index.html')).includes(c)),
       'codes des parties 2 et 3 absents du code des pages');

  // Code d'accès : ordinateur (partie 2)
  for (const [nom, bon, ctxOpt] of [['ordinateur.html', CODE2, { viewport: { width: 1280, height: 800 } }]]) {
    const ctx = await b.newContext(ctxOpt);
    const p = await ctx.newPage();
    await p.goto(url(nom));
    note(await p.isVisible('.pg-code') && !(await p.isVisible('.pg-cookies')), `${nom} : code demandé avant tout, pas de bandeau cookies`);
    await code(p, autre(bon));
    note(await p.isVisible('.pg-codeko'), `${nom} : mauvais code refusé`);
    await code(p, bon);
    note(!(await p.isVisible('.pg-code')) && await p.isVisible('.pg-cookies'), `${nom} : bon code -> bandeau cookies`);
    await p.reload();
    note(!(await p.isVisible('.pg-code')) && await p.isVisible('.pg-cookies'), `${nom} : après rechargement, code non redemandé`);
    await ctx.close();
  }

  // Signature sur téléphone : message « ordinateur seulement », pas de code
  const m = await b.newContext({ viewport: { width: 390, height: 844 }, userAgent: mobileUA });
  const pm = await m.newPage();
  await pm.goto(url('signature.html'));
  note(await pm.isVisible('.mobile') && !(await pm.isVisible('.pg-code')), 'signature sur téléphone : « disponible que sur ordinateur »');
  await m.close();

  // Signature sur ordinateur
  const ctx = await b.newContext({ viewport: { width: 1280, height: 800 }, acceptDownloads: true });
  const p = await ctx.newPage();
  await p.goto(url('signature.html'));
  await code(p, CODE2);
  note(await p.isVisible('.pg-codeko'), 'signature : le code de la partie 2 ne marche pas');
  await code(p, CODE3);
  note(!(await p.isVisible('.pg-code')) && !(await p.isVisible('.pg-cookies')), 'signature : bon code accepté, pas de bandeau cookies');

  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#telecharger')]);
  const recu = fs.readFileSync(await dl.path());
  note(dl.suggestedFilename() === 'engagement_confidentialite_SPECIMEN.pdf' && recu.equals(ORIGINAL),
       `signature : téléchargement de ${dl.suggestedFilename()} identique à l'original`);

  await p.click('#envoyer');
  note(await p.isVisible('#erreur'), 'signature : « Envoyer » sans fichier refusé');

  const lire = async () => {
    await p.waitForFunction(() => { const e = document.querySelector('#msg'); return e.textContent && !e.textContent.startsWith('Vérification'); });
    return (await p.textContent('#msg')).trim();
  };
  const CAS = [
    ['photo.jpg', '✖ Format non accepté'],
    ['engagement_confidentialite_SPECIMEN.pdf', '✖ Document non complété et non signé'],
    ['avis_4pages.pdf', '✖ Document non conforme'],
    ['texte_seul.pdf', '✖ Document non signé'],
    ['signature_seule.pdf', '✔ Fichier ajouté'],
    ['signe_objstm.pdf', '✔ Fichier ajouté'],
  ];
  if (avecImprime) CAS.push(['imprime.pdf', '✔ Fichier ajouté']);
  else console.log('—     pdftocairo absent : cas « imprimé en PDF » sauté');
  for (const [f, attendu] of CAS) {
    await p.setInputFiles('#fichier', path.join(t, f));
    const txt = await lire();
    note(txt.startsWith(attendu), `signature ${f} -> ${txt.split('\n')[0].replace(/ Consultez.*/, '')}`);
  }
  // Après un fichier refusé, l'envoi est bloqué
  await p.setInputFiles('#fichier', path.join(t, 'texte_seul.pdf'));
  await lire();
  await p.click('#envoyer');
  note(await p.isVisible('#erreur') && !(await p.isVisible('#succes')), 'signature : envoi bloqué après un refus');

  await p.setInputFiles('#fichier', path.join(t, 'signe_complet.pdf'));
  await lire();
  await p.click('#envoyer');
  note(await p.isVisible('#succes') && await p.isVisible('.appel'), 'signature : écran « Document reçu » avec « Appelez le professeur »');
  const bil = await p.textContent('#bilan');
  note(bil === 'Signature dessinée : oui · Texte ajouté : 3 zones', `signature : bilan « ${bil} »`);
  note((await p.textContent('#recap')).includes('Voir le document'), 'signature : lien « Voir le document »');

  // Cas « imprimé en PDF » jusqu'au bout : accepté, mais signalé au professeur
  if (avecImprime) {
    await p.click('#recommencer');
    await p.waitForSelector('#formulaire', { state: 'visible' });
    await p.setInputFiles('#fichier', path.join(t, 'imprime.pdf'));
    await lire();
    await p.click('#envoyer');
    const bil2 = await p.textContent('#bilan');
    note(bil2.startsWith('Aucune annotation trouvée'), `signature imprimée : bilan « ${bil2} »`);
  }

  await b.close();
  fs.rmSync(t, { recursive: true, force: true });
  console.log(`\n${echecs} échec(s)`);
  process.exit(echecs ? 1 : 0);
})();

/* Pièges « de terrain » communs aux deux simulateurs : cookies, fausse publicité, aides « ? », navigation.
   Rien n'est envoyé : tout reste dans la page. Le bilan (choix cookies, clic sur la pub) s'affiche
   sur l'écran final pour que le professeur en parle avec l'élève. */
const Pieges = (() => {
  const bilan = { cookies: 'aucun choix', pub: 'non cliquée' };
  const el = h => { const d = document.createElement('div'); d.innerHTML = h.trim(); return d.firstChild; };

  function cookies(site) {
    const m = el(`<div class="pg-fond"><div class="pg-boite pg-cookies" role="dialog">
      <button class="pg-sans" data-r="refusés">Continuer sans accepter →</button>
      <h2>Votre vie privée nous importe</h2>
      <p>${site} et ses <u>148 partenaires</u> utilisent des cookies et traceurs pour mesurer l'audience,
      personnaliser les contenus et vous proposer des publicités adaptées à vos centres d'intérêt.</p>
      <div class="pg-choix" hidden>
        <label><input type="checkbox" checked> Mesure d'audience</label>
        <label><input type="checkbox" checked> Publicité personnalisée</label>
        <label><input type="checkbox" checked> Partage avec les réseaux sociaux</label>
        <button class="pg-second" data-r="perso">Enregistrer mes choix</button>
      </div>
      <button class="pg-tout" data-r="tout accepté">Tout accepter</button>
      <button class="pg-second pg-perso">Personnaliser</button>
    </div></div>`);
    m.onclick = e => {
      const b = e.target.closest('button');
      if (!b) return;
      if (b.classList.contains('pg-perso')) { m.querySelector('.pg-choix').hidden = false; b.hidden = true; return; }
      let r = b.dataset.r;
      if (r === 'perso') { const n = m.querySelectorAll('input:checked').length; r = n ? `${n} sur 3 acceptés` : 'refusés'; }
      bilan.cookies = r; m.remove();
      if (r === 'tout accepté') avertirCookies(site);
    };
    document.body.appendChild(m);
  }

  // Petit avertissement pédagogique après « Tout accepter »
  function avertirCookies(site) {
    const a = el(`<div class="pg-avert" role="status"><button class="pg-sans" aria-label="Fermer">✕</button>
      <strong>⚠ Vous avez tout accepté.</strong> ${site} et ses 148 partenaires peuvent maintenant suivre ce que
      vous faites sur internet, pour vous afficher de la publicité ciblée. Sur l'appareil de quelqu'un d'autre,
      vous l'avez fait en son nom. Le bon réflexe : « Continuer sans accepter », ou « Personnaliser » et tout décocher.
      <span class="pg-petit">(Exercice : rien n'est enregistré.)</span></div>`);
    a.querySelector('button').onclick = () => a.remove();
    document.body.appendChild(a);
  }

  function pub(cible, site) {
    const p = el(`<div class="pg-pub" role="button"><span class="pg-mention">Annonce</span>
      <strong>Fichier refusé ?</strong> Convertissez et compressez vos documents en PDF conforme en 1 clic.
      <span class="pg-pubbtn">Convertir gratuitement</span><span class="pg-marque">PdfMagik</span></div>`);
    p.onclick = () => {
      bilan.pub = 'ouverte puis fermée';
      const f = el(`<div class="pg-fond"><div class="pg-boite pg-faux">
        <div class="pg-fauxhaut">PdfMagik <small>convertisseur gratuit</small></div>
        <h2>Tous vos fichiers en PDF</h2>
        <p>JPG, HEIC, PNG, Word → PDF. Rapide, gratuit, sans inscription.</p>
        <button class="pg-tout pg-dep">Déposer mes fichiers</button>
        <p class="pg-petit">En utilisant ce service, vous acceptez nos conditions générales, dont la conservation
        de vos fichiers et leur transmission à nos partenaires.</p>
        <button class="pg-sans pg-ret">‹ Retour</button></div></div>`);
      f.onclick = e => {
        if (e.target.closest('.pg-ret')) f.remove();
        if (e.target.closest('.pg-dep')) {
          bilan.pub = 'fichiers presque envoyés';
          f.firstChild.innerHTML = `<h2 class="pg-stop">Stop !</h2>
            <p>Vous alliez confier les papiers de Mme Le Goff (avis d'imposition, carte d'identité…) à une société inconnue.</p>
            <p>Ce site était une <strong>publicité</strong> : il n'a rien à voir avec ${site}. Les petites lignes
            disaient qu'il conserve vos fichiers et les transmet à des partenaires.</p>
            <p><strong>Une démarche se fait sur le site de l'organisme, et nulle part ailleurs.</strong></p>
            <p class="pg-petit">(Exercice : rien n'a été envoyé.)</p>
            <button class="pg-tout pg-ret">Revenir à ma démarche</button>`;
        }
      };
      document.body.appendChild(f);
    };
    cible.appendChild(p);
  }

  // Bouton « ? » : <button class="pg-q" data-rep="id">?</button> ouvre/ferme l'élément id
  document.addEventListener('click', e => {
    const q = e.target.closest('.pg-q');
    if (!q) return;
    e.preventDefault();
    const r = document.getElementById(q.dataset.rep);
    r.hidden = !r.hidden;
  });

  // Navigation par rubriques : <section class="vue" id="vue-xxx">, lien href="#xxx"
  function rubriques(defaut, apres) {
    const montrer = () => {
      const h = location.hash.slice(1);
      const v = document.getElementById('vue-' + h) ? h : defaut;
      document.querySelectorAll('.vue').forEach(s => { s.hidden = s.id !== 'vue-' + v; });
      window.scrollTo(0, 0);
      if (apres) apres(v);
    };
    addEventListener('hashchange', montrer);
    montrer();
  }

  // Code à 3 chiffres que seul le professeur connaît : il le donne au binôme quand il a validé
  // la partie précédente. La page ne contient qu'une empreinte du code (pas le code en clair).
  // Le code est retenu pour l'onglet (sessionStorage) : un rechargement ne le redemande pas.
  const empreinte = s => { let x = 0x811c9dc5; for (const c of 'kerlann-' + s) x = Math.imul(x ^ c.charCodeAt(0), 0x01000193) >>> 0; return x.toString(16); };
  function code(attendu, partie, ensuite) {
    const cle = 'code-' + attendu;
    try { if (sessionStorage.getItem(cle) === '1') { ensuite(); return; } } catch (e) {}
    const m = el(`<div class="pg-fond pg-verrou"><form class="pg-boite pg-code">
      <div class="pg-petit">Exercice – ${partie}</div>
      <h2>Code d'accès</h2>
      <p>Faites valider la partie précédente par le professeur : il vous donnera le code à 3 chiffres.</p>
      <input id="pgCode" inputmode="numeric" pattern="[0-9]*" maxlength="3" autocomplete="off" aria-label="Code à 3 chiffres">
      <div class="pg-codeko" hidden>Code incorrect.</div>
      <button class="pg-tout" type="submit">Valider</button>
    </form></div>`);
    const champ = m.querySelector('input'), ko = m.querySelector('.pg-codeko');
    m.querySelector('form').onsubmit = e => {
      e.preventDefault();
      if (empreinte(champ.value.trim()) !== attendu) { ko.hidden = false; champ.select(); return; }
      try { sessionStorage.setItem(cle, '1'); } catch (e2) {}
      m.remove();
      ensuite();
    };
    champ.oninput = () => { ko.hidden = true; };
    document.body.appendChild(m);
    champ.focus();
  }

  const recommencer = () => location.replace(location.pathname + location.search);
  const resume = () => `Cookies : ${bilan.cookies} · Publicité : ${bilan.pub}`;
  return { cookies, pub, rubriques, recommencer, resume, code };
})();

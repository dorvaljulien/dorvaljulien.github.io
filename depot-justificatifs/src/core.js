/* Noyau commun des simulateurs de dépôt — tout se passe dans le navigateur, rien n'est envoyé. */
const Depot = (() => {
  function latin1(bytes) {
    let s = '';
    const CH = 0x8000;
    for (let i = 0; i < bytes.length; i += CH) {
      s += String.fromCharCode.apply(null, bytes.subarray(i, i + CH));
    }
    return s;
  }

  // Format réel d'après le contenu (pas d'après l'extension)
  function detecterFormat(b) {
    const head = latin1(b.subarray(0, 1024));
    if (head.indexOf('%PDF-') !== -1) return 'pdf';
    if (b[0] === 0xFF && b[1] === 0xD8) return 'jpg';
    if (b[0] === 0x89 && b[1] === 0x50 && b[2] === 0x4E && b[3] === 0x47) return 'png';
    const ftyp = latin1(b.subarray(4, 12));
    if (/^ftyp(heic|heix|hevc|mif1|msf1|heim|heis)/.test(ftyp)) return 'heic';
    if (/^ftyp/.test(ftyp)) return 'video';
    if (b[0] === 0x50 && b[1] === 0x4B) return 'office';
    if (latin1(b.subarray(0, 4)) === 'RIFF') return 'webp';
    return 'inconnu';
  }

  async function inflate(bytes) {
    if (typeof DecompressionStream === 'undefined') return null;
    try {
      const ds = new DecompressionStream('deflate');
      const out = await new Response(new Blob([bytes]).stream().pipeThrough(ds)).arrayBuffer();
      return latin1(new Uint8Array(out));
    } catch (e) { return null; }
  }

  function compterDans(txt) {
    // 1) /Count de l'arbre des pages (le plus grand = la racine)
    let max = 0;
    const re = /\/Type\s*\/Pages(?![A-Za-z])/g;
    let m;
    while ((m = re.exec(txt))) {
      const fen = txt.slice(Math.max(0, m.index - 400), m.index + 400);
      const c = fen.match(/\/Count\s+(\d+)/g);
      if (c) c.forEach(x => { const n = parseInt(x.replace(/\D/g, ''), 10); if (n > max && n < 10000) max = n; });
    }
    if (max > 0) return max;
    // 2) sinon, on compte les objets /Type /Page
    const p = txt.match(/\/Type\s*\/Page(?![A-Za-z])/g);
    return p ? p.length : 0;
  }

  // Nombre de pages d'un PDF, ou null si indéterminable
  async function compterPages(b) {
    const txt = latin1(b);
    let n = compterDans(txt);
    if (n > 0) return n;
    n = compterDans(await objStm(b, txt));
    return n > 0 ? n : null;
  }

  // Contenu décompressé des flux d'objets (/ObjStm) : certains logiciels y rangent tout
  async function objStm(b, txt) {
    const re = /\/Type\s*\/ObjStm/g;
    let m, total = '';
    while ((m = re.exec(txt))) {
      const s = txt.indexOf('stream', m.index);
      if (s < 0) continue;
      let start = s + 6;
      if (txt[start] === '\r') start++;
      if (txt[start] === '\n') start++;
      const e = txt.indexOf('endstream', start);
      if (e < 0) continue;
      const dec = await inflate(b.subarray(start, e));
      if (dec) total += dec + '\n';
    }
    return total;
  }

  // Annotations ajoutées par un lecteur PDF (Edge, Chrome, Firefox) :
  // /Ink = tracé à main levée (la signature), /FreeText = zone de texte ajoutée.
  async function annotations(b) {
    const raw = latin1(b);
    const txt = raw + '\n' + await objStm(b, raw);
    const nb = re => (txt.match(re) || []).length;
    return { ink: nb(/\/Subtype\s*\/Ink(?![A-Za-z])/g), texte: nb(/\/Subtype\s*\/FreeText(?![A-Za-z])/g) };
  }

  async function analyser(file) {
    const b = new Uint8Array(await file.arrayBuffer());
    const format = detecterFormat(b);
    const info = { nom: file.name, taille: file.size, format, pages: null, chiffre: false };
    if (format === 'pdf') {
      const head = latin1(b.subarray(0, Math.min(b.length, 200000)));
      info.chiffre = /\/Encrypt\s/.test(latin1(b));
      info.pages = await compterPages(b);
      if (!/%%EOF/.test(latin1(b.subarray(Math.max(0, b.length - 2048))))) info.tronque = true;
    }
    return info;
  }

  function mo(octets) {
    const v = octets / (1024 * 1024);
    if (v < 0.1) return Math.max(1, Math.round(octets / 1024)) + ' Ko';
    return v.toFixed(1).replace('.', ',') + ' Mo';
  }

  function maintenant() {
    const d = new Date();
    const p = n => String(n).padStart(2, '0');
    return `${p(d.getDate())}/${p(d.getMonth() + 1)}/${d.getFullYear()} à ${p(d.getHours())}h${p(d.getMinutes())}`;
  }

  return { analyser, annotations, mo, maintenant };
})();

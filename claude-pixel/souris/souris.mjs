#!/usr/bin/env node
/*
 * souris : la commande qui parle au serveur de la souris.
 *
 *   node souris.mjs demarre [--id nom] [--tel] [--humain] [--port 4917]
 *   node souris.mjs va 12 8          (une commande)
 *   node souris.mjs - < gestes.txt   (une commande par ligne, arrêt au premier refus)
 *   node souris.mjs fin              (ferme la séance et range la vidéo)
 */
import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ICI = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const iPort = argv.indexOf('--port');
const PORT = Number(iPort >= 0 ? argv[iPort + 1] : process.env.SOURIS_PORT || 4917);

function requete(methode, corps) {
  return new Promise((ok, ko) => {
    const r = http.request({ host: '127.0.0.1', port: PORT, path: methode === 'GET' ? '/sante' : '/', method: methode, headers: { 'content-type': 'text/plain; charset=utf-8' } }, res => {
      let t = ''; res.setEncoding('utf8'); res.on('data', c => { t += c; }); res.on('end', () => { try { ok(JSON.parse(t)); } catch (e) { ko(new Error(t)); } });
    });
    r.on('error', ko); r.setTimeout(120000, () => r.destroy(new Error('délai dépassé')));
    if (corps) r.write(corps); r.end();
  });
}

async function demarre() {
  try { const s = await requete('GET'); console.log('déjà lancée · séance ' + s.id); return; } catch (e) { /* pas encore lancée */ }
  const log = path.join(os.tmpdir(), 'claude-pixel-souris-' + PORT + '.log');
  const fd = fs.openSync(log, 'w');
  const p = spawn(process.execPath, [path.join(ICI, 'serveur.mjs'), ...argv.slice(1)], { detached: true, stdio: ['ignore', fd, fd] });
  p.unref();
  for (let i = 0; i < 120; i++) {
    await new Promise(r => setTimeout(r, 250));
    try { const s = await requete('GET'); console.log('souris prête · séance ' + s.id + ' · ' + s.vue.width + '×' + s.vue.height + ' · ' + path.relative(process.cwd(), s.dossier)); return; } catch (e) { /* on attend */ }
  }
  console.error('Le serveur ne répond pas. Journal : ' + log + '\n' + fs.readFileSync(log, 'utf8').slice(-2000));
  process.exit(1);
}

async function envoie(texte) {
  let r;
  try { r = await requete('POST', texte); } catch (e) { console.error('Pas de serveur sur le port ' + PORT + ' : lance « souris demarre ». (' + e.message + ')'); process.exit(2); }
  console.log(r.msg);
  if (!r.ok) process.exit(1);
}

if (!argv.length || argv[0] === 'aide') {
  console.log(fs.readFileSync(path.join(ICI, 'serveur.mjs'), 'utf8').match(/\/\*[\s\S]*?\*\//)[0]);
  console.log('Commandes : va, pas, choisis, defile, appuie, relache, clic, double, trace, glisse, molette, tiens, lache, touche, tape, survole, regarde, etat, cibles, attends, fichier, fin. Détails : souris/README.md');
} else if (argv[0] === 'demarre') await demarre();
else if (argv[0] === '-') await envoie(fs.readFileSync(0, 'utf8'));
else await envoie(argv.filter((a, i) => !(a === '--port' || argv[i - 1] === '--port')).join(' '));

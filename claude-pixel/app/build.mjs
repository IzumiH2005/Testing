// Claude Pixel — assemble app/index.html (un seul fichier, publiable en artefact).
// Usage : node app/build.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ici = dirname(fileURLToPath(import.meta.url));
const src = f => readFileSync(join(ici, 'src', f), 'utf8');
const ORDRE = ['core.js', 'detect.js', 'methode.js', 'exporte.js', 'ui-base.js', 'ui-scene.js', 'ui-outils.js', 'ui-panneaux.js', 'ui-plus.js'];

// La méthode complète, embarquée telle quelle (onglet Aide, règles, portes).
const methode = readFileSync(join(ici, '..', 'METHODE_PIXEL_ART.md'), 'utf8');
const sur = s => s.replace(/<\/(script)/gi, '<\\/$1').replace(/<!--/g, '<\\!--');
const docJs = '(function(G){const AP=G.AP=G.AP||{};AP.DOC_METHODE=' + sur(JSON.stringify(methode)) + ';})(window);\n';

const js = docJs + ORDRE.map(f => '/* ===== ' + f + ' ===== */\n' + src(f)).join('\n');
if (/<\/script/i.test(js.replace(/<\\\/script/gi, ''))) throw new Error('</script> non échappé dans le JS');
const css = src('style.css');
const tpl = src('template.html');
if (!tpl.includes('/*CSS*/') || !tpl.includes('/*JS*/')) throw new Error('Gabarit sans emplacements /*CSS*/ ou /*JS*/');
const html = tpl.replace('/*CSS*/', () => css).replace('/*JS*/', () => '\n' + sur(js) + '\n');
writeFileSync(join(ici, 'index.html'), html);
console.log('app/index.html : ' + (Buffer.byteLength(html) / 1024).toFixed(0) + ' Ko (' + ORDRE.length + ' modules, méthode ' + methode.split('\n').length + ' lignes)');

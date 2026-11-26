// Le générateur de rampe suit le sélecteur : après un nouveau code hex, l'aperçu et la rampe
// ajoutée partent de la nouvelle couleur (et non de celle du dernier rendu du panneau).
const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const { AP, RACINE } = require('./aide.cjs');

let pw = null; try { pw = require('playwright'); } catch (e) { /* navigateur absent */ }

test('générateur de rampe : aperçu et ajout depuis la couleur saisie', { skip: !pw && 'playwright absent' }, async () => {
  const nav = await pw.chromium.launch();
  try {
    const page = await nav.newPage({ viewport: { width: 1280, height: 900 } });
    await page.goto('file://' + path.join(RACINE, 'app', 'index.html'));
    await page.waitForFunction(() => window.claudePixel && document.querySelector('[data-cible]'));
    await page.locator('[data-cible="modale-oui"]').click();   // la modale « Nouveau dessin » : on crée le dessin par défaut
    await page.waitForSelector('.voile', { state: 'detached' });
    await page.locator('[data-cible="onglet-couleurs"]').first().click();
    const base = '#3a7bd5', attendu = AP.genereRampe(base, 5, 15);
    const hex = page.locator('[data-cible="hex"]').first();
    await hex.fill(base); await hex.press('Tab');
    const apercu = await page.locator('[data-cible="rampe-apercu"] button').evaluateAll(L => L.map(b => b.title));
    assert.deepEqual(apercu, attendu);
    const avant = await page.locator('[data-cible^="rampe-retire-"]').count();
    await page.locator('[data-cible="rampe-ajoute"]').first().click();
    await page.waitForSelector('[data-cible="rampe-' + avant + '-0"]');
    const ajoutee = await page.locator('[data-cible^="rampe-' + avant + '-"]').evaluateAll(L => L.map(b => b.title));
    assert.deepEqual(ajoutee, attendu);
  } finally { await nav.close(); }
});

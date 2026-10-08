// Parcours complet, comme un élève : chaque exemple s'exécute, chaque code de départ
// est refusé, chaque solution est acceptée, et la progression arrive au bout.
const { test, expect } = require('@playwright/test');

async function attendreResultat(bloc, bouton) {
  await bloc.locator(`[data-a="${bouton}"]`).click();
  await expect(bloc.locator(`[data-a="${bouton}"]`)).toBeEnabled();
  await expect(bloc.locator('.out')).not.toContainText(/Exécution…|Vérification…/);
}

test('parcours complet dans le navigateur', async ({ page }) => {
  const problemes = [];
  page.on('pageerror', e => problemes.push('erreur JS : ' + e.message));
  page.on('console', m => { if (m.type() === 'error') problemes.push('console : ' + m.text()); });
  page.on('request', r => { if (new URL(r.url()).hostname !== '127.0.0.1' && !r.url().startsWith('data:')) problemes.push('requête externe : ' + r.url()); });

  await page.goto('/python-lycee/');
  await expect(page.locator('#pyPill')).toHaveClass(/ready/);

  const modules = await page.locator('.step[data-mod]:not([data-mod="bac"])').evaluateAll(bs => bs.map(b => b.dataset.mod));
  expect(modules.length).toBe(8);

  for (const id of modules) {
    await page.locator(`.step[data-mod="${id}"]`).click();

    const notions = page.locator('.notion');
    for (let i = 0; i < await notions.count(); i++) {
      const n = notions.nth(i);
      await attendreResultat(n, 'run');
      await expect(n.locator('.out .msg.err'), `${id}, exemple ${i + 1}`).toHaveCount(0);
    }

    const exos = page.locator('article.exo');
    for (let i = 0; i < await exos.count(); i++) {
      const exo = exos.nth(i);
      const titre = `${id}, ${await exo.locator('h3').textContent()}`;

      await attendreResultat(exo, 'check');
      await expect(exo.locator('.out .msg'), titre + ' : départ').toHaveCount(1);
      await expect(exo.locator('.out .msg.ok'), titre + ' : départ refusé').toHaveCount(0);

      await exo.locator('[data-a="sol"]').click();
      await exo.locator('[data-copy]').click();
      await attendreResultat(exo, 'check');
      await expect(exo.locator('.out .msg.ok'), titre + ' : solution acceptée').toHaveCount(1);
    }
  }

  await expect(page.locator('#progTxt')).toContainText('17/17');
  await expect(page.locator('#fin')).toContainText('Parcours terminé');
  expect(problemes).toEqual([]);
});

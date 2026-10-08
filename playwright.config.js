// Test de bout en bout : le site servi tel quel, ouvert dans Chromium.
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: 'tests/e2e',
  timeout: 10 * 60 * 1000,
  expect: { timeout: 120 * 1000 },
  workers: 1,
  reporter: 'list',
  use: { baseURL: 'http://127.0.0.1:8765', browserName: 'chromium' },
  webServer: { command: 'python3 -m http.server 8765 --bind 127.0.0.1', url: 'http://127.0.0.1:8765/', reuseExistingServer: false, stderr: 'ignore' },
});

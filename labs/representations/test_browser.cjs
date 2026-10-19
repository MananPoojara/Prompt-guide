const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const { pathToFileURL } = require("node:url");
const path = require("node:path");
(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({
      viewport: { width: 1280, height: 1000 },
    });
    const errors = [],
      external = [];
    page.on("pageerror", (e) => errors.push(String(e)));
    page.on("request", (r) => {
      if (/^https?:/.test(r.url())) external.push(r.url());
    });
    await page.goto(pathToFileURL(path.join(__dirname, "index.html")).href);
    assert.equal(await page.locator("#cosines tr").count(), 3);
    assert.equal(await page.locator("#vectors tr").count(), 12);
    const initial = await page.locator("#attention tbody").textContent();
    await page.selectOption("#head", { value: "11" });
    await page.selectOption("#layer", { value: "5" });
    assert.notEqual(
      await page.locator("#attention tbody").textContent(),
      initial,
    );
    await page.selectOption("#input", "1");
    assert.match(
      await page.locator("#status").textContent(),
      /Input 2, block 6, head 12/,
    );
    const before = await page.locator("#vectors").textContent();
    await page.selectOption("#stage", "final_hidden");
    assert.notEqual(await page.locator("#vectors").textContent(), before);
    await page.screenshot({
      path: "/tmp/prompt-guide-representations-desktop.png",
      fullPage: true,
    });
    await page.setViewportSize({ width: 375, height: 812 });
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    await page.screenshot({
      path: "/tmp/prompt-guide-representations-mobile.png",
      fullPage: true,
    });
    assert.deepEqual(errors, []);
    assert.deepEqual(external, []);
    console.log(
      "Controls, measurements, mobile width, and offline operation verified",
    );
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exit(1);
});

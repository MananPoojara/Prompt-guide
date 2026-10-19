// Requires Playwright and Chromium. Uses only local files and saved model data.
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
(async () => {
  const browser = await chromium.launch({headless:true});
  try {
    const page=await browser.newPage({viewport:{width:1280,height:1000}});
    const errors=[];const external=[];
    page.on('pageerror',e=>errors.push(String(e)));
    page.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url());});
    await page.goto(pathToFileURL(path.join(__dirname,'index.html')).href);
    await page.waitForFunction(()=>document.querySelector('#load-status').textContent.startsWith('Recorded data loaded'));
    assert.equal(await page.locator('#candidate-table tr').count(),50);
    assert.equal(await page.locator('.token').count(),2);
    await page.selectOption('#text-choice','5');
    assert.equal(await page.locator('.token').count(),3);
    for(const value of ['0.4','1.6']){
      await page.locator('#temperature').evaluate((el,v)=>{el.value=v;el.dispatchEvent(new Event('input',{bubbles:true}));},value);
      const probability=Number((await page.locator('.bar-value').first().textContent()).replace('%',''));
      if(value==='0.4')global.cold=probability;else assert(probability<global.cold);
    }
    await page.click('#draw');assert(!(await page.locator('#draw-result').textContent()).includes('No token'));
    await page.selectOption('#run-temperature','0');assert(await page.locator('#seed').isDisabled());
    const france=await page.locator('#output-continuation').textContent();
    await page.selectOption('#prefix-choice','1');
    assert.notEqual(await page.locator('#output-continuation').textContent(),france);
    await page.selectOption('#run-temperature','1');await page.selectOption('#seed','41');
    assert((await page.locator('#run-summary').textContent()).includes('seed 41'));
    await page.screenshot({path:'/tmp/prompt-guide-model-desktop.png',fullPage:true});
    await page.setViewportSize({width:375,height:812});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await page.screenshot({path:'/tmp/prompt-guide-model-mobile.png',fullPage:true});
    assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
    console.log('Browser controls, data states, no external requests, and mobile width verified.');
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1);});

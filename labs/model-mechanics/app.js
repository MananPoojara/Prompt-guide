'use strict';
(() => {
  const data = window.MODEL_MECHANICS_DATA;
  const byId = id => document.getElementById(id);
  if (!data) { byId('load-status').textContent = 'Recorded data could not load. Keep data.js beside this file, or read the JSON artifact.'; return; }
  const display = text => text.replace(/ /g, '␠').replace(/\n/g, '↵').replace(/\t/g, '⇥');
  const option = (select, label, value) => { const el = document.createElement('option'); el.value = value; el.textContent = label; select.append(el); };
  data.tokenizations.forEach((row,i) => option(byId('text-choice'), JSON.stringify(row.text), i));
  data.prefixes.forEach((row,i) => option(byId('prefix-choice'), row.prefix, i));
  let currentProbs = [];
  const prefix = () => data.prefixes[Number(byId('prefix-choice').value)];
  function tokenView() {
    const row = data.tokenizations[Number(byId('text-choice').value)];
    byId('input-text').textContent = row.text;
    byId('token-pieces').replaceChildren();
    row.ids.forEach((id,i) => {
      const chip = document.createElement('span'); chip.className = 'token'; chip.textContent = display(row.pieces[i]);
      const small = document.createElement('small'); small.textContent = `ID ${id}`; chip.append(small); byId('token-pieces').append(chip);
    });
    byId('token-summary').textContent = `${row.ids.length} tokens · ${Array.from(row.text).length} Unicode code points · complete ID sequence round-trips to the original text`;
    byId('raw-tokens').textContent = JSON.stringify({ids: row.ids, vocabulary_pieces: row.vocabulary_pieces, decoded: row.decoded},null,2);
  }
  function probabilityView() {
    const candidates = prefix().first_candidates;
    const temperature = Number(byId('temperature').value);
    byId('temperature-label').textContent = temperature.toFixed(1);
    const largest = Math.max(...candidates.map(x => x.logit));
    const weights = candidates.map(x => Math.exp((x.logit-largest)/temperature));
    const total = weights.reduce((a,b) => a+b,0);
    currentProbs = weights.map(w => w/total);
    byId('bars').replaceChildren(); byId('candidate-table').replaceChildren();
    candidates.forEach((candidate,i) => {
      if (i < 10) {
        const row = document.createElement('div'); row.className = 'bar-row';
        const label = document.createElement('span'); label.className='bar-label'; label.textContent=display(candidate.piece);
        const track = document.createElement('div'); track.className='bar-track'; track.setAttribute('aria-hidden','true');
        const fill=document.createElement('div'); fill.className='bar-fill'; fill.style.width=`${currentProbs[i]*100}%`; track.append(fill);
        const value=document.createElement('span'); value.className='bar-value'; value.textContent=`${(currentProbs[i]*100).toFixed(2)}%`;
        row.append(label,track,value); byId('bars').append(row);
      }
      const row=document.createElement('tr');
      [display(candidate.piece),candidate.id,candidate.logit.toFixed(4),`${(currentProbs[i]*100).toFixed(4)}%`].forEach(value => {const cell=document.createElement('td');cell.textContent=value;row.append(cell);});
      byId('candidate-table').append(row);
    });
    const remaining=currentProbs.slice(10).reduce((a,b) => a+b,0);
    byId('remaining').textContent=`Top 10 shown on a fixed 0–100% bar scale. The remaining 40 candidates share ${(remaining*100).toFixed(2)}%.`;
    byId('draw-result').textContent='No token drawn at this setting.';
  }
  function runView() {
    const row=prefix(); const temperature=Number(byId('run-temperature').value);
    const seed=temperature===0 ? null : Number(byId('seed').value);
    byId('seed').disabled=temperature===0;
    const run=row.runs.find(x => x.temperature===temperature && x.seed===seed);
    byId('output-prefix').textContent=row.prefix;
    byId('output-continuation').textContent=run.continuation;
    byId('run-summary').textContent=`${run.new_ids.length} new tokens · ${temperature===0 ? 'greedy decoding; no random draw' : `temperature ${temperature}, seed ${seed}, top 50 candidates per step`} · saved output`;
    byId('run-trace').textContent=JSON.stringify(run.trace,null,2);
  }
  byId('text-choice').addEventListener('change',tokenView);
  byId('prefix-choice').addEventListener('change',() => {probabilityView();runView();});
  byId('temperature').addEventListener('input',probabilityView);
  byId('run-temperature').addEventListener('change',runView);
  byId('seed').addEventListener('change',runView);
  byId('draw').addEventListener('click',() => {
    const point=Math.random();let cumulative=0;let selected=currentProbs.length-1;
    for (let i=0;i<currentProbs.length;i++) {cumulative+=currentProbs[i];if(point<cumulative){selected=i;break;}}
    byId('draw-result').textContent=`${display(prefix().first_candidates[selected].piece)} · ${(currentProbs[selected]*100).toFixed(2)}% at this setting`;
  });
  byId('provenance').textContent=`Recorded ${data.metadata.recorded_on} · ${data.metadata.model} · revision ${data.metadata.revision} · ${data.metadata.device}. All 20 default continuations are retained.`;
  byId('load-status').textContent='Recorded data loaded. No network connection or model account needed.';
  tokenView();probabilityView();runView();
})();

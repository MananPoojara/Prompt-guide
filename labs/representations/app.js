'use strict';
const data=window.REPRESENTATION_DATA;
const byId=id=>document.getElementById(id);
function cell(tag,text){const el=document.createElement(tag);el.textContent=text;return el;}
function options(id,values){for(const [value,text] of values){const el=cell('option',text);el.value=value;byId(id).append(el);}}
options('input',data.inputs.map((x,i)=>[i,x.text]));
options('layer',Array.from({length:data.metadata.layers},(_,i)=>[i,i+1]));
options('head',Array.from({length:data.metadata.heads},(_,i)=>[i,i+1]));
for(const x of data.inputs)byId('sentences').append(cell('p',x.text));
const labels={token_embedding:['Stored token embedding','Same vocabulary entry'],input_hidden:['Input representation','Token plus position, before transformer blocks'],final_hidden:['Final representation','After all blocks and final layer normalization']};
for(const [stage,value] of Object.entries(data.target_cosines)){const tr=document.createElement('tr');for(const t of [labels[stage][0],value.toFixed(6),labels[stage][1]])tr.append(cell('td',t));byId('cosines').append(tr);}
function attention(){const x=data.inputs[Number(byId('input').value)],layer=Number(byId('layer').value),head=Number(byId('head').value);const matrix=x.attention[layer][head];const table=byId('attention'),thead=table.querySelector('thead'),tbody=table.querySelector('tbody');thead.replaceChildren();tbody.replaceChildren();const header=document.createElement('tr');header.append(cell('th','Query ↓ / Key →'));x.pieces.forEach((p,i)=>header.append(cell('th',`${i}: ${JSON.stringify(p)}`)));thead.append(header);matrix.forEach((row,i)=>{const tr=document.createElement('tr');const heading=cell('th',`${i}: ${JSON.stringify(x.pieces[i])}`);heading.scope='row';tr.append(heading);row.forEach((v,j)=>{const td=cell('td',v.toFixed(3));td.style.backgroundColor=`rgba(36,116,85,${v*.65})`;td.title=`Query ${i}, key ${j}: ${v}`;tr.append(td);});tbody.append(tr);});byId('status').textContent=`Input ${Number(byId('input').value)+1}, block ${layer+1}, head ${head+1}. ${x.ids.length} tokens. All values are saved measurements.`;}
function vectors(){const stage=byId('stage').value,body=byId('vectors');body.replaceChildren();for(let i=0;i<12;i++){const tr=document.createElement('tr');tr.append(cell('th',i));for(const x of data.inputs)tr.append(cell('td',x.vectors[stage][x.target_position][i].toFixed(6)));body.append(tr);}}
byId('dimensions').textContent=`Each recorded vector has ${data.metadata.dimensions} coordinates. The two inputs use the same target token ID and position.`;
for(const id of ['input','layer','head'])byId(id).addEventListener('change',attention);byId('stage').addEventListener('change',vectors);attention();vectors();

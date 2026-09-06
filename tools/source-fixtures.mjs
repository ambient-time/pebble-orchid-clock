/** Capture normalized geometry from Luke Steuber's supplied canvas functions.
 * Regenerate with Node.js; ordinary builds use the checked-in fixture.
 * Copyright 2026 Luke Steuber. MIT License.
 */
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=fs.readFileSync(path.join(root,'reference/source.html'),'utf8');
const functions=['labellum','hourFreckles','column'].map(name=>{
  const fn=source.match(new RegExp('  function '+name+'\\([^]*?\\n  \\}'));
  if(!fn)throw new Error('Missing source function '+name);
  return fn[0];
}).join('\n');
let active=[],paths=[],ellipses=[];
const x={
  beginPath(){active=[];},moveTo(...v){active.push(['M',...v]);},
  bezierCurveTo(...v){active.push(['C',...v]);},quadraticCurveTo(...v){active.push(['Q',...v]);},
  closePath(){active.push(['Z']);},fill(){if(active.length)paths.push(structuredClone(active));},
  ellipse(...v){ellipses.push(v);},stroke(){},
  save(){},restore(){},translate(){},arc(){},
  createLinearGradient(){return {addColorStop(){}};}
};
const context=vm.createContext({x,Math,TAU:Math.PI*2,HOUR_SPOTS:12,MINUTE_SPOTS:60});
vm.runInContext(functions,context,{timeout:1000});
vm.runInContext('hourFreckles(0,0,1,12,{})',context,{timeout:1000});
const hours=ellipses.map(v=>v.slice(0,3));
ellipses=[];paths=[];
vm.runInContext('labellum(1,.38,0,0,{})',context,{timeout:1000});
const fixture={sourceSHA256:crypto.createHash('sha256').update(source).digest('hex'),
  hours,minutes:ellipses.map(v=>v.slice(0,2)),lip:paths[0],throat:paths[1]};
ellipses=[];
vm.runInContext('column(0,0,.22,{})',context,{timeout:1000});
fixture.column=ellipses[0].slice(0,4);
fs.writeFileSync(path.join(root,'test/source-fixtures.json'),JSON.stringify(fixture,null,2)+'\n');

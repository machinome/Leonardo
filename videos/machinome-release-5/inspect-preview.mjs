// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Inspect the live preview and its aligned cues; never render a movie.
import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {driverX,wheelAngle} from './ending-motion.mjs';
const base=dirname(fileURLToPath(import.meta.url));
const tool=resolve(process.argv[2]);
const origin=process.argv[3]??'http://127.0.0.1:8785';
const {chromium}=await import(pathToFileURL(resolve(tool,'node_modules/playwright/index.mjs')));
const doc=JSON.parse(await readFile(resolve(base,'_build/movie-resolved.json')));
const outline=await (await fetch(`${origin}/film.json`)).json();
const shots=outline.shots;
const browser=await chromium.launch({headless:true});
const output=resolve(base,'_build/inspection');await mkdir(output,{recursive:true});
const checks=[];
try{
  const page=await browser.newPage({viewport:{width:1440,height:1050}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`${origin}/#movie`);
  await page.waitForFunction(()=>window.player?.generation()>0);
  const seek=async time=>{
    await page.evaluate(async time=>{window.player.seek(time);await window.player.idle();},time);
    const fault=await page.locator('#fault').textContent();assert.equal(fault,'');
  };
  for(const id of ['document','behind-the-film','mirror','open-source','wheel-returns','invitation']){
    const shot=shots.find(s=>s.id===id);
    for(const fraction of id==='document'||id==='open-source'?[.05,.8]:[.5]){
      const time=shot.start+(shot.end-shot.start)*fraction;
      await seek(time);
      await page.locator('iframe').screenshot({path:resolve(output,`${id}-${fraction}.png`)});
      const overflow=await page.evaluate(()=>[...document.querySelector('iframe').contentDocument.querySelectorAll('.listing')]
        .map(el=>({file:el.querySelector('.listing-file').textContent,
          bottom:el.querySelector('pre').getBoundingClientRect().bottom,
          limit:el.getBoundingClientRect().bottom})));
      for(const item of overflow)assert.ok(item.bottom<=item.limit+1,`Code overflows: ${item.file}`);
      if(id==='document'){
        const picture=await page.evaluate(()=>{
          const win=document.querySelector('iframe').contentWindow;
          const img=win.document.querySelector('.vm-picture-img').getBoundingClientRect();
          const note=win.document.querySelector('.archive .vm-title');
          const box=note.getBoundingClientRect();
          return {image:{left:img.left,top:img.top,right:img.right,bottom:img.bottom},
            width:win.innerWidth,height:win.innerHeight,text:note.textContent,
            note:{left:box.left,top:box.top,right:box.right,bottom:box.bottom},background:win.getComputedStyle(note).backgroundColor};
        });
        assert.ok(picture.image.left<=0.5&&picture.image.top<=0.5&&picture.image.right>=picture.width-.5&&picture.image.bottom>=picture.height-.5,
          'The manuscript covers every edge of the video');
        assert.equal(picture.text,'Source: Codex Atlanticus · 1078r');
        assert.ok(picture.note.left>picture.width/2&&picture.note.top>picture.height*.85);
        assert.notEqual(picture.background,'rgba(0, 0, 0, 0)');
      }
      checks.push({id,time,overflow});
    }
  }
  const source=doc.chapters[0].shots.find(s=>s.id==='behind-the-film');
  assert.ok(source.end-source.start<18,'The enumeration must stay brief');
  const feed=doc.chapters[0].shots.find(s=>s.id==='feed-motion');
  const meta=JSON.parse(await readFile(resolve(base,'_build/narration-manifest.json')));
  const take=JSON.parse(await readFile(meta.cacheFile+'.json'));
  const aligned=take.alignment.characters.join('');
  const endOf=phrase=>{
    const index=aligned.indexOf(phrase);assert.ok(index>=0);
    return 3+take.alignment.character_end_times_seconds[Array.from(aligned.slice(0,index)+phrase).length-1];
  };
  const startOf=phrase=>{
    const index=aligned.indexOf(phrase);assert.ok(index>=0);
    return 3+take.alignment.character_start_times_seconds[Array.from(aligned.slice(0,index)).length];
  };
  const frameTolerance=.5/doc.output.fps+1e-6;
  const firstReturn=feed.cues.find(c=>c.actions.some(a=>a.action==='highlight')&&
    Math.abs(feed.start+c.until-endOf('while the first returns'))<=frameTolerance);
  assert.ok(firstReturn,'A measured highlight covers the first pawl returning');
  assert.deepEqual(firstReturn.actions.find(a=>a.action==='highlight').parts,
    [['Feed mechanism','Driving pawl']]);
  await seek(feed.start+(firstReturn.at+firstReturn.until)/2);
  await page.locator('iframe').screenshot({path:resolve(output,'returning-pawl.png')});
  checks.push({id:'returning-pawl',time:feed.start+firstReturn.at});
  const open=doc.chapters[0].shots.find(s=>s.id==='open-source');
  const returned=doc.chapters[0].shots.find(s=>s.id==='wheel-returns');
  const props=doc.chapters[0].elements.ecosystem.props;
  const driveStart=open.start+open.cues.find(c=>c.actions.some(a=>a.action==='drive')).at;
  const speechEnd=endOf('a stream of open source tools');
  assert.ok(returned.start<driveStart+6*props.stagger,'The handoff starts before the last tool is released');
  assert.ok(Math.abs(driveStart+props.streamDuration-speechEnd)<.001,'The stream ends with the spoken phrase');
  assert.ok(driverX(props.streamDuration-6*props.stagger,props)<-100,'The last label has crossed the whole frame');
  const overlapTime=returned.start+.8;
  await seek(overlapTime);
  const frame=await (await fetch(`${origin}/frame?t=${overlapTime}`)).json();
  const physical=(frame.elements['continuous.returned'].time*doc.model.expectedDurationSeconds-500)*90;
  assert.ok(Math.abs(physical-wheelAngle(frame.time-driveStart,props))<1e-6,'The physical and graphic wheels share a phase');
  const overlap=await page.evaluate(()=>{
    const w=document.querySelector('iframe').contentWindow;
    return [...w.document.querySelectorAll('.incoming')].filter(el=>Number(w.getComputedStyle(el).opacity)>.1&&
      el.getBoundingClientRect().right>0&&el.getBoundingClientRect().left<w.innerWidth).map(el=>el.textContent);
  });
  assert.ok(overlap.length>0,'Tool names remain visible while the real wheel appears');
  await page.locator('iframe').screenshot({path:resolve(output,'stream-wheel-overlap.png')});
  checks.push({id:'stream-wheel-overlap',time:overlapTime,visible:overlap});
  const zoom=returned.cues.find(c=>c.actions.some(a=>a.action==='move'));
  const zoomStart=returned.start+zoom.at,zoomEnd=returned.start+zoom.actions[0].until;
  assert.ok(Math.abs(zoomStart-startOf('and humans...'))<=frameTolerance);
  assert.ok(Math.abs(zoomEnd-endOf('their own'))<=frameTolerance);
  const invitation=doc.chapters[0].shots.find(s=>s.id==='invitation');
  assert.equal(invitation.start,zoomEnd,'Logo begins only after their own ends');
  let previousDistance=Infinity;
  for(const fraction of [0,.5,.8,.99]){
    const time=Math.floor((zoomStart+(zoomEnd-zoomStart)*fraction)*doc.output.fps+1e-9)/doc.output.fps;
    await seek(time);
    const frame=await (await fetch(`${origin}/frame?t=${time}`)).json();
    const camera=frame.elements['continuous.returned'].view;
    const distance=Math.hypot(...camera.camera.map((v,i)=>v-camera.target[i]));
    assert.ok(distance<previousDistance,'The camera moves continuously into the wheel centre');
    assert.deepEqual(camera.target,[0,-151,120]);
    previousDistance=distance;
    const opacity=await page.evaluate(()=>Number(getComputedStyle(document.querySelector('iframe').contentDocument.querySelector('.wheel-exit')).opacity));
    if(fraction===.99)assert.equal(opacity,1,'Wheel has disappeared before the logo');
    await page.locator('iframe').screenshot({path:resolve(output,`wheel-zoom-${fraction}.png`)});
    checks.push({id:'wheel-zoom',time,distance,opacity});
  }
  for(const offset of [0,.4,.9]){
    await seek(invitation.start+offset);
    const opacity=await page.evaluate(()=>Number(getComputedStyle(document.querySelector('iframe').contentDocument.querySelector('.signature')).opacity));
    if(offset===0)assert.equal(opacity,0);
    else if(offset===.4)assert.ok(opacity>.4&&opacity<.6);
    else assert.equal(opacity,1);
    await page.locator('iframe').screenshot({path:resolve(output,`logo-fade-${offset}.png`)});
    checks.push({id:'logo-fade',time:invitation.start+offset,opacity});
  }
  for(const id of ['behind-the-film','mirror']){
    const shot=doc.chapters[0].shots.find(s=>s.id===id);
    for(const cue of shot.cues){
      const action=cue.actions.find(a=>a.action==='blink');if(!action)continue;
      await seek(shot.start+(cue.at+cue.until)/2);
      const tokens=await page.evaluate(()=>[...document.querySelector('iframe').contentDocument.querySelectorAll('.blink-token')].map(x=>x.textContent));
      assert.deepEqual(tokens,[action.params.token]);
      checks.push({id,token:action.params.token,from:shot.start+cue.at,to:shot.start+cue.until});
    }
  }
  await seek(outline.output.duration-1);
  assert.equal(await page.evaluate(()=>document.querySelector('iframe').contentDocument.querySelector('.question')),null);
  assert.deepEqual(errors,[]);
  await writeFile(resolve(output,'checks.json'),JSON.stringify({status:'passed',duration:outline.output.duration,checks},null,2)+'\n');
  console.log(`Preview checked: ${checks.length} frames/cues; no video rendered.`);
}finally{await browser.close();}

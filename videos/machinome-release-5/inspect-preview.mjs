// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Inspect the live preview and its aligned cues; never render a movie.
import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {driverX,wheelAngle,approachScale} from './ending-motion.mjs';
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
  let previousOpeningTime=-Infinity,openingPixels;
  for(const time of [0,1/doc.output.fps,.25,.5,1]){
    await seek(time);
    const frame=await (await fetch(`${origin}/frame?t=${time}`)).json();
    const modelTime=frame.elements['continuous.wheel'].time*doc.model.expectedDurationSeconds;
    assert.ok(modelTime>previousOpeningTime,'The opening wheel moves from the very first frame');
    previousOpeningTime=modelTime;
    const pixels=await page.locator('iframe').screenshot({path:resolve(output,`opening-spin-${time.toFixed(3)}.png`)});
    if(openingPixels)assert.ok(!pixels.equals(openingPixels),'The opening must not hold a static image');
    openingPixels=pixels;
    checks.push({id:'opening-spin',time,modelTime});
  }
  const ancestor=doc.chapters[0].shots.find(s=>s.id==='ancestor');
  const revealOpacity=()=>page.evaluate(()=>{
    const w=document.querySelector('iframe').contentWindow;
    const element=w.document.querySelector('[data-element="continuous.mill"]');
    return element?Number(w.getComputedStyle(element).opacity):0;
  });
  await seek(ancestor.start+.6);
  assert.ok(Math.abs(await revealOpacity()-.5)<.06,
    'The machine must be half faded in at the opening reveal midpoint, not cut in');
  assert.equal(ancestor.transition.kind,'reframe');
  for(const offset of [0,.3,.6,.9,1.25]){
    const time=ancestor.start+offset;
    await seek(time);
    const opacity=await revealOpacity();
    const progress=Math.min(1,offset/1.2),expected=progress*progress*(3-2*progress);
    assert.ok(Math.abs(opacity-expected)<.06);
    const frame=await (await fetch(`${origin}/frame?t=${time}`)).json();
    const wheel=frame.elements['continuous.wheel'],mill=frame.elements['continuous.mill'];
    assert.equal(wheel.time,mill.time,'Both layers show the same rotating wheel pose');
    assert.deepEqual(wheel.view,mill.view,'No double image during the reveal');
    const wheelOpacity=await page.evaluate(()=>{
      const w=document.querySelector('iframe').contentWindow;
      return Number(w.getComputedStyle(w.document.querySelector('[data-element="continuous.wheel"]')).opacity);
    });
    assert.equal(wheelOpacity,1,'The opening wheel stays fully visible');
    await page.locator('iframe').screenshot({path:resolve(output,`opening-reveal-${offset}.png`)});
    checks.push({id:'opening-reveal',time,opacity,wheelOpacity});
  }
  const water=doc.chapters[0].shots.find(s=>s.id==='water');
  await seek(water.start+.6);
  const waterOpacity=await page.evaluate(()=>{
    const w=document.querySelector('iframe').contentWindow;
    return Number(w.getComputedStyle(w.document.querySelector('[data-element="continuous.drive"]')).opacity);
  });
  assert.ok(Math.abs(waterOpacity-.5)<.06,'The 32-second change must fade in live');
  assert.equal(water.transition.kind,'reframe');
  for(const offset of [0,.3,.6,.9,1.25]){
    await seek(water.start+offset);
    const frame=await (await fetch(`${origin}/frame?t=${water.start+offset}`)).json();
    assert.deepEqual(frame.elements['continuous.mill'].view,frame.elements['continuous.drive'].view);
    assert.equal(frame.elements['continuous.mill'].time,frame.elements['continuous.drive'].time);
    if(offset===1.25){
      const withBase=await page.locator('iframe').screenshot();
      await page.evaluate(()=>document.querySelector('iframe').contentDocument
        .querySelector('[data-element="continuous.mill"]').style.visibility='hidden');
      assert.ok(withBase.equals(await page.locator('iframe').screenshot()),'The earlier full machine must be covered after the fade');
      await page.evaluate(()=>document.querySelector('iframe').contentDocument
        .querySelector('[data-element="continuous.mill"]').style.visibility='');
    }
    await page.locator('iframe').screenshot({path:resolve(output,`mechanism-fade-${offset}.png`)});
    checks.push({id:'mechanism-fade',time:water.start+offset});
  }
  for(const id of ['ancestor','document','behind-the-film','mirror','open-source','wheel-returns','invitation']){
    const shot=shots.find(s=>s.id===id);
    for(const fraction of id==='document'||id==='open-source'?[.05,.8]:[.5]){
      const time=shot.start+(shot.end-shot.start)*fraction;
      await seek(time);
      await page.locator('iframe').screenshot({path:resolve(output,`${id}-${fraction}.png`)});
      if(id==='ancestor'){
        const withBase=await page.locator('iframe').screenshot();
        await page.evaluate(()=>document.querySelector('iframe').contentDocument
          .querySelector('[data-element="continuous.wheel"]').style.visibility='hidden');
        const withoutBase=await page.locator('iframe').screenshot();
        assert.ok(withBase.equals(withoutBase),'The faded-in machine must fully cover the old wheel during the orbit');
        await page.evaluate(()=>document.querySelector('iframe').contentDocument
          .querySelector('[data-element="continuous.wheel"]').style.visibility='');
      }
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
          const range=win.document.createRange();range.selectNodeContents(note);
          const textWidth=range.getBoundingClientRect().width;
          const style=win.getComputedStyle(note);
          return {image:{left:img.left,top:img.top,right:img.right,bottom:img.bottom},
            width:win.innerWidth,height:win.innerHeight,text:note.textContent,
            note:{left:box.left,top:box.top,right:box.right,bottom:box.bottom,width:box.width},
            textWidth,padding:parseFloat(style.paddingLeft)+parseFloat(style.paddingRight),background:style.backgroundColor};
        });
        assert.ok(picture.image.left<=0.5&&picture.image.top<=0.5&&picture.image.right>=picture.width-.5&&picture.image.bottom>=picture.height-.5,
          'The manuscript covers every edge of the video');
        assert.equal(picture.text,'Source: Codex Atlanticus 1078r · Wikimedia Commons');
        assert.ok(picture.note.left>picture.width*.3&&picture.note.top>picture.height*.85);
        assert.ok(Math.abs(picture.note.right-picture.width)<.6&&Math.abs(picture.note.bottom-picture.height)<.6,
          'The source plate touches the right and bottom edges');
        assert.notEqual(picture.background,'rgba(0, 0, 0, 0)');
        assert.ok(Math.abs(picture.note.width-picture.textWidth-picture.padding)<1,
          'The source plate hugs the text plus padding, without an empty wide rectangle');
      }
      checks.push({id,time,overflow});
    }
  }
  const source=doc.chapters[0].shots.find(s=>s.id==='behind-the-film');
  assert.ok(source.end-source.start<18,'The enumeration must stay brief');
  const code=doc.chapters[0].elements['film-code'].props.code;
  const shotToken=source.cues.flatMap(c=>c.actions).find(a=>a.params?.token==='Shot');
  assert.ok(shotToken,'The spoken a shot highlights the Shot constructor, not the variable');
  assert.ok(!/^\s*(stroke|end)\s*=/m.test(code),'Speech anchors are inline in the actual shot and cues');
  for(const [id,element,from,to] of [
    ['testing','tests',105,110],['behind-the-film','film-code',source.start,source.start+2],
  ]){
    const full=doc.chapters[0].elements[element].props.code;
    let prior=-1;
    for(const fraction of [0,.25,.5,.75,1]){
      const time=from+(to-from)*fraction;
      await seek(time);
      // The live player's composed dissolve still displays the outgoing shot
      // at the exact onset. Check the incoming source state there, then its DOM.
      if(fraction===0){
        const frame=await (await fetch(`${origin}/frame?t=${time}`)).json();
        const state=frame.elements[`continuous.${element}`];
        assert.equal(state.props.initiallyEmpty,true);
        assert.ok((state.actions.find(a=>a.action==='write')?.progress??0)<.01);
        prior=0;
        checks.push({id:`${id}-typing`,time,characters:0,stateOnly:true});
        continue;
      }
      const shown=await page.evaluate(element=>{
        const pre=document.querySelector('iframe').contentDocument
          .querySelector(`[data-element="continuous.${element}"] pre`).cloneNode(true);
        pre.querySelectorAll('.line-number').forEach(el=>el.remove());
        return [...pre.children].map(el=>el.textContent).join('\n');
      },element);
      assert.ok(shown.length>prior,'Source typing progresses at every sample');
      assert.ok(full.startsWith(shown),'Typing reveals the actual source without rewriting it');
      prior=shown.length;
      if(fraction===0)assert.ok(shown.length<=1);
      if(fraction===1)assert.equal(shown,full);
      if(fraction===.5)await page.locator('iframe').screenshot({path:resolve(output,`${id}-typing.png`)});
      checks.push({id:`${id}-typing`,time,characters:shown.length});
    }
  }
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
  const rope=doc.chapters[0].shots.find(s=>s.id==='consequence');
  const ropeCue=rope.cues.find(c=>c.actions.some(a=>a.action==='highlight'));
  assert.deepEqual(ropeCue.actions[0].parts,[
    ['Feed mechanism','Central small-radius take-up'],
    ['Feed mechanism','Upper roller to thin shaft'],
    ['Feed mechanism','Carriage haul'],
  ]);
  await seek(rope.start+(ropeCue.at+ropeCue.until)/2);
  await page.locator('iframe').screenshot({path:resolve(output,'complete-second-rope.png')});
  checks.push({id:'complete-second-rope',time:rope.start+ropeCue.at,parts:ropeCue.actions[0].parts});
  const open=doc.chapters[0].shots.find(s=>s.id==='open-source');
  const returned=doc.chapters[0].shots.find(s=>s.id==='wheel-returns');
  const props=doc.chapters[0].elements.ecosystem.props;
  const driveStart=open.start+open.cues.find(c=>c.actions.some(a=>a.action==='drive')).at;
  const approachTime=open.start+1.5;
  await seek(approachTime);
  const approachFrame=await (await fetch(`${origin}/frame?t=${approachTime}`)).json();
  const approach=approachFrame.elements['continuous.ecosystem'].actions.find(a=>a.action==='approach');
  const scale=await page.evaluate(()=>{
    const w=document.querySelector('iframe').contentWindow;
    return new w.DOMMatrix(w.getComputedStyle(w.document.querySelector('.constellation')).transform).a;
  });
  assert.ok(Math.abs(scale-approachScale(approach.progress))<.0001,'The approach uses the authored ease-out curve');
  assert.ok(scale>.5,'The M and title advance promptly from the distance');
  await page.locator('iframe').screenshot({path:resolve(output,'open-source-ease-out.png')});
  checks.push({id:'open-source-ease-out',time:approachTime,scale});
  const firstTechnology=open.start+open.cues.find(c=>c.actions.some(a=>
    a.action==='reveal'&&a.params.name==='OpenSCAD')).at;
  for(const time of [approachTime,firstTechnology-1/doc.output.fps,firstTechnology,firstTechnology+.175,firstTechnology+.4]){
    await seek(time);
    const appearance=await page.evaluate(()=>{
      const w=document.querySelector('iframe').contentWindow,d=w.document;
      const circle=d.querySelector('.spokes > g > circle');
      const spoke=d.querySelector('.spokes > g > g');
      return {circle:Number(w.getComputedStyle(circle).opacity),spoke:Number(w.getComputedStyle(spoke).opacity)};
    });
    if(time<firstTechnology)assert.equal(appearance.circle,0,'No circumference during the M/title zoom-in');
    assert.ok(Math.abs(appearance.circle-.22*appearance.spoke)<.00001,
      'The circumference appears with the first OpenSCAD label and spoke');
    if(time>firstTechnology+.35)assert.equal(appearance.circle,.22);
    await page.locator('iframe').screenshot({path:resolve(output,`circumference-${time.toFixed(3)}.png`)});
    checks.push({id:'circumference-arrival',time,...appearance});
  }
  const speechEnd=endOf('a stream of open source tools');
  const returnSpeech=startOf('The wheel... makes revolutions');
  const streamEnd=driveStart+props.streamDuration;
  assert.ok(returned.start<driveStart+6*props.stagger,'The handoff starts before the last tool is released');
  assert.ok(Math.abs(streamEnd-(returnSpeech-.2))<.001,'The slower stream clears just before the returning wheel sentence');
  assert.ok(props.arrival>1.9,'Each label takes nearly two seconds to reach the centre');
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
  for(const [i,name] of props.drivers.entries()){
    const time=driveStart+i*props.stagger+props.arrival;
    await seek(time);
    const label=await page.evaluate(name=>{
      const w=document.querySelector('iframe').contentWindow;
      const el=[...w.document.querySelectorAll('.incoming')].find(el=>el.textContent===name);
      const rect=el.getBoundingClientRect();
      return {width:el.getBBox().width,opacity:Number(w.getComputedStyle(el).opacity),
        fits:rect.left>=0&&rect.right<=w.innerWidth};
    },name);
    assert.ok(label.fits&&label.opacity===1,`The complete ${name} label is visible at centre`);
    let readableFrames=0;
    for(let n=0;n/doc.output.fps<props.streamDuration;n++){
      const elapsed=n/doc.output.fps,age=elapsed-i*props.stagger;
      const x=driverX(age,props),half=label.width/2;
      if(age>=0&&x-half>=48&&x+half<=1872&&elapsed<props.streamDuration-.15)readableFrames++;
    }
    const seconds=readableFrames/doc.output.fps;
    assert.ok(seconds>=3,`${name} stays fully visible for at least three seconds`);
    if(i===props.drivers.length-1)await page.locator('iframe').screenshot({path:resolve(output,'last-tool-over-waterwheel.png')});
    checks.push({id:'tool-reading-window',name,time,fullyVisibleSeconds:seconds});
  }
  for(const [sample,time] of [['late',streamEnd-.6],['cleared',returnSpeech-.05]]){
    await seek(time);
    const result=await page.evaluate(()=>{
      const w=document.querySelector('iframe').contentWindow;
      return {circleOpacity:Number(w.getComputedStyle(w.document.querySelector('.graph-title')).opacity),
        names:[...w.document.querySelectorAll('.incoming')].filter(el=>Number(w.getComputedStyle(el).opacity)>.1&&
          el.getBoundingClientRect().right>0&&el.getBoundingClientRect().left<w.innerWidth).map(el=>el.textContent)};
    });
    assert.equal(result.circleOpacity,0,'Only the stream remains over the waterwheel, not the graphic wheel');
    if(sample==='late')assert.ok(result.names.includes('OpenSpec'),'The last tool remains readable after the graphic wheel fades');
    else assert.deepEqual(result.names,[],'The stream is clear before the returning sentence');
    await page.locator('iframe').screenshot({path:resolve(output,`stream-tail-${sample}.png`)});
    checks.push({id:'stream-tail',sample,time,...result});
  }
  const zoom=returned.cues.find(c=>c.actions.some(a=>a.action==='move'));
  const zoomStart=returned.start+zoom.at,zoomEnd=returned.start+zoom.actions[0].until;
  assert.ok(Math.abs(zoomStart-startOf('and humans...'))<=frameTolerance);
  assert.ok(Math.abs(zoomEnd-endOf('their own'))<=frameTolerance);
  // Measure angular speed from the actual posed model, not the animation helper.
  // Eight similar spokes repeat every 45 degrees; keep each 24 fps step below
  // half that angle while making the zoom substantially faster than a slow turn.
  let previousSpeed=0;
  const speedTimes=[returned.start+2,speechEnd,zoomStart,(zoomStart+zoomEnd)/2,zoomEnd-1/doc.output.fps];
  for(const sample of speedTimes){
    const time=Math.floor(sample*doc.output.fps+1e-9)/doc.output.fps;
    const [before,current]=await Promise.all([time-1/doc.output.fps,time]
      .map(async t=>(await fetch(`${origin}/frame?t=${t}`)).json()));
    const angleStep=(current.elements['continuous.returned'].time-before.elements['continuous.returned'].time)
      *doc.model.expectedDurationSeconds*90;
    const speed=angleStep/(current.time-before.time);
    assert.ok(speed>previousSpeed,'The final wheel keeps accelerating through the zoom');
    assert.ok(angleStep<22.5,'The eight-spoke wheel stays below half a spoke interval per authored frame');
    if(sample>=zoomStart)assert.ok(speed>360,'The zoom must start above one revolution per second');
    if(sample===speedTimes.at(-1))assert.ok(speed>440,'The final wheel reaches a very fast spin');
    previousSpeed=speed;
    await seek(time);
    await page.locator('iframe').screenshot({path:resolve(output,`wheel-speed-${time.toFixed(3)}.png`)});
    checks.push({id:'wheel-acceleration',time,degreesPerSecond:speed,revolutionsPerSecond:speed/360,angleStep});
  }
  const invitation=doc.chapters[0].shots.find(s=>s.id==='invitation');
  assert.equal(invitation.start,zoomEnd,'The closing scene begins after their own ends');
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
  let previousLogoScale=-1;
  let fixedUrlWidth;
  const logoApproach=invitation.cues.find(c=>c.actions.some(a=>a.action==='approach'));
  const logoStart=invitation.start+logoApproach.at;
  assert.ok(Math.abs(logoStart-startOf("I'm Machinome"))<=frameTolerance,
    'The logo approach starts on the recorded I am entrance');
  for(const time of [invitation.start,logoStart-1/doc.output.fps]){
    await seek(time);
    const width=await page.evaluate(()=>document.querySelector('iframe').contentDocument
      .querySelector('.wordmark').getBoundingClientRect().width);
    assert.equal(width,0,'No full-size logo flashes before the spoken I am');
    await page.locator('iframe').screenshot({path:resolve(output,`logo-wait-${time.toFixed(3)}.png`)});
    checks.push({id:'logo-wait',time,width});
  }
  for(const offset of [0,.3,.6,.9,1.25]){
    await seek(logoStart+offset);
    const {opacity,scale,urlWidth}=await page.evaluate(()=>{
      const w=document.querySelector('iframe').contentWindow;
      const style=w.getComputedStyle(w.document.querySelector('.signature'));
      const motion=w.getComputedStyle(w.document.querySelector('.logo-approach'));
      return {opacity:Number(style.opacity),scale:new w.DOMMatrix(motion.transform).a,
        urlWidth:w.document.querySelector('.repository-url').getBoundingClientRect().width};
    });
    fixedUrlWidth??=urlWidth;
    assert.equal(urlWidth,fixedUrlWidth,'The address never scales with the approaching logo');
    assert.equal(opacity,1,'The logo approaches from the distance, without an opacity fade');
    assert.ok(scale>previousLogoScale,'The logo keeps approaching until it settles');
    previousLogoScale=scale;
    if(offset===0)assert.ok(scale<.01,'The logo starts at the wheel-centre vanishing point');
    else if(offset===.6)assert.ok(scale>.45&&scale<.55);
    else if(offset===1.25)assert.equal(scale,1);
    await page.locator('iframe').screenshot({path:resolve(output,`logo-approach-${offset}.png`)});
    checks.push({id:'logo-approach',time:logoStart+offset,opacity,scale});
  }
  const closingFade=invitation.cues.find(c=>c.actions.some(a=>a.action==='link'));
  const linkStart=invitation.start+closingFade.at,linkEnd=invitation.start+closingFade.until;
  assert.ok(Math.abs(linkStart-startOf('Open Source'))<=frameTolerance,'The address fade starts on the closing Open Source');
  assert.ok(Math.abs(linkEnd-endOf('Open Source'))<=frameTolerance,'The address fade completes with the spoken phrase');
  for(const [sample,time] of [['before',linkStart-.25],['start',linkStart],['middle',(linkStart+linkEnd)/2],['after',linkEnd+.15]]){
    await seek(time);
    const result=await page.evaluate(()=>{
      const w=document.querySelector('iframe').contentWindow,d=w.document;
      const url=d.querySelector('.repository-url');
      const license=d.querySelector('.repository-license');
      const licenseBox=license.getBoundingClientRect(),urlBox=url.getBoundingClientRect();
      return {opacity:Number(w.getComputedStyle(url).opacity),urlWidth:url.getBoundingClientRect().width,
        logoWidth:d.querySelector('.wordmark').getBoundingClientRect().width,tagline:!!d.querySelector('.tagline'),
        license:license.textContent,licenseOpacity:Number(w.getComputedStyle(license).opacity),
        licenseBelow:licenseBox.top>urlBox.bottom,licenseFits:licenseBox.left>=0&&licenseBox.right<=w.innerWidth};
    });
    assert.equal(result.tagline,false);
    if(['before','start'].includes(sample))assert.ok(result.opacity<.01,'Only the logo appears until open source');
    else if(sample==='middle')assert.ok(result.opacity>.4&&result.opacity<.6);
    else assert.equal(result.opacity,1);
    assert.equal(result.license,'GPL-2.0-or-later OR CERN-OHL-S-2.0+');
    assert.equal(result.licenseOpacity,result.opacity,'The licence line fades together with the address');
    assert.ok(result.licenseBelow&&result.licenseFits);
    assert.equal(result.urlWidth,fixedUrlWidth,'The address fades at a fixed size');
    assert.ok(result.urlWidth>result.logoWidth&&result.urlWidth<result.logoWidth*1.2,'GitHub address is slightly wider than the logo');
    await page.locator('iframe').screenshot({path:resolve(output,`github-fade-${sample}.png`)});
    checks.push({id:'github-fade',time,...result});
  }
  for(const id of ['behind-the-film','mirror']){
    const shot=doc.chapters[0].shots.find(s=>s.id===id);
    for(const cue of shot.cues){
      const action=cue.actions.find(a=>['blink','blink-all'].includes(a.action));if(!action)continue;
      await seek(shot.start+(cue.at+cue.until)/2);
      const tokens=await page.evaluate(()=>[...document.querySelector('iframe').contentDocument.querySelectorAll('.blink-token')].map(x=>x.textContent));
      const cueSpoken=id==='behind-the-film'&&action.params.token==='spoken';
      const rows=code.split('\n'),firstCue=rows.findIndex(line=>/^\s*Cue\(/.test(line));
      const spokenRows=rows.flatMap((line,i)=>i>=firstCue&&/\bspoken\b/.test(line)
        ?[doc.chapters[0].elements['film-code'].props.numbers[i]]:[]);
      const count=cueSpoken?spokenRows.length:action.action==='blink-all'
        ?[...code.matchAll(/[A-Za-z_][A-Za-z_0-9]*/g)].filter(m=>m[0]===action.params.token).length
        :cue.actions.filter(a=>a.action==='blink').length;
      assert.ok(count>0);
      assert.deepEqual(tokens,Array(count).fill(action.params.token));
      if(cueSpoken){
        assert.equal(count,7,'Only the seven spoken calls inside the four Cues light up');
        const markedRows=await page.evaluate(()=>[...document.querySelector('iframe').contentDocument
          .querySelectorAll('.blink-token')].map(mark=>Number(mark.parentElement.querySelector('.line-number').textContent)));
        assert.deepEqual(markedRows,spokenRows,'Do not jump to the earlier shot-ending spoken call');
      }
      if(action.action==='blink-all'||action.params.token==='Shot'||cueSpoken)
        await page.locator('iframe').screenshot({path:resolve(output,`all-${action.params.token}.png`)});
      checks.push({id,token:action.params.token,from:shot.start+cue.at,to:shot.start+cue.until});
    }
  }
  await seek(outline.output.duration-1);
  assert.equal(await page.evaluate(()=>document.querySelector('iframe').contentDocument.querySelector('.question')),null);
  assert.deepEqual(errors,[]);
  await writeFile(resolve(output,'checks.json'),JSON.stringify({status:'passed',duration:outline.output.duration,checks},null,2)+'\n');
  console.log(`Preview checked: ${checks.length} frames/cues; no video rendered.`);
}finally{await browser.close();}

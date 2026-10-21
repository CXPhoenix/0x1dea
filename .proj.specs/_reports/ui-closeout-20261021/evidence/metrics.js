(() => {
 const rgb=s=>{let a=s.match(/[\d.]+/g).map(Number);return [a[0],a[1],a[2],a[3]??1]};
 const bg=e=>{let s=getComputedStyle(e),c=rgb(s.backgroundColor);if(c[3]===1)return c;if(!e.parentElement)return [255,255,255,1];let b=bg(e.parentElement);return c.map((v,i)=>i<3?v*c[3]+b[i]*(1-c[3]):1)};
 const lum=c=>c.slice(0,3).map(x=>x/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4).reduce((n,x,i)=>n+x*[.2126,.7152,.0722][i],0);
 const contrast=e=>{let a=lum(rgb(getComputedStyle(e).color)),b=lum(bg(e));return (Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
 const box=e=>{let r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}};
 const summaries=[...document.querySelectorAll('aside[role=note]:not(.preview-notice)')];
 return JSON.stringify({url:location.href,theme:document.documentElement.className,viewport:innerWidth,pageWidth:document.documentElement.scrollWidth,
 summaries:summaries.map(e=>({class:e.className,label:e.getAttribute('aria-label'),text:e.innerText,bounds:box(e),contrast:contrast(e),children:[...e.querySelectorAll(':scope > div > ul > li')].map(x=>({text:x.innerText,bounds:box(x),before:getComputedStyle(x,'::before').content,contrast:contrast(x)})),nestedPrompts:[...e.querySelectorAll('li li,.custom-block li')].map(x=>getComputedStyle(x,'::before').content),interactive:e.querySelectorAll('input,button,textarea').length})),
 notices:[...document.querySelectorAll('.preview-notice')].map(e=>({text:e.innerText,label:e.getAttribute('aria-label'),contrast:contrast(e),bounds:box(e),executable:e.querySelectorAll('img,script').length})),
 captions:[...document.querySelectorAll('figcaption,caption')].map(e=>({text:e.innerText,font:parseFloat(getComputedStyle(e).fontSize),contrast:contrast(e),bounds:box(e),clipped:e.scrollWidth>e.clientWidth+1})),
 references:[...document.querySelectorAll('a[href^="#fig-"],a[href^="#tbl-"]')].map(e=>({text:e.innerText,href:e.getAttribute('href'),target:!!document.getElementById(e.hash.slice(1))})),
 recommendation:[...document.querySelectorAll('a')].filter(e=>e.textContent.includes('ENCORE')).map(e=>({text:e.innerText,href:e.getAttribute('href'),links:e.querySelectorAll('a,button,input').length,bounds:box(e),contrast:contrast(e)})),
 sentinel:document.querySelector('.vp-doc')?.innerText.includes('第二個後文 sentinel'),images:[...document.querySelectorAll('.vp-doc img')].map(e=>({src:e.getAttribute('src'),alt:e.alt,loaded:e.complete&&e.naturalWidth>0})),duplicates:[...document.querySelectorAll('[id]')].map(e=>e.id).filter((id,i,a)=>a.indexOf(id)!==i)})
})()
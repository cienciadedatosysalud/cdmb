import{am as b,an as g}from"./index.835f9034.js";function v(t){return t<.5?4*t*t*t:.5*Math.pow(2*t-2,3)+1}function h(t){const a=t-1;return a*a*a+1}function w(t,{delay:a=0,duration:c=400,easing:p=v,amount:i=5,opacity:o=0}={}){const d=getComputedStyle(t),s=+d.opacity,l=d.filter==="none"?"":d.filter,n=s*(1-o),[e,u]=g(i);return{delay:a,duration:c,easing:p,css:(y,$)=>`opacity: ${s-n*$}; filter: ${l} blur(${$*e}${u});`}}function F(t,{delay:a=0,duration:c=400,easing:p=b}={}){const i=+getComputedStyle(t).opacity;return{delay:a,duration:c,easing:p,css:o=>`opacity: ${o*i}`}}function C(t,{delay:a=0,duration:c=400,easing:p=h,x:i=0,y:o=0,opacity:d=0}={}){const s=getComputedStyle(t),l=+s.opacity,n=s.transform==="none"?"":s.transform,e=l*(1-d),[u,y]=g(i),[$,m]=g(o);return{delay:a,duration:c,easing:p,css:(_,f)=>`
			transform: ${n} translate(${(1-_)*u}${y}, ${(1-_)*$}${m});
			opacity: ${l-e*f}`}}function S(t,{delay:a=0,duration:c=400,easing:p=h,axis:i="y"}={}){const o=getComputedStyle(t),d=+o.opacity,s=i==="y"?"height":"width",l=parseFloat(o[s]),n=i==="y"?["top","bottom"]:["left","right"],e=n.map(r=>`${r[0].toUpperCase()}${r.slice(1)}`),u=parseFloat(o[`padding${e[0]}`]),y=parseFloat(o[`padding${e[1]}`]),$=parseFloat(o[`margin${e[0]}`]),m=parseFloat(o[`margin${e[1]}`]),_=parseFloat(o[`border${e[0]}Width`]),f=parseFloat(o[`border${e[1]}Width`]);return{delay:a,duration:c,easing:p,css:r=>`overflow: hidden;opacity: ${Math.min(r*20,1)*d};${s}: ${r*l}px;padding-${n[0]}: ${r*u}px;padding-${n[1]}: ${r*y}px;margin-${n[0]}: ${r*$}px;margin-${n[1]}: ${r*m}px;border-${n[0]}-width: ${r*_}px;border-${n[1]}-width: ${r*f}px;`}}export{C as a,w as b,v as c,F as f,S as s};
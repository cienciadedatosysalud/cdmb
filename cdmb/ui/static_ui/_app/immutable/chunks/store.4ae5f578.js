import{d as s,w as r}from"./index.47d812cb.js";import{e as o}from"./store.6b5c88ac.js";import{a as n}from"./runtime.esm.481ebd84.js";import{ao as l}from"./index.d22cb2b3.js";const i=r(""),m=r(""),q=r(""),w=r("String"),x=r("Categorical"),y=r(""),O=r("Required"),S=r("Observed"),j=r(!1),k=r(""),z=r(""),C=r(""),R=r("");let c={data:void 0,column_name:"",filename:""};const $=r(c),d=s(i,e=>!e.replace(/\s/g,"").length),u=s(i,e=>e.indexOf(" ")>=0),A=s(d,e=>e?l(n)("entities.modal_label_required"):""),B=s(u,e=>e?l(n)("entities.modal_label_spaces"):""),f=s(m,e=>!e.replace(/\s/g,"").length),D=s(f,e=>e?l(n)("entities.modal_description_required"):""),E=s(o,e=>{let t=[];for(let a of e)a.name.indexOf(" ")>=0||!a.name.replace(/\s/g,"").length?t.push(!0):t.push(!1);return t}),F=s(o,e=>{let t=[];for(let a of e)a.variables.length==0?t.push(!0):t.push(!1);return t}),G=s(o,e=>{let t=!1,a=e.map(_=>_.name);return new Set(a).size!=a.length&&(t=!0),t});export{j as a,S as b,$ as c,m as d,R as e,w as f,k as g,E as h,G as i,F as j,d as k,i as l,u as m,f as n,z as o,C as p,A as q,O as r,q as s,x as t,y as u,B as v,D as w};
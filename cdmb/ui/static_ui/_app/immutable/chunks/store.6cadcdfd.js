import{d as e}from"./index.258591cf.js";import{h as n,u,v as c,j as i}from"./store.30bfcf08.js";import{a as o}from"./runtime.esm.58062527.js";import{aq as a}from"./index.835f9034.js";const p=e(n,r=>!r.replace(/\s/g,"").length),v=e(p,r=>r?a(o)("project.project_required"):""),_=e(u,r=>!r.replace(/\s/g,"").length),x=e(_,r=>r?a(o)("project.usecase_required"):""),l=e(c,r=>!new RegExp(/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$/gm).test(r)),z=e(l,r=>r?a(o)("project.sematic_version_error"):""),A=e(i,r=>{let t=[];for(let s of r)!new RegExp(/^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$/gm).test(s.id)&&s.id.replace(/\s/g,"").length?t.push(!0):t.push(!1);return t});export{v as a,_ as b,x as c,l as d,p as e,z as f,A as g};
import{d as e}from"./index.BJGfC3rd.js";import{p as n,u,v as c,a as p}from"./store.BaiRHQQa.js";import{$ as o}from"./runtime.BaKyRKnx.js";import{E as a}from"./scheduler.8EYOJlnQ.js";const i=e(n,r=>!r.replace(/\s/g,"").length),v=e(i,r=>r?a(o)("project.project_required"):""),_=e(u,r=>!r.replace(/\s/g,"").length),x=e(_,r=>r?a(o)("project.usecase_required"):""),l=e(c,r=>!new RegExp(/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$/gm).test(r)),z=e(l,r=>r?a(o)("project.sematic_version_error"):""),A=e(p,r=>{let t=[];for(let s of r)!new RegExp(/^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$/gm).test(s.id)&&s.id.replace(/\s/g,"").length?t.push(!0):t.push(!1);return t});export{v as a,_ as b,x as c,l as d,i as e,z as f,A as g};

import{S as he,i as ge,s as ke,e as j,b as y,g as p,v as V,d as k,f as W,h as g,V as Z,a7 as ve,a2 as ye,R as B,W as J,k as T,a as A,y as F,l as z,m as D,c as L,z as O,n as v,F as re,A as H,G as S,ah as Ce,a9 as x,aa as Ee,U as je,Z as we,B as I,a1 as ne,a3 as $,N as K,ap as ee,O as U,P as G,Q,q as Ne,r as Te,u as ze}from"./index.d8ca07a9.js";import{c as P}from"./Indicator.svelte_svelte_type_style_lang.e2c519f7.js";import{F as R}from"./store.4d7a1ebc.js";import{C as fe}from"./CloseButton.0aecb936.js";const De=`
  a[href], area[href], input:not([disabled]):not([tabindex='-1']),
  button:not([disabled]):not([tabindex='-1']),select:not([disabled]):not([tabindex='-1']),
  textarea:not([disabled]):not([tabindex='-1']),
  iframe, object, embed, *[tabindex]:not([tabindex='-1']):not([disabled]), *[contenteditable=true]
`;function Se(a){const t=Array.from(a.querySelectorAll(De));function s(e){if(!(e.key==="Tab"||e.keyCode===9))return;let o=t.indexOf(document.activeElement);o===-1&&e.shiftKey&&(o=0),o+=t.length+(e.shiftKey?-1:1),o%=t.length,t[o].focus(),e.preventDefault()}return document.addEventListener("keydown",s,!0),{destroy(){document.removeEventListener("keydown",s,!0)}}}const Fe=a=>({}),te=a=>({}),Oe=a=>({}),le=a=>({});function se(a){let t,s,e,l,o,c,i,r,_,E;const h=[{rounded:!0},{shadow:!0},a[13],{class:a[6]}];let C={$$slots:{default:[Ae]},$$scope:{ctx:a}};for(let d=0;d<h.length;d+=1)C=B(C,h[d]);return c=new R({props:C}),{c(){t=T("div"),e=A(),l=T("div"),o=T("div"),F(c.$$.fragment),this.h()},l(d){t=z(d,"DIV",{class:!0}),D(t).forEach(g),e=L(d),l=z(d,"DIV",{class:!0,tabindex:!0,"aria-modal":!0,role:!0});var u=D(l);o=z(u,"DIV",{class:!0});var m=D(o);O(c.$$.fragment,m),m.forEach(g),u.forEach(g),this.h()},h(){v(t,"class",s=P("fixed inset-0 z-40",a[5])),v(o,"class",i="flex relative "+a[9][a[2]]+" w-full max-h-full"),v(l,"class",P("fixed top-0 left-0 right-0 h-modal md:inset-0 md:h-full z-50 w-full p-4 flex",...a[8]())),v(l,"tabindex","-1"),v(l,"aria-modal","true"),v(l,"role","dialog")},m(d,u){y(d,t,u),y(d,e,u),y(d,l,u),re(l,o),H(c,o,null),r=!0,_||(E=[S(l,"keydown",a[12]),S(l,"wheel",Ce(a[18]),{passive:!1}),x(a[7].call(null,l)),x(Se.call(null,l)),S(l,"click",function(){Ee(a[3]?a[10]:null)&&(a[3]?a[10]:null).apply(this,arguments)})],_=!0)},p(d,u){a=d,(!r||u&32&&s!==(s=P("fixed inset-0 z-40",a[5])))&&v(t,"class",s);const m=u&8256?je(h,[h[0],h[1],u&8192&&we(a[13]),u&64&&{class:a[6]}]):{};u&1073170&&(m.$$scope={dirty:u,ctx:a}),c.$set(m),(!r||u&4&&i!==(i="flex relative "+a[9][a[2]]+" w-full max-h-full"))&&v(o,"class",i)},i(d){r||(p(c.$$.fragment,d),r=!0)},o(d){k(c.$$.fragment,d),r=!1},d(d){d&&g(t),d&&g(e),d&&g(l),I(c),_=!1,ne(E)}}}function He(a){let t,s;return t=new fe({props:{name:"Close modal",class:"absolute top-3 right-2.5",color:a[13].color}}),t.$on("click",a[11]),{c(){F(t.$$.fragment)},l(e){O(t.$$.fragment,e)},m(e,l){H(t,e,l),s=!0},p(e,l){const o={};l&8192&&(o.color=e[13].color),t.$set(o)},i(e){s||(p(t.$$.fragment,e),s=!0)},o(e){k(t.$$.fragment,e),s=!1},d(e){I(t,e)}}}function Ie(a){let t,s;return t=new R({props:{color:a[13].color,class:"flex justify-between items-center p-4 rounded-t border-b",$$slots:{default:[Ve]},$$scope:{ctx:a}}}),{c(){F(t.$$.fragment)},l(e){O(t.$$.fragment,e)},m(e,l){H(t,e,l),s=!0},p(e,l){const o={};l&8192&&(o.color=e[13].color),l&1056786&&(o.$$scope={dirty:l,ctx:e}),t.$set(o)},i(e){s||(p(t.$$.fragment,e),s=!0)},o(e){k(t.$$.fragment,e),s=!1},d(e){I(t,e)}}}function Pe(a){let t,s,e;return{c(){t=T("h3"),s=Ne(a[1]),this.h()},l(l){t=z(l,"H3",{class:!0});var o=D(t);s=Te(o,a[1]),o.forEach(g),this.h()},h(){v(t,"class",e="text-xl font-semibold "+(a[13].color?"":"text-gray-900 dark:text-white")+" p-0")},m(l,o){y(l,t,o),re(t,s)},p(l,o){o&2&&ze(s,l[1]),o&8192&&e!==(e="text-xl font-semibold "+(l[13].color?"":"text-gray-900 dark:text-white")+" p-0")&&v(t,"class",e)},d(l){l&&g(t)}}}function ae(a){let t,s;return t=new fe({props:{name:"Close modal",color:a[13].color}}),t.$on("click",a[11]),{c(){F(t.$$.fragment)},l(e){O(t.$$.fragment,e)},m(e,l){H(t,e,l),s=!0},p(e,l){const o={};l&8192&&(o.color=e[13].color),t.$set(o)},i(e){s||(p(t.$$.fragment,e),s=!0)},o(e){k(t.$$.fragment,e),s=!1},d(e){I(t,e)}}}function Ve(a){let t,s,e;const l=a[17].header,o=K(l,a,a[20],le),c=o||Pe(a);let i=!a[4]&&ae(a);return{c(){c&&c.c(),t=A(),i&&i.c(),s=j()},l(r){c&&c.l(r),t=L(r),i&&i.l(r),s=j()},m(r,_){c&&c.m(r,_),y(r,t,_),i&&i.m(r,_),y(r,s,_),e=!0},p(r,_){o?o.p&&(!e||_&1048576)&&U(o,l,r,r[20],e?Q(l,r[20],_,Oe):G(r[20]),le):c&&c.p&&(!e||_&8194)&&c.p(r,e?_:-1),r[4]?i&&(V(),k(i,1,1,()=>{i=null}),W()):i?(i.p(r,_),_&16&&p(i,1)):(i=ae(r),i.c(),p(i,1),i.m(s.parentNode,s))},i(r){e||(p(c,r),p(i),e=!0)},o(r){k(c,r),k(i),e=!1},d(r){c&&c.d(r),r&&g(t),i&&i.d(r),r&&g(s)}}}function oe(a){let t,s;return t=new R({props:{color:a[13].color,class:"flex items-center p-6 space-x-2 rounded-b border-t",$$slots:{default:[We]},$$scope:{ctx:a}}}),{c(){F(t.$$.fragment)},l(e){O(t.$$.fragment,e)},m(e,l){H(t,e,l),s=!0},p(e,l){const o={};l&8192&&(o.color=e[13].color),l&1048576&&(o.$$scope={dirty:l,ctx:e}),t.$set(o)},i(e){s||(p(t.$$.fragment,e),s=!0)},o(e){k(t.$$.fragment,e),s=!1},d(e){I(t,e)}}}function We(a){let t;const s=a[17].footer,e=K(s,a,a[20],te);return{c(){e&&e.c()},l(l){e&&e.l(l)},m(l,o){e&&e.m(l,o),t=!0},p(l,o){e&&e.p&&(!t||o&1048576)&&U(e,s,l,l[20],t?Q(s,l[20],o,Fe):G(l[20]),te)},i(l){t||(p(e,l),t=!0)},o(l){k(e,l),t=!1},d(l){e&&e.d(l)}}}function Ae(a){let t,s,e,l,o,c,i,r,_;const E=[Ie,He],h=[];function C(n,b){return n[14].header||n[1]?0:n[4]?-1:1}~(t=C(a))&&(s=h[t]=E[t](a));const d=a[17].default,u=K(d,a,a[20],null);let m=a[14].footer&&oe(a);return{c(){s&&s.c(),e=A(),l=T("div"),u&&u.c(),o=A(),m&&m.c(),c=j(),this.h()},l(n){s&&s.l(n),e=L(n),l=z(n,"DIV",{id:!0,class:!0});var b=D(l);u&&u.l(b),b.forEach(g),o=L(n),m&&m.l(n),c=j(),this.h()},h(){v(l,"id","modal"),v(l,"class","p-6 space-y-6 flex-1 overflow-y-auto overscroll-contain")},m(n,b){~t&&h[t].m(n,b),y(n,e,b),y(n,l,b),u&&u.m(l,null),y(n,o,b),m&&m.m(n,b),y(n,c,b),i=!0,r||(_=[S(l,"keydown",ee(a[12])),S(l,"wheel",ee(a[19]),{passive:!0})],r=!0)},p(n,b){let w=t;t=C(n),t===w?~t&&h[t].p(n,b):(s&&(V(),k(h[w],1,1,()=>{h[w]=null}),W()),~t?(s=h[t],s?s.p(n,b):(s=h[t]=E[t](n),s.c()),p(s,1),s.m(e.parentNode,e)):s=null),u&&u.p&&(!i||b&1048576)&&U(u,d,n,n[20],i?Q(d,n[20],b,null):G(n[20]),null),n[14].footer?m?(m.p(n,b),b&16384&&p(m,1)):(m=oe(n),m.c(),p(m,1),m.m(c.parentNode,c)):m&&(V(),k(m,1,1,()=>{m=null}),W())},i(n){i||(p(s),p(u,n),p(m),i=!0)},o(n){k(s),k(u,n),k(m),i=!1},d(n){~t&&h[t].d(n),n&&g(e),n&&g(l),u&&u.d(n),n&&g(o),m&&m.d(n),n&&g(c),r=!1,ne(_)}}}function Le(a){let t,s,e=a[0]&&se(a);return{c(){e&&e.c(),t=j()},l(l){e&&e.l(l),t=j()},m(l,o){e&&e.m(l,o),y(l,t,o),s=!0},p(l,[o]){l[0]?e?(e.p(l,o),o&1&&p(e,1)):(e=se(l),e.c(),p(e,1),e.m(t.parentNode,t)):e&&(V(),k(e,1,1,()=>{e=null}),W())},i(l){s||(p(e),s=!0)},o(l){k(e),s=!1},d(l){e&&e.d(l),l&&g(t)}}}function Me(a,t,s){const e=["open","title","size","placement","autoclose","permanent","backdropClasses","defaultClass"];let l=Z(t,e),{$$slots:o={},$$scope:c}=t;const i=ve(o);let{open:r=!1}=t,{title:_=""}=t,{size:E="md"}=t,{placement:h="center"}=t,{autoclose:C=!1}=t,{permanent:d=!1}=t,{backdropClasses:u="bg-gray-900 bg-opacity-50 dark:bg-opacity-80"}=t,{defaultClass:m="relative flex flex-col mx-auto"}=t;const n=ye();function b(f){const N=document.createTreeWalker(f,NodeFilter.SHOW_ELEMENT);let q;for(;q=N.nextNode();)if(q instanceof HTMLElement){const Y=q,[be,pe]=ue(Y);(be||pe)&&(Y.tabIndex=0)}f.focus()}const w=()=>{switch(h){case"top-left":return["justify-start","items-start"];case"top-center":return["justify-center","items-start"];case"top-right":return["justify-end","items-start"];case"center-left":return["justify-start","items-center"];case"center":return["justify-center","items-center"];case"center-right":return["justify-end","items-center"];case"bottom-left":return["justify-start","items-end"];case"bottom-center":return["justify-center","items-end"];case"bottom-right":return["justify-end","items-end"];default:return["justify-center","items-center"]}},ie={xs:"max-w-md",sm:"max-w-lg",md:"max-w-2xl",lg:"max-w-4xl",xl:"max-w-7xl"},ce=f=>{const N=f.target;C&&(N==null?void 0:N.tagName)==="BUTTON"&&M(f)},M=f=>{f.preventDefault(),s(0,r=!1)};let X;const ue=f=>[f.scrollWidth>f.clientWidth&&["scroll","auto"].indexOf(getComputedStyle(f).overflowX)>=0,f.scrollHeight>f.clientHeight&&["scroll","auto"].indexOf(getComputedStyle(f).overflowY)>=0];function me(f){if(f.key==="Escape"&&!d)return M(f)}function de(f){$.call(this,a,f)}function _e(f){$.call(this,a,f)}return a.$$set=f=>{s(24,t=B(B({},t),J(f))),s(13,l=Z(t,e)),"open"in f&&s(0,r=f.open),"title"in f&&s(1,_=f.title),"size"in f&&s(2,E=f.size),"placement"in f&&s(15,h=f.placement),"autoclose"in f&&s(3,C=f.autoclose),"permanent"in f&&s(4,d=f.permanent),"backdropClasses"in f&&s(5,u=f.backdropClasses),"defaultClass"in f&&s(16,m=f.defaultClass),"$$scope"in f&&s(20,c=f.$$scope)},a.$$.update=()=>{a.$$.dirty&1&&n(r?"open":"hide"),s(6,X=P(m,t.class))},t=J(t),[r,_,E,C,d,u,X,b,w,ie,ce,M,me,l,i,h,m,o,de,_e,c]}class Ge extends he{constructor(t){super(),ge(this,t,Me,Le,ke,{open:0,title:1,size:2,placement:15,autoclose:3,permanent:4,backdropClasses:5,defaultClass:16})}}export{Ge as M};

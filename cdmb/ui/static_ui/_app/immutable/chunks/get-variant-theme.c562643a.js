import{d,f as b}from"./Space.81935c0b.js";const l=(o,n)=>{const{themeColor:r,rgba:e}=b,a={"&.disabled":{pointerEvents:"none",borderColor:"transparent",backgroundColor:"rgb(233, 236, 239)",background:"rgb(233, 236, 239)",color:"rgb(173, 181, 189)",cursor:"not-allowed"}},t={filled:{[`${d.selector} &`]:{backgroundColor:r(o,8)},border:"transparent",backgroundColor:r(o,6),color:"White","&:hover":{backgroundColor:r(o,7)},...a},light:{[`${d.selector} &`]:{backgroundColor:e(r(o,8),.35),color:o==="dark"?r("dark",0):r(o,2),"&:hover":{backgroundColor:e(r(o,7),.45)}},border:"transparent",backgroundColor:r(o,0),color:o==="dark"?r("dark",9):r(o,6),"&:hover":{backgroundColor:r(o,1)},...a},outline:{[`${d.selector} &`]:{border:`1px solid ${r(o,4)}`,color:`${r(o,4)}`,"&:hover":{backgroundColor:e(r(o,4),.05)}},border:`1px solid ${r(o,7)}`,backgroundColor:"transparent",color:r(o,7),"&:hover":{backgroundColor:e(r(o,0),.35)},...a},subtle:{[`${d.selector} &`]:{color:o==="dark"?r("dark",0):r(o,2),"&:hover":{backgroundColor:e(r(o,8),.35)}},border:"transparent",backgroundColor:"transparent",color:o==="dark"?r("dark",9):r(o,6),"&:hover":{backgroundColor:r(o,0)},...a},default:{[`${d.selector} &`]:{border:`1px solid ${r("dark",5)}`,backgroundColor:r("dark",5),color:"White","&:hover":{backgroundColor:r("dark",4)}},border:`1px solid ${r("gray",4)}`,backgroundColor:"White",color:"Black","&:hover":{backgroundColor:r("gray",0)},...a},white:{border:"transparent",backgroundColor:"White",color:r(o,7),"&:hover":{backgroundColor:"White"},...a},gradient:{}};return n&&(t.gradient={border:"transparent",background:`linear-gradient(${n.deg}deg, $${n.from}600 0%, $${n.to}600 100%)`,color:"White"}),t};export{l as v};

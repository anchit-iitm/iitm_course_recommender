import{_ as h,o as m,e as p,w as n,a as l,a1 as o,a7 as r,b as u,$ as a,a9 as c,ay as i,a0 as t}from"./index-af240f69.js";import{V as g}from"./VContainer-dc02ce2b.js";import{V as _}from"./VCol-7430c998.js";import{V}from"./VRow-3a9fd07a.js";/* empty css              */const b={data(){return{cards:[{title:"Student Details",data:{}},{title:"Course Details",data:{}},{title:"Non-Student Details",data:{}}]}},mounted:async function(){let f=sessionStorage.getItem("token");await fetch("/api/v1/stats/general",{method:"GET",headers:{Authorization:`Bearer ${f}`,"Content-Type":"application/json"}}).then(s=>s.json().then(d=>({response:s,data:d}))).then(({response:s,data:d})=>{if(!s.ok)throw new Error(`Error ${s.status}: ${d.msg}`);this.cards[0].data=d.students,this.cards[1].data=d.courses,this.cards[2].data=d.admins}).catch(s=>{console.log(s)})}},D=t("td",null,"Total",-1),T=t("td",null,"Foundation",-1),x=t("td",null,"Diploma",-1),C=t("td",null,"BSc",-1),w=t("td",null,"BS",-1),y=t("td",null,"Total",-1),B=t("td",null,"Foundation",-1),S=t("td",null,"Diploma",-1),k=t("td",null,"Degree",-1),v=t("td",null,"Admins",-1),N=t("td",null,"Course Team Members",-1),A=t("td",null,"IITM Management",-1);function E(f,s,d,I,e,M){return m(),p(g,{"fill-height":"",fluid:"",class:"down-top-padding"},{default:n(()=>[l(V,null,{default:n(()=>[l(_,{cols:"3",lg:"4"},{default:n(()=>[l(o,{elevation:"3"},{default:n(()=>[l(r,{class:"text-center"},{default:n(()=>[u(a(e.cards[0].title),1)]),_:1}),l(c),l(i,null,{default:n(()=>[t("tbody",null,[t("tr",null,[D,t("td",null,a(e.cards[0].data.total),1)]),t("tr",null,[T,t("td",null,a(e.cards[0].data.foundation),1)]),t("tr",null,[x,t("td",null,a(e.cards[0].data.diploma),1)]),t("tr",null,[C,t("td",null,a(e.cards[0].data.bsc),1)]),t("tr",null,[w,t("td",null,a(e.cards[0].data.bs),1)])])]),_:1})]),_:1})]),_:1}),l(_,{cols:"3",lg:"4"},{default:n(()=>[l(o,{elevation:"3"},{default:n(()=>[l(r,{class:"text-center"},{default:n(()=>[u(a(e.cards[1].title),1)]),_:1}),l(c),l(i,null,{default:n(()=>[t("tbody",null,[t("tr",null,[y,t("td",null,a(e.cards[1].data.total),1)]),t("tr",null,[B,t("td",null,a(e.cards[1].data.foundation),1)]),t("tr",null,[S,t("td",null,a(e.cards[1].data.diploma),1)]),t("tr",null,[k,t("td",null,a(e.cards[1].data.degree),1)])])]),_:1})]),_:1})]),_:1}),l(_,{cols:"3",lg:"4"},{default:n(()=>[l(o,{elevation:"3"},{default:n(()=>[l(r,{class:"text-center"},{default:n(()=>[u(a(e.cards[2].title),1)]),_:1}),l(c),l(i,null,{default:n(()=>[t("tbody",null,[t("tr",null,[v,t("td",null,a(e.cards[2].data.superadmins),1)]),t("tr",null,[N,t("td",null,a(e.cards[2].data.ctm),1)]),t("tr",null,[A,t("td",null,a(e.cards[2].data.management),1)])])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})}const q=h(b,[["render",E]]);export{q as default};

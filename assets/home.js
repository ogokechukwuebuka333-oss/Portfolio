(()=>{
const STAGES=["Discover","Define","Design","Test","Handoff"];
const TYPE={Research:["R","var(--violet-soft)","var(--violet)"],UX:["UX","var(--accent-soft)","var(--accent)"],Visual:["V","var(--warn-soft)","var(--warn)"],Docs:["D","var(--good-soft)","var(--good)"],Systems:["S","var(--accent-soft)","var(--accent)"]};
const P=[
 {id:"betalmighty",title:"Product designer",code:"BA-01",name:"BetAlmighty",sector:"Fintech · Betting",hue:218,x:1,y:1,w:3,d:3,h:4,status:"Case study",tone:"good",stage:5,page:"/betalmighty",
  metric:["Screens","135"],role:"Product designer, iOS app",
  summary:"A Nigerian betting app where friends stake against each other and the money waits in escrow. I designed the iOS app end to end: betting, escrow, wallet, lottery, community and responsible gambling.",
  items:[["135-screen iOS app","UX"],["Escrow state system","Systems"],["Responsible gambling tools","UX"],["Wallet: bank, card, crypto","UX"],["Design tokens","Visual"]],tags:"fintech betting escrow lottery wallet ios responsible gambling"},
 {id:"dnt",title:"Product designer",code:"DN-02",name:"Dataset Nexus Tech",short:"Dataset Nexus",sector:"Edtech · Learning platform",hue:176,x:10.3,y:0.8,w:2.2,d:2,h:3,status:"Case study",tone:"good",stage:3,build:{f:.5,crane:[12.7,3.25]},pinUp:44,page:"/activation-rescue",
  metric:["Sign-up","15+ fields → 2"],role:"Product designer",
  summary:"A learning platform where new learners waited days for a sales-led onboarding. I redesigned it into self-service with instant access, and I lead the design team's critiques.",
  items:[["Self-service onboarding","UX"],["Two-field sign-up","UX"],["Design system","Systems"],["Discovery: a new learner segment","Research"]],tags:"edtech onboarding activation sign-up design system critique"},
 {id:"myestate",title:"Product designer on the team",code:"ME-04",name:"MyEstates",sector:"Proptech · Estate management",hue:150,x:7.6,y:2.4,w:1.8,d:1.9,h:2.6,status:"Case study",tone:"good",stage:4,page:"/myestate",
  metric:["Roles","5 kinds of user"],role:"Product designer on the team · resident experience",
  summary:"Estate management for gated communities: estates register and get approved, committees bill and enforce dues, and residents pay and keep a permanent record.",
  items:[["Role and permission map","Systems"],["Resident app wireframes","UX"],["Payment and failure states","UX"]],tags:"proptech estate residents dues payments roles permissions"},
 {id:"hassanah",hidden:true,title:"Brand strategist",code:"HS-07",name:"Hassanah Shonibare",short:"Hassanah",sector:"Fashion · Brand identity",hue:36,x:7.6,y:2.4,w:1.8,d:1.9,h:2.6,status:"In progress",tone:"warn",stage:1,build:{f:.3,crane:[7.25,2.05]},
  metric:["Archetype","Creator + Outlaw"],role:"Brand strategy and identity",
  summary:"Brand identity exploration for a Nigerian creative fashion house: archetype framing, positioning language and visual direction.",
  items:[["Archetype framing","Research"],["Positioning language","Docs"],["Visual identity direction","Visual"]],tags:"fashion brand identity strategy"},
 {id:"soundyaad",title:"Artist Relationship Manager",code:"SY-03",name:"Soundyaad",sector:"Music-tech · Artist platform",hue:6,x:1,y:8,w:2,d:2,h:3.4,status:"Case study",tone:"good",stage:4,build:{f:.65,crane:[.45,7.45]},page:"/soundyaad",
  metric:["Focus","Feature adoption"],role:"Artist Relationship Manager",nondesign:true,
  summary:"A platform for independent African artists. Artists signed up but few started, so I diagnosed why, fixed how we measure it and set out what should change.",
  items:[["Activation diagnosis","Research"],["Metric definitions","Docs"],["Segmented onboarding messages","UX"],["Explainer videos","Visual"]],tags:"music artists retention adoption"},
 {id:"hq",title:"Product designer",code:"HQ",name:"Studio HQ",sector:"About · Contact",hue:222,x:8.3,y:8.4,w:1.7,d:1.2,h:1.5,hq:true,tags:"about contact skills hire"}
].filter(p=>!p.hidden); // hidden projects stay in the data but leave the city and the cards
const byId=Object.fromEntries(P.map(p=>[p.id,p]));
const N=13, TW=64, TH=32, HZ=26;
const svg=document.getElementById("scene");
let sel="betalmighty";
const HOME={x:-450,y:-150,w:900,h:600};
let vb={...HOME};

const dark=()=>{const t=document.documentElement.getAttribute("data-theme");if(t)return t==="dark";return matchMedia("(prefers-color-scheme: dark)").matches};
const iso=(x,y,z=0)=>[(x-y)*TW/2,(x+y)*TH/2-z*HZ];
const pts=a=>a.map(p=>p[0].toFixed(1)+","+p[1].toFixed(1)).join(" ");
const poly=(a,f,ex="")=>`<polygon points="${pts(a)}" fill="${f}" ${ex}/>`;
function rnd(s){let t=s;return()=>{t=(t*9301+49297)%233280;return t/233280}}

function box(x,y,w,d,h,c,z0=0){
  const top=[iso(x,y,z0+h),iso(x+w,y,z0+h),iso(x+w,y+d,z0+h),iso(x,y+d,z0+h)];
  const L=[iso(x,y+d,z0),iso(x+w,y+d,z0),iso(x+w,y+d,z0+h),iso(x,y+d,z0+h)];
  const R=[iso(x+w,y,z0),iso(x+w,y+d,z0),iso(x+w,y+d,z0+h),iso(x+w,y,z0+h)];
  return poly(L,c.l)+poly(R,c.r)+poly(top,c.t);
}
function pal(n){return n?{ground:"#1B1D22",side1:"#131418",side2:"#0E0F12",grid:"rgba(236,226,206,.06)",road:"#25272D",line:"rgba(255,214,120,.35)",tree:"#24584A",tree2:"#1C4639",trunk:"#3A2E25",crate:"#5B4A35",crate2:"#4A3B2A",crate3:"#6B5840",lamp:"#FFD27A",body:"#C9D4E8",bodyS:"#8E9CB8",shadow:"rgba(0,0,0,.35)"}
  :{ground:"#E6E2D9",side1:"#D2CDC1",side2:"#C3BDB0",grid:"rgba(70,58,36,.07)",road:"#D6D1C6",line:"rgba(255,255,255,.95)",tree:"#86CBA0",tree2:"#6DB68A",trunk:"#9A7A5A",crate:"#E3C08F",crate2:"#C9A26D",crate3:"#F0D3AA",lamp:"#9AA8C0",body:"#FFFFFF",bodyS:"#D3DBE8",shadow:"rgba(60,48,28,.14)"}}
function bcol(h,n,hq){
  if(n) return {t:`hsl(${h} 24% 30%)`,l:`hsl(${h} 34% 21%)`,r:`hsl(${h} 36% 16%)`,win:"#FFD27A",winOff:`hsl(${h} 30% 26%)`,roof:`hsl(${h} 22% 36%)`};
  return hq?{t:"#FFFFFF",l:"hsl(222 70% 60%)",r:"hsl(222 66% 50%)",win:"hsl(222 90% 92%)",winOff:"hsl(222 90% 92%)",roof:"hsl(222 30% 90%)"}
           :{t:`hsl(${h} 35% 96%)`,l:`hsl(${h} 58% 64%)`,r:`hsl(${h} 54% 53%)`,win:`hsl(${h} 85% 90%)`,winOff:`hsl(${h} 85% 90%)`,roof:`hsl(${h} 25% 88%)`};
}
function windows(p,c,n,r){
  let s="";const floors=Math.max(1,Math.floor(p.h));
  const fh=p.h/floors;
  const face=(len,fn)=>{const cols=Math.max(1,Math.floor(len/0.5));
    for(let f=0;f<floors;f++){for(let k=0;k<cols;k++){
      const u0=(k+.22)/cols,u1=(k+.78)/cols,v0=f*fh+fh*.32,v1=f*fh+fh*.74;
      if(p.id==="betalmighty"&&f===0&&k%2===0) continue;
      const on=!n||r()>.32;
      s+=poly([fn(u0,v0),fn(u1,v0),fn(u1,v1),fn(u0,v1)],on?c.win:c.winOff,(n&&on?'opacity=".95"':'opacity=".85"')+(p.id==="betalmighty"&&r()>.8?` class="tw" style="animation-delay:-${(r()*6).toFixed(1)}s"`:""));
    }}};
  face(p.w,(u,v)=>iso(p.x+u*p.w,p.y+p.d,v));
  face(p.d,(u,v)=>iso(p.x+p.w,p.y+u*p.d,v));
  return s;
}
function docks(p,n){ // loading bays on the hero building
  if(p.id!=="betalmighty")return "";let s="";
  for(let k=0;k<3;k++){const u0=(k*2+.25)/6*1,u1=(k*2+1.05)/6;
    const fn=(u,v)=>iso(p.x+p.w,p.y+u*p.d,v);
    s+=poly([fn(u0,0),fn(u1,0),fn(u1,.75),fn(u0,.75)],n?"#0B1222":"hsl(218 40% 32%)");}
  return s;
}

// ---------- construction sites ----------
const L=(a,b,st,w=1.2,ex="")=>`<line x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}" stroke="${st}" stroke-width="${w}" stroke-linecap="round" ${ex}/>`;
function worker(pt,n,mode,to,t){
  const vest="#F47A1F",hat="#FFC61A",skin="#6B4226",pants=n?"#8FA0C4":"#2B3956";
  const mv=to?`style="--dx:${(to[0]-pt[0]).toFixed(1)}px;--dy:${(to[1]-pt[1]).toFixed(1)}px;--t:${t||5}s"`:"";
  return `<g transform="translate(${pt[0].toFixed(1)},${pt[1].toFixed(1)})"><g class="wk ${mode}" ${mv}>
    <ellipse cx="0" cy="0.5" rx="4" ry="1.4" fill="rgba(0,0,0,.18)"/>
    <g class="legs">${L([-1.4,0],[-1.4,-5],pants,1.9)}${L([1.4,0],[1.4,-5],pants,1.9)}</g>
    <rect x="-3.2" y="-11.5" width="6.4" height="7.2" rx="1.6" fill="${vest}"/><rect x="-3.2" y="-8.4" width="6.4" height="1.1" fill="#FFF3C4" opacity=".9"/>
    <g class="arm">${L([2.6,-10],[6.2,-13.4],vest,1.7)}<rect x="5.2" y="-16" width="3.2" height="2.2" rx=".5" fill="#4A4F5A"/></g>
    <circle cx="0" cy="-13.9" r="2.3" fill="${skin}"/><path d="M-3.1 -14.4a3.1 3.1 0 0 1 6.2 0z" fill="${hat}"/>${L([-3.6,-14.4],[3.6,-14.4],hat,1.1)}
  </g></g>`;
}
function civ(pt,n,shirt,to,t,delay){
  const pants=n?"#7E8BA8":"#3B4660", skin=n?"#8A5A3C":"#7A4A2A";
  return `<g transform="translate(${pt[0].toFixed(1)},${pt[1].toFixed(1)})"><g class="wk walk" style="--dx:${(to[0]-pt[0]).toFixed(1)}px;--dy:${(to[1]-pt[1]).toFixed(1)}px;--t:${t}s;animation-delay:${delay||0}s">
   <ellipse cx="0" cy=".5" rx="3.6" ry="1.3" fill="rgba(0,0,0,.16)"/><g class="legs">${L([-1.3,0],[-1.3,-5],pants,1.8)}${L([1.3,0],[1.3,-5],pants,1.8)}</g>
   <rect x="-3" y="-11.5" width="6" height="7" rx="2" fill="${shirt}"/><circle cx="0" cy="-14" r="2.4" fill="${skin}"/></g></g>`;
}
function hero(p,n){
  const {x,y,w,d}=p, acc=n?"#7DA3FF":"#2F64F2";
  let s=`<g class="pulse">${poly([iso(x-.6,y-.6),iso(x+w+.6,y-.6),iso(x+w+.6,y+d+.6),iso(x-.6,y+d+.6)],"none",`stroke="#E8A020" stroke-width="2.5" opacity=".9"`)}${poly([iso(x-.6,y-.6),iso(x+w+.6,y-.6),iso(x+w+.6,y+d+.6),iso(x-.6,y+d+.6)],"#E8A020",'opacity=".12"')}</g>`;
  s+=poly([iso(x-.3,y+d+.05),iso(x+w+.05,y+d+.05),iso(x+w+.05,y+d+.65),iso(x-.3,y+d+.65)],n?"#2A3854":"#F4F7FC");  // plaza
  return s;
}
function heroPeople(p,n){
  const {x,y,w,d}=p;
  return civ(iso(x+.25,y+d+.35,0),n,"#E8A020",iso(x+w-.4,y+d+.35,0),9,0)
        +civ(iso(x+w-.3,y+d+.5,0),n,n?"#9DB6F7":"#2F64F2",iso(x+.5,y+d+.5,0),11,-4)
        +civ(iso(x+w+.35,y+.4,0),n,"#5AC462",iso(x+w+.35,y+d-.4,0),8,-2);
}
function construction(p,n){
  const B=p.build, c=bcol(p.hue,n,false), H=p.h, F=Math.max(2,Math.round(H)), fh=H/F;
  const builtF=Math.max(1,Math.round(F*B.f)), hb=builtF*fh;
  const steel=n?"#5F6C86":"#A3AEC0", wood=n?"#7A5A36":"#C8975A", slab=n?"#3A4256":"#D5DAE3", slabS=n?"#2B3243":"#B9C0CC", dirt=n?"#1E2638":"#E3D7BF";
  const {x,y,w,d}=p; let s="";
  // dirt pad
  s+=poly([iso(x-.35,y-.35),iso(x+w+.35,y-.35),iso(x+w+.35,y+d+.4),iso(x-.35,y+d+.4)],dirt,'opacity=".9"');
  if(sel===p.id) s+=poly([iso(x-.4,y-.4),iso(x+w+.4,y-.4),iso(x+w+.4,y+d+.45),iso(x-.4,y+d+.45)],"none",`stroke="${pcol(p,n)}" stroke-width="2" stroke-dasharray="6 5" opacity=".9"`);
  // crane mast (behind)
  const [mx,my]=B.crane, top=H+1.7;
  const mb=box(mx-.18,my-.18,.36,.36,.18,{t:slab,l:slabS,r:slabS});
  let mast=""; for(let z=.18;z<top;z+=.35){mast+=L(iso(mx-.08,my+.08,z),iso(mx+.08,my-.08,z+.35),"#E8A11A",.9)+L(iso(mx+.08,my+.08,z),iso(mx-.08,my-.08,z+.35),"#E8A11A",.9)}
  s+=mb+L(iso(mx-.08,my+.08,.18),iso(mx-.08,my+.08,top),"#F2B02A",1.8)+L(iso(mx+.08,my-.08,.18),iso(mx+.08,my-.08,top),"#D9900F",1.8)+mast;
  // back columns
  const col=(cx,cy,z0)=>box(cx-.05,cy-.05,.1,.1,H-z0,{t:steel,l:steel,r:n?"#4A556C":"#8C98AD"},z0);
  s+=col(x+.05,y+.05,hb)+col(x+w-.05,y+.05,hb)+col(x+.05,y+d-.05,hb);
  // finished lower floors
  s+=box(x,y,w,d,hb,c);
  s+=windows({...p,h:hb,id:"_"},c,n,rnd(p.x*13+p.y*5));
  // slabs above
  for(let k=builtF;k<=F;k++){const z=k*fh; if(k===F&&B.f<.5)break; s+=box(x-.04,y-.04,w+.08,d+.08,.07,{t:slab,l:slabS,r:slabS},z-.07)}
  // rebar stubs on top
  const topZ=(B.f<.5?F-1:F)*fh;
  // front columns
  s+=col(x+w-.05,y+d-.05,hb); for(let u=1;u<Math.round(w);u++) s+=col(x+u,y+d-.05,hb); for(let u=1;u<Math.round(d);u++) s+=col(x+w-.05,y+u,hb);
  // scaffolding on the two visible faces
  const sh=Math.min(H,hb+fh*1.2), oy=y+d+.2, ox=x+w+.2;
  let sc="";
  for(let u=0;u<=w+.01;u+=w/Math.max(2,Math.round(w/.6))) sc+=L(iso(x+u,oy,0),iso(x+u,oy,sh),steel,1.1);
  for(let u=0;u<=d+.01;u+=d/Math.max(2,Math.round(d/.6))) sc+=L(iso(ox,y+u,0),iso(ox,y+u,sh),steel,1.1);
  for(let z=fh/2;z<=sh+.01;z+=fh/2){sc+=L(iso(x,oy,z),iso(x+w,oy,z),steel,1)+L(iso(ox,y,z),iso(ox,y+d,z),steel,1)}
  for(let z=fh;z<=sh+.01;z+=fh){sc+=poly([iso(x,oy-.12,z),iso(x+w,oy-.12,z),iso(x+w,oy+.12,z),iso(x,oy+.12,z)],wood)+poly([iso(ox-.12,y,z),iso(ox+.12,y,z),iso(ox+.12,y+d,z),iso(ox-.12,y+d,z)],wood)}
  // diagonal braces
  sc+=L(iso(x,oy,0),iso(x+w*.5,oy,sh*.5),steel,.8)+L(iso(ox,y+d*.5,0),iso(ox,y+d,sh*.5),steel,.8);
  s+=sc;
  // barrier fence (orange/white) along the front edges
  const fz=.22; for(let u=0;u<w+.7;u+=.35){const a=x-.3+u, col2=(Math.round(u/.35)%2)?"#FFFFFF":"#F47A1F"; s+=poly([iso(a,y+d+.42,0),iso(Math.min(a+.35,x+w+.4),y+d+.42,0),iso(Math.min(a+.35,x+w+.4),y+d+.42,fz),iso(a,y+d+.42,fz)],col2,'opacity=".95"')}
  for(let u=0;u<d+.75;u+=.35){const a=y-.3+u, col2=(Math.round(u/.35)%2)?"#FFFFFF":"#F47A1F"; s+=poly([iso(x+w+.42,a,0),iso(x+w+.42,Math.min(a+.35,y+d+.42),0),iso(x+w+.42,Math.min(a+.35,y+d+.42),fz),iso(x+w+.42,a,fz)],n?"#C9681C":col2,'opacity=".9"')}
  // cone
  const cn=iso(x+w+.6,y+d+.6,0); s+=`<path d="M${cn[0]-4} ${cn[1]} L${cn[0]} ${cn[1]-11} L${cn[0]+4} ${cn[1]}z" fill="#F47A1F"/><rect x="${cn[0]-2.4}" y="${cn[1]-6}" width="4.8" height="1.6" fill="#fff"/>`;
  // workers
  s+=worker(iso(x+.35,y+d*.55,hb),n,"walk",iso(x+w-.35,y+d*.55,hb),4.5);           // on the finished roof slab
  s+=worker(iso(x+w*.3,oy,fh),n,"hammer");                                            // on scaffold, front face
  // welder with sparks on the top slab
  
  // night work light
  if(n){const lp=iso(x+w*.5,oy,sh); s+=`<circle cx="${lp[0]}" cy="${lp[1]}" r="22" fill="#FFD27A" opacity=".12"/><circle cx="${lp[0]}" cy="${lp[1]}" r="2.6" fill="#FFE7A8"/>`}
  // crane jib, counter-jib, trolley, cable and load (in front)
  const tx=x+w*.55, ty=y+d*.5, dx=tx-mx, dy=ty-my, len=Math.hypot(dx,dy), ux=dx/len, uy=dy/len;
  const jt=iso(mx,my,top), je=iso(mx+ux*(len+.6),my+uy*(len+.6),top), cj=iso(mx-ux*1.1,my-uy*1.1,top);
  s+=L(jt,je,"#F2B02A",2.2)+L(iso(mx,my,top+.25),je,"#E8A11A",.8)+L(iso(mx,my,top+.25),cj,"#E8A11A",.8)+L(jt,cj,"#F2B02A",2.2);
  s+=box(mx-ux*1.1-.15,my-uy*1.1-.15,.3,.3,.3,{t:slab,l:slabS,r:"#7D8597"},top-.3);
  s+=box(mx-.14,my-.14,.28,.28,.28,{t:"#FFD36A",l:"#E8A11A",r:"#C98710"},top-.05); // cab
  s+=`<circle class="blink" cx="${iso(mx,my,top+.3)[0]}" cy="${iso(mx,my,top+.3)[1]}" r="2.2" fill="#FF4D4D"/>`;
  const tp=iso(tx,ty,top), lz=Math.max(topZ+.9,H+.2), lp=iso(tx,ty,lz), Lc=tp[1]-lp[1]<0?lp[1]-tp[1]:lp[1]-tp[1];
  const drop=Math.min(22,Lc*.5);
  s+=`<rect x="${tp[0]-3}" y="${tp[1]-1.5}" width="6" height="3" fill="#4A4F5A"/>`;
  s+=`<line class="cable" x1="${tp[0]}" y1="${tp[1]}" x2="${tp[0]}" y2="${lp[1]}" stroke="${n?"#AAB4C8":"#3A4152"}" stroke-width=".9" style="--cs:${((Lc+drop)/Lc).toFixed(3)}"/>`;
  s+=`<g class="load" style="--ly:${drop.toFixed(1)}px">${box(tx-.45,ty-.07,.9,.14,.12,{t:"#E25B3A",l:"#B8432A",r:"#9C3722"},lz-.12)}</g>`;
  return s;
}
function building(p,n){
  const c=bcol(p.hue,n,p.hq), r=rnd(p.x*31+p.y*7+3);
  let s=`<g class="bld" data-id="${p.id}">`;
  if(p.build) return s+construction(p,n)+"</g>";
  // shadow
  s+=poly([iso(p.x+.15,p.y+p.d,0),iso(p.x+p.w,p.y+p.d,0),iso(p.x+p.w+.6,p.y+p.d+.3,0),iso(p.x+.75,p.y+p.d+.3,0)],pal(n).shadow);
  if(sel===p.id){s+=poly([iso(p.x-.25,p.y-.25),iso(p.x+p.w+.25,p.y-.25),iso(p.x+p.w+.25,p.y+p.d+.25),iso(p.x-.25,p.y+p.d+.25)],"none",`stroke="${pcol(p,n)}" stroke-width="2" stroke-dasharray="6 5" opacity=".9"`);}
  if(p.id==="betalmighty") s+=hero(p,n);
  s+=box(p.x,p.y,p.w,p.d,p.h,c);
  s+=windows(p,c,n,r)+docks(p,n);
  // parapet + roof unit
  s+=box(p.x+.12,p.y+.12,p.w-.24,p.d-.24,.06,{t:c.roof,l:c.l,r:c.r},p.h);
  if(!p.hq) s+=box(p.x+p.w*.55,p.y+p.d*.2,Math.min(.6,p.w*.3),Math.min(.5,p.d*.3),.35,{t:c.roof,l:c.r,r:c.r},p.h+.06);
  else{ // HQ flag
    const b=iso(p.x+p.w*.5,p.y+p.d*.5,p.h);s+=`<line x1="${b[0]}" y1="${b[1]}" x2="${b[0]}" y2="${b[1]-34}" stroke="${n?"#97A5BF":"#5C6A84"}" stroke-width="2"/><polygon points="${b[0]},${b[1]-34} ${b[0]+18},${b[1]-28} ${b[0]},${b[1]-22}" fill="${n?"#7DA3FF":"#2F64F2"}"/>`;}
  if(p.id==="betalmighty") s+=heroPeople(p,n);
  s+="</g>";return s;
}
const PIN_AT={};
// project colour: BetAlmighty's gold, the HQ's blueprint blue, otherwise the building's own hue
const pcol=(p,n)=>p.id==="betalmighty"?"#E8A020":p.hq?(n?"#7DA3FF":"#2F5BEA"):`hsl(${p.hue} 58% ${n?62:46}%)`;
function pin(p,n){
  const t=iso(p.x+p.w/2,p.y+p.d/2,p.h+(p.hq?1.5:p.build?1.0:.6));const on=sel===p.id;
  const lift=(on?50:40)+(p.pinUp||0), c=pcol(p,n);
  PIN_AT[p.id]=[t[0],t[1]-lift];
  return `<g class="bld pin" data-id="${p.id}" style="pointer-events:all">
   <line x1="${t[0]}" y1="${t[1]}" x2="${t[0]}" y2="${t[1]-lift}" stroke="${c}" stroke-width="1.5" opacity="${on?1:.7}"/>
   <circle cx="${t[0]}" cy="${t[1]}" r="3" fill="${c}"/>
  </g>`;
}
function tree(x,y,P_){const b=iso(x,y,0),t=iso(x,y,.9);
  return `<ellipse cx="${b[0]+5}" cy="${b[1]+2}" rx="10" ry="4" fill="${P_.shadow}"/><rect x="${b[0]-1.5}" y="${t[1]+4}" width="3" height="${b[1]-t[1]-3}" fill="${P_.trunk}"/><circle cx="${t[0]}" cy="${t[1]}" r="10" fill="${P_.tree2}"/><circle cx="${t[0]-2.5}" cy="${t[1]-2.5}" r="7.5" fill="${P_.tree}"/>`}
function crate(x,y,P_){return box(x,y,.38,.38,.32,{t:P_.crate3,l:P_.crate,r:P_.crate2})}
function lamp(x,y,P_,n){const b=iso(x,y,0),t=iso(x,y,1.1);
  return `<line x1="${b[0]}" y1="${b[1]}" x2="${t[0]}" y2="${t[1]}" stroke="${n?"#3A4864":"#A8B4C8"}" stroke-width="1.6"/>${n?`<circle cx="${t[0]}" cy="${t[1]}" r="11" fill="#FFD27A" opacity=".16"/>`:""}<circle cx="${t[0]}" cy="${t[1]}" r="2.6" fill="${P_.lamp}"/>`}

const TREES=[[4.7,1.7],[5.4,2.7],[7.6,10.3],[9.4,10.4],[5.5,4.7],[4.5,8.5],[5.4,9.4],[4.3,9.8],[10.5,8.5],[11.5,9.2],[10.4,10.1],[11.6,10.6],[4.4,4.4],[5.3,3.9],[0.6,4.7],[2.6,4.8],[11.4,4.6],[0.7,11.4],[2.4,11.6],[5.2,11.2],[3.3,10.6],[8.2,11.6],[12.4,12.2],[9.6,11.8],[12.4,6.2+1.5]];
const CRATES=[[5.1,1.2],[5.3,8.2],[10.9,9.6],[11.3,9.9],[4.3,3.4],[4.8,3.5],[4.5,3.9],[0.6,7.6],[0.9,10.6],[6.2+1.4,10.6],[10.6,11.5],[11.1,11.6],[7.5,5.25-.3],[12.3,4.3]];
const LAMPS=[[1.5,5.9],[4.5,5.9],[9.5,5.9],[12,5.9],[5.9,1.5],[5.9,9.5],[5.9,12]];

let staticSVG="";
function cityMarkup(n){
  const P_=pal(n);
  let s=`<defs></defs>`;
  // plate
  s+=poly([iso(0,N,0),iso(N,N,0),iso(N,N,-.7),iso(0,N,-.7)],P_.side1);
  s+=poly([iso(N,0,0),iso(N,N,0),iso(N,N,-.7),iso(N,0,-.7)],P_.side2);
  s+=poly([iso(0,0),iso(N,0),iso(N,N),iso(0,N)],P_.ground);
  for(let i=1;i<N;i++){const a=iso(i,0),b=iso(i,N),c=iso(0,i),d=iso(N,i);s+=`<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="${P_.grid}"/><line x1="${c[0]}" y1="${c[1]}" x2="${d[0]}" y2="${d[1]}" stroke="${P_.grid}"/>`}
  // roads
  s+=poly([iso(0,6),iso(N,6),iso(N,7),iso(0,7)],P_.road)+poly([iso(6,0),iso(7,0),iso(7,N),iso(6,N)],P_.road);
  const l1=iso(0,6.5),l2=iso(N,6.5),l3=iso(6.5,0),l4=iso(6.5,N);
  s+=`<line x1="${l1[0]}" y1="${l1[1]}" x2="${l2[0]}" y2="${l2[1]}" stroke="${P_.line}" stroke-width="1.6" stroke-dasharray="10 9"/><line x1="${l3[0]}" y1="${l3[1]}" x2="${l4[0]}" y2="${l4[1]}" stroke="${P_.line}" stroke-width="1.6" stroke-dasharray="10 9"/>`;
  s+=poly([iso(6,6),iso(7,6),iso(7,7),iso(6,7)],P_.road);
  // objects sorted back-to-front
  const objs=[];
  P.forEach(p=>objs.push({k:p.x+p.w+p.y+p.d-.01,svg:building(p,n)}));
  TREES.forEach(([x,y])=>objs.push({k:x+y+.4,svg:tree(x,y,P_)}));
  CRATES.forEach(([x,y])=>objs.push({k:x+y+.76,svg:crate(x,y,P_)}));
  LAMPS.forEach(([x,y])=>objs.push({k:x+y,svg:lamp(x,y,P_,n)}));
  objs.sort((a,b)=>a.k-b.k).forEach(o=>s+=o.svg);
  P.forEach(p=>s+=pin(p,n));
  return s;
}
function render(){svg.innerHTML=cityMarkup(dark());setVB();renderHero()}
const RM=matchMedia("(prefers-reduced-motion: reduce)");

function setVB(){svg.setAttribute("viewBox",`${vb.x} ${vb.y} ${vb.w} ${vb.h}`);placeLabels()}

// map labels are HTML so they stay readable at any zoom or screen size
const labelsEl=document.getElementById("plabels");
function buildLabels(){
  labelsEl.innerHTML=P.map(p=>`<button type="button" class="plabel" data-id="${p.id}" aria-pressed="false"><i></i><b>${esc(p.hq?"About me":(p.short||p.name))}</b><small>${esc(p.hq?"Contact":(p.build?"In progress":"Case study"))}</small></button>`).join("");
  labelsEl.querySelectorAll(".plabel").forEach(b=>b.onclick=()=>select(b.dataset.id));
}
function placeLabels(){placeLabelsIn(svg,labelsEl,dark(),true)}
function placeLabelsIn(svg,labelsEl,n,selectable){
  if(!labelsEl.firstChild)return;
  const m=svg.getScreenCTM(), box=labelsEl.getBoundingClientRect();
  if(!m)return;
  const pt=svg.createSVGPoint();
  const items=[];
  labelsEl.querySelectorAll(".plabel").forEach(el=>{
    const id=el.dataset.id, p=byId[id], a=PIN_AT[id];if(!a)return;
    if(selectable){const on=id===sel;el.classList.toggle("on",on);el.setAttribute("aria-pressed",on)}
    el.style.setProperty("--pc",pcol(p,n));
    pt.x=a[0];pt.y=a[1];const q=pt.matrixTransform(m);
    items.push({el,x:q.x-box.left,y:q.y-box.top,w:el.offsetWidth,h:el.offsetHeight});
  });
  // keep labels from overlapping: place bottom-up, nudging later ones upward
  items.sort((a,b)=>b.y-a.y);
  const placed=[];
  for(const it of items){
    for(let guard=0;guard<6;guard++){
      const hit=placed.find(o=>Math.abs(o.x-it.x)<(o.w+it.w)/2+4&&it.y>o.y-o.h-4&&it.y-it.h<o.y+4);
      if(!hit)break;it.y=hit.y-hit.h-6;
    }
    it.x=Math.min(Math.max(it.x,it.w/2+6),box.width-it.w/2-6);
    placed.push(it);
    it.el.style.transform=`translate(${it.x.toFixed(1)}px,${it.y.toFixed(1)}px) translate(-50%,-100%)`;
    it.el.hidden=it.x<-40||it.y-it.h<-8||it.x>box.width+40||it.y>box.height+40;
  }
}
new ResizeObserver(()=>placeLabels()).observe(svg);
function zoom(f){const cx=vb.x+vb.w/2,cy=vb.y+vb.h/2;const w=Math.min(1400,Math.max(320,vb.w*f));const h=w*HOME.h/HOME.w;vb={x:cx-w/2,y:cy-h/2,w,h};setVB()}
document.getElementById("zin").onclick=()=>zoom(.8);
document.getElementById("zout").onclick=()=>zoom(1.25);
document.getElementById("zre").onclick=()=>{vb={...HOME};setVB()};

// full-screen city: native full screen where the browser allows it, a fixed overlay everywhere
const plan=document.querySelector(".plan"), fb=document.getElementById("zfull");
let opener=null;
function setFull(on){
  if(plan.classList.contains("full")===on)return;
  if(on)opener=document.activeElement;
  plan.classList.toggle("full",on);fb.setAttribute("aria-pressed",on);
  if(on&&plan.requestFullscreen)plan.requestFullscreen().catch(()=>{});
  if(!on&&document.fullscreenElement)document.exitFullscreen().catch(()=>{});
  vb={...HOME};
  // portrait screens: start closer in so the city fills the tall frame
  const r=svg.getBoundingClientRect();if(on&&r.height>r.width){const w=HOME.w*.72,h=w*HOME.h/HOME.w;vb={x:HOME.x+(HOME.w-w)/2,y:HOME.y+(HOME.h-h)/2,w,h}}
  setVB();
  if(on)document.getElementById("xclose").focus({preventScroll:true});
  else if(opener&&opener.focus){const o=opener;opener=null;o.focus({preventScroll:true});
    // leaving native full screen resets focus when it finishes, so restore it again then
    if(document.fullscreenElement)document.addEventListener("fullscreenchange",()=>requestAnimationFrame(()=>o.focus({preventScroll:true})),{once:true})}
}
document.getElementById("xclose").onclick=()=>setFull(false);
fb.onclick=()=>setFull(false);
document.addEventListener("fullscreenchange",()=>{if(!document.fullscreenElement)setFull(false)});
addEventListener("keydown",e=>{if(e.key==="Escape"&&plan.classList.contains("full"))setFull(false)});
// wheel and pinch zoom while full screen, centred on the pointer
document.getElementById("map").addEventListener("wheel",e=>{if(!plan.classList.contains("full"))return;e.preventDefault();
  const r=svg.getBoundingClientRect(),k=Math.max(vb.w/r.width,vb.h/r.height);
  const px=vb.x+(e.clientX-r.left-(r.width-vb.w/k)/2)*k, py=vb.y+(e.clientY-r.top-(r.height-vb.h/k)/2)*k;
  const f=Math.exp(e.deltaY*.0015), w=Math.min(1400,Math.max(320,vb.w*f)), h=w*HOME.h/HOME.w, s2=w/vb.w;
  vb={x:px-(px-vb.x)*s2,y:py-(py-vb.y)*s2,w,h};setVB()},{passive:false});
const touches=new Map();let pinch=null;
svg.addEventListener("pointerdown",e=>{if(e.pointerType!=="touch")return;touches.set(e.pointerId,e);if(touches.size===2){const [a,b]=[...touches.values()];pinch={d:Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY),vb:{...vb}};down=null}});
svg.addEventListener("pointermove",e=>{if(!touches.has(e.pointerId))return;touches.set(e.pointerId,e);if(pinch&&touches.size===2){const [a,b]=[...touches.values()];const d=Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY);
  const cx=pinch.vb.x+pinch.vb.w/2,cy=pinch.vb.y+pinch.vb.h/2,w=Math.min(1400,Math.max(320,pinch.vb.w*pinch.d/d)),h=w*HOME.h/HOME.w;vb={x:cx-w/2,y:cy-h/2,w,h};setVB()}});
const lift=e=>{touches.delete(e.pointerId);if(touches.size<2)pinch=null};
svg.addEventListener("pointerup",lift);svg.addEventListener("pointercancel",lift);

// pan + click
let down=null;
svg.addEventListener("pointerdown",e=>{down={x:e.clientX,y:e.clientY,vb:{...vb},t:e.target.closest("[data-id]"),moved:false,id:e.pointerId}});
svg.addEventListener("pointermove",e=>{if(!down)return;const dx=e.clientX-down.x,dy=e.clientY-down.y;
  if(!down.moved&&Math.hypot(dx,dy)>5){down.moved=true;svg.classList.add("drag");try{svg.setPointerCapture(down.id)}catch(_){}}
  if(down.moved){const r=svg.getBoundingClientRect();const k=Math.max(vb.w/r.width,vb.h/r.height);vb.x=down.vb.x-dx*k;vb.y=down.vb.y-dy*k;setVB()}});
const end=()=>{if(down&&!down.moved&&down.t)select(down.t.dataset.id);down=null;svg.classList.remove("drag")};
svg.addEventListener("pointerup",end);svg.addEventListener("pointercancel",()=>{down=null;svg.classList.remove("drag")});
svg.addEventListener("keydown",e=>{const g=e.target.closest&&e.target.closest("[data-id]");if(g&&(e.key==="Enter"||e.key===" ")){e.preventDefault();select(g.dataset.id)}});

const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

function panel(){
  const p=byId[sel], el=document.getElementById("panel");
  if(p.hq){
    el.innerHTML=`<div class="ph"><div><span class="eyebrow">HQ · About</span><h2>Chukwuebuka Ogoke</h2></div></div>
    <p class="sum">Product designer for AI-powered products and complex workflows. I turn complicated rules into clear flows, systems and screens, and I stay close to the people who use them.</p>
    <div class="stats"><div><span>Focus</span><b class="rl">Complex workflows · AI-powered products</b></div><div><span>Ventures</span><b>Multi-venture</b></div></div>
    <h3>Skills inventory <span>6 in stock</span></h3>
    <ul class="inv">${[["Product strategy","Research"],["UX flows and state mapping","UX"],["Design systems in Figma","Systems"],["PRDs and design scopes","Docs"],["Brand and visual identity","Visual"],["User research and retention","Research"]].map(inv).join("")}</ul>
    <div class="links"><button class="cta" type="button" data-mail aria-haspopup="menu" aria-expanded="false">Email me</button><a class="cta alt" href="#about">About me</a></div>`;
  } else {
    el.innerHTML=`<div class="ph"><div><span class="eyebrow">${p.code} · ${esc(p.sector)}</span><h2>${esc(p.name)}</h2></div><span class="pill ${p.tone}">${p.status}</span></div>
    <p class="sum">${esc(p.summary)}</p>
    <div class="stats"><div><span>${p.metric[0]}</span><b>${esc(p.metric[1])}</b></div><div><span>My role</span><b class="rl">${esc(p.title)}</b></div></div>
    <h3>Deliverables <span>${p.items.length} items</span></h3>
    <ul class="inv">${p.items.map(inv).join("")}</ul>
    <div class="role">Role · <b>${esc(p.role)}</b></div>
    ${p.page?`<a class="cta" href="${p.page}">Read the case study <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>`:`<div class="soon">Case study in progress</div>`}`;
  }
}
function inv([name,type]){const t=TYPE[type];return `<li><span class="sq" style="background:${t[1]};color:${t[2]}">${t[0]}</span><span class="nm">${esc(name)}</span><span class="tag">${type}</span></li>`}
function thumbMarkup(p,n){
  const P_=pal(n),keep=sel;sel=null;
  const a=[p.x-.7,p.y-.7],b=[p.x+p.w+.7,p.y+p.d+.7];
  let s=poly([iso(a[0],b[1],0),iso(b[0],b[1],0),iso(b[0],b[1],-.35),iso(a[0],b[1],-.35)],P_.side1)
       +poly([iso(b[0],a[1],0),iso(b[0],b[1],0),iso(b[0],b[1],-.35),iso(b[0],a[1],-.35)],P_.side2)
       +poly([iso(a[0],a[1]),iso(b[0],a[1]),iso(b[0],b[1]),iso(a[0],b[1])],P_.ground)
       +building(p,n);
  sel=keep;return s;
}
function select(id){if(!byId[id])return;sel=id;render();panel()}

// case study links: remember where the click came from so the case study page can grow out of it
function rememberOrigin(r){try{sessionStorage.setItem("ow-from",JSON.stringify({t:r.top,l:r.left,r:r.right,b:r.bottom,w:innerWidth,h:innerHeight,bg:getComputedStyle(document.body).backgroundColor}))}catch(_){}}
document.addEventListener("click",e=>{const a=e.target.closest('a[href="/betalmighty"],a[href="/activation-rescue"],a[href="/myestate"],a[href="/soundyaad"]');if(a&&!e.metaKey&&!e.ctrlKey&&!e.shiftKey&&!e.button)rememberOrigin(a.getBoundingClientRect())});

// theme
const tb=document.getElementById("theme");
function themeLabel(){const n=dark();tb.innerHTML=n?`<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>Day`:`<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>Night`}
try{const saved=localStorage.getItem("ow-theme");if(saved)document.documentElement.setAttribute("data-theme",saved)}catch(_){}
tb.onclick=()=>{const next=dark()?"light":"dark";document.documentElement.setAttribute("data-theme",next);try{localStorage.setItem("ow-theme",next)}catch(_){}};
new MutationObserver(()=>{themeLabel();render()}).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]});
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>{themeLabel();render()});



// email menu: mailto alone fails for anyone without a mail app set up
const mp=document.getElementById("mailpop");let mpFrom=null;
function closeMail(){if(mp.hidden)return;mp.hidden=true;if(mpFrom){mpFrom.setAttribute("aria-expanded","false");mpFrom.focus({preventScroll:true})}mpFrom=null}
function placeMail(){const r=mpFrom.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight){closeMail();return}
  const w=mp.offsetWidth,h=mp.offsetHeight;let x=Math.min(Math.max(8,r.right-w),innerWidth-w-8),y=r.bottom+8;if(y+h>innerHeight-8)y=Math.max(8,r.top-h-8);
  mp.style.left=x+"px";mp.style.top=y+"px"}
function openMail(btn){mpFrom=btn;btn.setAttribute("aria-expanded","true");mp.hidden=false;placeMail();mp.querySelector("a,button").focus({preventScroll:true})}
document.addEventListener("click",e=>{const t=e.target.closest("[data-mail]");if(t){e.preventDefault();if(!mp.hidden&&mpFrom===t)closeMail();else{closeMail();openMail(t)}return}if(!mp.hidden&&!e.target.closest("#mailpop"))closeMail()});
mp.addEventListener("click",e=>{if(e.target.closest("a"))setTimeout(closeMail,0)});
addEventListener("keydown",e=>{if(e.key==="Escape")closeMail()});
// follow the button while the page scrolls; close once it leaves the screen
addEventListener("scroll",()=>{if(!mp.hidden)placeMail()},{passive:true,capture:true});addEventListener("resize",()=>{if(!mp.hidden)placeMail()});
document.getElementById("mailCopy").onclick=async()=>{const sm=document.querySelector("#mailCopy small");try{await navigator.clipboard.writeText("Harryebuka7@gmail.com");sm.textContent="Copied to clipboard"}catch(_){sm.textContent="Harryebuka7@gmail.com (select and copy)"}setTimeout(()=>{sm.textContent="Harryebuka7@gmail.com";closeMail()},1100)};

// glide the map to a building
function focusOn(id){if(!byId[id])return;select(id);const p=byId[id];const c=iso(p.x+p.w/2,p.y+p.d/2,p.h/2);
  const R=svg.getBoundingClientRect(),C=document.getElementById("panel").getBoundingClientRect(),w=HOME.w*(R.width>1100?1.15:.85),h=w*HOME.h/HOME.w;
  const k=Math.max(w/R.width,h/R.height);let dx=0,dy=0;
  if(C.width&&C.height){if(R.width>760)dx=(C.right-R.left)/2;else dy=-(R.bottom-C.top)/2}
  const target={x:c[0]-w/2-dx*k,y:c[1]-h/2-dy*k,w,h};
  if(RM.matches){vb=target;setVB();return}
  const from={...vb},t0=performance.now();
  (function step(now){const k=Math.min(1,(now-t0)/600),e=1-Math.pow(1-k,3);vb={x:from.x+(target.x-from.x)*e,y:from.y+(target.y-from.y)*e,w:from.w+(target.w-from.w)*e,h:from.h+(target.h-from.h)*e};setVB();if(k<1)requestAnimationFrame(step)})(t0)}

// ---------- hero: the city, in the site's light or dark theme ----------
const heroSvg=document.getElementById("heroScene"), heroLabels=document.getElementById("heroLabels"), hcity=document.getElementById("hcity");
function renderHero(){
  const n=dark();
  hcity.dataset.sky=n?"night":"day";
  heroSvg.innerHTML=cityMarkup(n);
  placeLabelsIn(heroSvg,heroLabels,n,false);
}
heroLabels.innerHTML=P.map(p=>`<button type="button" class="plabel" data-id="${p.id}" aria-label="${p.page?`Open the ${esc(p.name)} case study`:`Explore ${esc(p.hq?"About me":p.name)} in the city`}"><i></i><b>${esc(p.hq?"About me":(p.short||p.name))}</b>${p.page?"<small>Case study ↗</small>":""}</button>`).join("");
function openExplorer(id){setFull(true);if(id)focusOn(id)}
function heroGo(id){
  const p=byId[id];if(!p||!p.page){openExplorer(id);return}
  const g=heroSvg.querySelector(`g.bld:not(.pin)[data-id="${id}"]`);if(g)rememberOrigin(g.getBoundingClientRect());location.href=p.page;
}
heroLabels.addEventListener("click",e=>{const b=e.target.closest("[data-id]");if(b)heroGo(b.dataset.id)});
heroSvg.addEventListener("click",e=>{const g=e.target.closest("[data-id]");if(g)heroGo(g.dataset.id);else openExplorer()});
document.querySelectorAll("[data-explore]").forEach(b=>b.onclick=()=>openExplorer());
new ResizeObserver(()=>placeLabelsIn(heroSvg,heroLabels,dark(),false)).observe(heroSvg);

buildLabels();themeLabel();select(sel);
})();

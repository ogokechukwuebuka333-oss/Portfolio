(()=>{
// ?draft shows the notes marking what still needs input; visitors never see them
if(new URLSearchParams(location.search).has("draft"))document.documentElement.classList.add("draft");
const RM=matchMedia("(prefers-reduced-motion: reduce)");
const sheet=document.getElementById("case");

// arriving from the homepage: grow out of the building or link that was clicked
(()=>{let o=null;try{o=JSON.parse(sessionStorage.getItem("ow-from"));sessionStorage.removeItem("ow-from")}catch(_){}
  if(!o||RM.matches||!sheet.animate||Math.abs(o.w-innerWidth)>2)return;
  const rr=Math.max(0,innerWidth-o.r),b=Math.max(0,innerHeight-o.b),bg=document.body.style.background;
  document.body.style.background=o.bg;
  const a=sheet.animate([{clipPath:`inset(${Math.max(0,o.t)}px ${rr}px ${b}px ${Math.max(0,o.l)}px round 28px)`},{clipPath:"inset(0px 0px 0px 0px round 0px)"}],{duration:620,easing:"cubic-bezier(.2,.8,.2,1)"});
  document.getElementById("csBody").animate([{opacity:.35,transform:"translateY(18px)"},{opacity:1,transform:"none"}],{duration:620,easing:"cubic-bezier(.2,.8,.2,1)"});
  a.onfinish=a.oncancel=()=>{document.body.style.background=bg};
})();

// back to the homepage: return to where you were if you came from it
function backHome(e){
  let ref=null;try{ref=new URL(document.referrer)}catch(_){}
  if(ref&&ref.origin===location.origin&&ref.pathname==="/"&&history.length>1){if(e)e.preventDefault();history.back()}
  else if(!e)location.href="/";
}
document.querySelectorAll("[data-home]").forEach(a=>a.addEventListener("click",backHome));

// image viewer
const lb=document.getElementById("lb"),lbImg=document.getElementById("lbImg"),lbCap=document.getElementById("lbCap");
document.getElementById("csBody").addEventListener("click",e=>{const t=e.target.closest("[data-full]");if(!t)return;lb.classList.toggle("wide",!!t.closest(".board")||t.hasAttribute("data-wide"));lbImg.src=t.dataset.full;lbImg.alt=t.dataset.cap||"";lbCap.textContent=t.dataset.cap||"";lb.hidden=false;lb.scrollLeft=0});
lb.addEventListener("click",()=>{lb.hidden=true});
addEventListener("keydown",e=>{if(e.key!=="Escape")return;if(!lb.hidden)lb.hidden=true;else backHome()});

// contents bar
document.getElementById("csToc").addEventListener("click",e=>{const a=e.target.closest("a");if(!a)return;e.preventDefault();const el=document.querySelector(a.getAttribute("href"));if(el)el.scrollIntoView({behavior:RM.matches?"instant":"smooth",block:"start"})});
(()=>{const links=[...document.querySelectorAll("#csToc a")];const io=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){links.forEach(l=>l.classList.toggle("on",l.getAttribute("href")==="#"+en.target.id));const on=links.find(l=>l.classList.contains("on"));if(on){const t=on.parentElement,r=on.getBoundingClientRect(),tr=t.getBoundingClientRect();t.scrollTo({left:t.scrollLeft+r.left-tr.left-(t.clientWidth-r.width)/2})}}})},{rootMargin:"-30% 0px -60% 0px"});document.querySelectorAll("#csBody section[id]").forEach(x=>io.observe(x))})();

// escrow state explorer (tabs: click, or arrow keys to move)
document.querySelectorAll(".cs .esx").forEach(root=>{
  const S=JSON.parse(root.dataset.states), tabs=[...root.querySelectorAll('[role="tab"]')], imgs=[...root.querySelectorAll(".esx-phone img")];
  const k=root.querySelector(".esx-k"), h=root.querySelector(".esx-text h3"), p=root.querySelector(".esx-text p"), panel=root.querySelector('[role="tabpanel"]');
  function pick(i,focus){tabs.forEach((t,j)=>{t.setAttribute("aria-selected",j===i);t.tabIndex=j===i?0:-1});tabs[i].scrollIntoView({block:"nearest",inline:"nearest",behavior:RM.matches?"instant":"smooth"});imgs.forEach((im,j)=>{im.classList.toggle("on",j===i);if(j===i)im.loading="eager"});
    k.className="esx-k "+S[i].c;k.textContent=`State ${i+1} of ${S.length} · ${S[i].l}`;h.textContent=S[i].n;p.textContent=S[i].d;panel.setAttribute("aria-labelledby",tabs[i].id);if(focus)tabs[i].focus()}
  tabs.forEach((t,i)=>{t.onclick=()=>pick(i);t.onkeydown=e=>{const d={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1}[e.key];if(e.key==="Home"||e.key==="End"){e.preventDefault();pick(e.key==="Home"?0:tabs.length-1,true)}else if(d){e.preventDefault();pick((i+d+tabs.length)%tabs.length,true)}}});
});

// videos: swap the thumbnail for the YouTube player only when asked, so nothing loads from YouTube until then
document.querySelectorAll(".cs .yt-play").forEach(b=>b.addEventListener("click",()=>{
  const f=document.createElement("iframe");
  f.src=`https://www.youtube-nocookie.com/embed/${b.dataset.yt}?autoplay=1&rel=0&playsinline=1`;
  f.title=b.dataset.title;f.allow="autoplay; encrypted-media; picture-in-picture; fullscreen";f.allowFullscreen=true;f.referrerPolicy="strict-origin-when-cross-origin";
  b.replaceWith(f);f.focus();
}));

// before / after slider
document.querySelectorAll(".cs .slider").forEach(el=>{const r=el.querySelector("input");r.addEventListener("input",()=>el.style.setProperty("--pos",r.value+"%"))});


})();

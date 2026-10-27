// Subtle scroll reveals: content fades and rises a little as it comes into view.
// Nothing is hidden unless this script runs, and reduced motion turns it off.
(()=>{
if(matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver" in window))return;
const ONE=[".block .bh",".proj .pj-text",".proj .pj-art",".aiex",".skills",".cta-end .contact",
  ".cs .summary",".cs section>*:not(.cards):not(.finds):not(.phones):not(.webs):not(.ratios):not(.steps):not(.stats):not(.todo)"];
const GROUPS=[".pipe>li",".facts>li",".cs .cards>*",".cs .finds>li",".cs .phones>*",".cs .webs>*",".cs .ratios>*",".cs .steps>li",".cs .stats>*"];
const els=new Set(document.querySelectorAll(ONE.join(",")));
document.querySelectorAll(GROUPS.join(",")).forEach(e=>{els.add(e);e.style.setProperty("--i",Math.min([...e.parentElement.children].indexOf(e),6))});
if(!els.size)return;
document.documentElement.classList.add("rv");
const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target)}}),{rootMargin:"0px 0px -6% 0px",threshold:.06});
els.forEach(e=>{e.setAttribute("data-rv",e.matches(".proj .pj-art")?"zoom":"");io.observe(e)});
})();

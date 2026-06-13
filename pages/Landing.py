import streamlit as st

st.html("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main, .block-container {
    background: #F0EEFF !important;
    color: #2D2250 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stToolbar"]  { display: none !important; }
header { visibility: hidden !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Keyframes (all original preserved) ── */
@keyframes fadeUp { from { opacity:0; transform:translateY(28px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes slideInRight { from { opacity:0; transform:translateX(40px); } to { opacity:1; transform:translateX(0); } }
@keyframes pulse { 0%,100% { box-shadow:0 0 0 0 rgba(139,92,246,0.35); } 50% { box-shadow:0 0 0 10px rgba(139,92,246,0); } }
@keyframes barGrow { from { width:0%; } }
@keyframes float { 0%,100% { transform:translateY(0px); } 50% { transform:translateY(-8px); } }
@keyframes dotPulse { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:0.5; transform:scale(0.85); } }
@keyframes marqueeScroll { from { transform:translateX(100%); } to { transform:translateX(-100%); } }

/* ── CV floating elements animations ── */
@keyframes floatDoc {
    0%,100% { transform:translateY(0px) rotate(-4deg); opacity:0.18; }
    50%      { transform:translateY(-18px) rotate(-4deg); opacity:0.28; }
}
@keyframes floatStar {
    0%,100% { transform:translateY(0px) rotate(12deg) scale(1); opacity:0.15; }
    50%      { transform:translateY(-14px) rotate(20deg) scale(1.1); opacity:0.25; }
}
@keyframes floatCheck {
    0%,100% { transform:translateY(0px) rotate(8deg); opacity:0.13; }
    60%      { transform:translateY(-20px) rotate(14deg); opacity:0.22; }
}
@keyframes floatChart {
    0%,100% { transform:translateY(0px) rotate(-8deg); opacity:0.12; }
    40%      { transform:translateY(-16px) rotate(-12deg); opacity:0.2; }
}
@keyframes floatPencil {
    0%,100% { transform:translateY(0px) rotate(20deg); opacity:0.14; }
    55%      { transform:translateY(-22px) rotate(26deg); opacity:0.24; }
}

/* ── Floating CV decorations — lane containers clip content physically ── */
.cv-deco-left-lane {
    position:fixed; top:0; left:0;
    width:52px; height:100vh;
    pointer-events:none; z-index:0; overflow:hidden;
}
.cv-deco-right-lane {
    position:fixed; top:0; right:0;
    width:52px; height:100vh;
    pointer-events:none; z-index:0; overflow:hidden;
}
.cv-deco { position:absolute; font-size:2rem; user-select:none; opacity:0.22; left:6px; }
.cv-deco-1 { top:10vh; animation:floatDoc    6s   ease-in-out infinite; }
.cv-deco-3 { top:36vh; animation:floatCheck  5.5s ease-in-out infinite 0.5s; }
.cv-deco-5 { top:60vh; animation:floatPencil 6.5s ease-in-out infinite 1.5s; }
.cv-deco-7 { top:80vh; animation:floatDoc    7s   ease-in-out infinite 1s; }
.cv-deco-2 { top:14vh; animation:floatStar   7s   ease-in-out infinite 1s; }
.cv-deco-4 { top:42vh; animation:floatChart  8s   ease-in-out infinite 2s; }
.cv-deco-6 { top:68vh; animation:floatDoc    7.5s ease-in-out infinite 0.8s; }

/* ── Ticker ── */
.ticker { background:rgba(139,92,246,0.08); border-bottom:1px solid rgba(139,92,246,0.18); padding:8px 0; overflow:hidden; }
.ticker-inner { display:inline-block; white-space:nowrap; animation:marqueeScroll 28s linear infinite; color:#7C3AED; font-size:0.82rem; font-weight:500; }

/* ── Navbar ── */
.nav { display:flex; align-items:center; justify-content:space-between; padding:18px 60px; background:rgba(240,238,255,0.92); backdrop-filter:blur(14px); border-bottom:1px solid rgba(139,92,246,0.14); position:sticky; top:0; z-index:100; animation:fadeIn 0.5s ease; }
.nav-brand { display:flex; align-items:center; gap:10px; font-size:1.25rem; font-weight:800; color:#2D2250; text-decoration:none; }
.nav-brand-icon { width:36px; height:36px; background:linear-gradient(135deg,#8B5CF6,#A78BFA); border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:1rem; }
.nav-actions { display:flex; gap:12px; }
.btn-outline { padding:8px 20px; border-radius:8px; border:1px solid rgba(139,92,246,0.4); background:transparent; color:#4C1D95; font-size:0.875rem; font-weight:500; cursor:pointer; text-decoration:none; transition:all 0.2s ease; display:inline-block; }
.btn-outline:hover { background:rgba(139,92,246,0.1); border-color:#8B5CF6; color:#7C3AED; }
.btn-primary { padding:8px 20px; border-radius:8px; background:linear-gradient(135deg,#8B5CF6,#7C3AED); border:none; color:#fff; font-size:0.875rem; font-weight:700; cursor:pointer; text-decoration:none; transition:all 0.2s ease; display:inline-block; }
.btn-primary:hover { transform:translateY(-1px); box-shadow:0 6px 20px rgba(139,92,246,0.35); }

/* ── Hero ── */
.hero { display:flex; align-items:center; justify-content:space-between; padding:80px 60px 60px; gap:60px; min-height:calc(100vh - 110px); position:relative; z-index:1; }
.hero-left { flex:1; max-width:560px; }
.hero-badge { display:inline-flex; align-items:center; gap:8px; background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.28); border-radius:100px; padding:6px 14px; font-size:0.8rem; font-weight:500; color:#7C3AED; margin-bottom:28px; animation:fadeUp 0.6s ease both; }
.badge-dot { width:7px; height:7px; border-radius:50%; background:#8B5CF6; animation:dotPulse 1.8s ease-in-out infinite; }
.hero-title { font-size:clamp(2.4rem,4.5vw,3.6rem); font-weight:800; line-height:1.1; color:#1E1245; margin-bottom:20px; animation:fadeUp 0.6s 0.1s ease both; }
.hero-title span { background:linear-gradient(135deg,#8B5CF6,#C4B5FD); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.hero-desc { font-size:1.05rem; line-height:1.7; color:#6B7280; margin-bottom:36px; animation:fadeUp 0.6s 0.2s ease both; }
.hero-buttons { display:flex; gap:14px; flex-wrap:wrap; animation:fadeUp 0.6s 0.3s ease both; }
.btn-hero-primary { display:inline-flex; align-items:center; gap:8px; padding:13px 28px; border-radius:10px; background:linear-gradient(135deg,#8B5CF6,#7C3AED); color:#fff; font-weight:700; font-size:0.95rem; text-decoration:none; border:none; cursor:pointer; transition:all 0.25s ease; }
.btn-hero-primary:hover { transform:translateY(-2px); box-shadow:0 8px 28px rgba(139,92,246,0.4); }
.btn-hero-secondary { display:inline-flex; align-items:center; gap:8px; padding:13px 28px; border-radius:10px; background:rgba(139,92,246,0.06); border:1px solid rgba(139,92,246,0.22); color:#4C1D95; font-weight:500; font-size:0.95rem; text-decoration:none; cursor:pointer; transition:all 0.25s ease; }
.btn-hero-secondary:hover { background:rgba(139,92,246,0.12); border-color:rgba(139,92,246,0.4); transform:translateY(-2px); }

/* ── Resume card ── */
.hero-right { flex:1; max-width:460px; animation:slideInRight 0.7s 0.2s ease both; position:relative; z-index:1; }
.resume-card { background:#FAF8FF; border:1px solid rgba(139,92,246,0.22); border-radius:18px; padding:24px; position:relative; animation:float 4s ease-in-out infinite; box-shadow:0 8px 40px rgba(139,92,246,0.12); }
.match-badge { position:absolute; top:-14px; right:20px; background:linear-gradient(135deg,#8B5CF6,#7C3AED); color:#fff; font-size:0.78rem; font-weight:700; padding:6px 14px; border-radius:100px; display:flex; align-items:center; gap:6px; }
.card-name { font-size:1.1rem; font-weight:700; color:#1E1245; }
.card-role { font-size:0.82rem; color:#9CA3AF; margin-top:3px; margin-bottom:18px; }
.section-label { font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#7C3AED; margin-bottom:12px; }
.skill-row { margin-bottom:10px; }
.skill-info { display:flex; justify-content:space-between; font-size:0.82rem; color:#6B7280; margin-bottom:5px; }
.skill-bar-bg { height:6px; background:rgba(139,92,246,0.1); border-radius:100px; overflow:hidden; }
.skill-bar-fill { height:100%; border-radius:100px; background:linear-gradient(90deg,#8B5CF6,#C4B5FD); animation:barGrow 1.2s 0.5s cubic-bezier(0.25,0.8,0.25,1) both; }
.tags-row { display:flex; flex-wrap:wrap; gap:7px; margin-top:14px; }
.tag { padding:4px 11px; border-radius:100px; font-size:0.76rem; font-weight:500; background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.25); color:#7C3AED; }
.card-footer { display:flex; justify-content:space-between; align-items:center; margin-top:18px; padding-top:16px; border-top:1px solid rgba(139,92,246,0.1); }
.ats-num { font-size:1.6rem; font-weight:800; background:linear-gradient(135deg,#7C3AED,#8B5CF6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.ats-label { font-size:0.72rem; color:#9CA3AF; }
.ats-badge { display:inline-flex; align-items:center; gap:6px; background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.28); color:#16A34A; font-size:0.78rem; font-weight:600; padding:5px 12px; border-radius:100px; animation:pulse 2s ease-in-out infinite; }
.score-pill { display:inline-flex; align-items:center; gap:8px; background:#FAF8FF; border:1px solid rgba(139,92,246,0.22); border-radius:100px; padding:8px 18px; font-size:0.88rem; color:#2D2250; font-weight:500; margin-top:16px; box-shadow:0 2px 12px rgba(139,92,246,0.08); }
.score-pill span { color:#7C3AED; font-weight:700; }

/* ── Features ── */
.features { padding:60px 60px 80px; background:#EDE9FF; border-top:1px solid rgba(139,92,246,0.1); position:relative; z-index:1; }
.features-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:20px; }
.feature-card { background:#FAF8FF; border:1px solid rgba(139,92,246,0.14); border-radius:14px; padding:24px; transition:all 0.25s ease; animation:fadeUp 0.6s ease both; }
.feature-card:hover { transform:translateY(-4px); border-color:rgba(139,92,246,0.4); box-shadow:0 12px 32px rgba(139,92,246,0.12); }
.feature-icon { width:42px; height:42px; background:rgba(139,92,246,0.12); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem; margin-bottom:14px; }
.feature-title { font-size:0.97rem; font-weight:600; color:#1E1245; margin-bottom:7px; }
.feature-desc { font-size:0.83rem; color:#6B7280; line-height:1.6; }

/* ── How it works ── */
.how-section { padding:80px 60px; background:#F0EEFF; position:relative; z-index:1; }
.section-header { text-align:center; margin-bottom:52px; }
.section-eyebrow { font-size:0.78rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#7C3AED; margin-bottom:12px; }
.section-title { font-size:clamp(1.6rem,3vw,2.2rem); font-weight:800; color:#1E1245; }
.steps-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:24px; }
.step-card { background:#FAF8FF; border:1px solid rgba(139,92,246,0.14); border-radius:14px; padding:28px 24px; text-align:center; transition:all 0.25s ease; }
.step-card:hover { transform:translateY(-4px); border-color:rgba(139,92,246,0.35); box-shadow:0 8px 24px rgba(139,92,246,0.1); }
.step-num { width:38px; height:38px; border-radius:50%; background:rgba(139,92,246,0.12); border:1px solid rgba(139,92,246,0.35); display:flex; align-items:center; justify-content:center; font-size:0.85rem; font-weight:700; color:#7C3AED; margin:0 auto 16px; }
.step-title { font-size:0.95rem; font-weight:600; color:#1E1245; margin-bottom:8px; }
.step-desc { font-size:0.82rem; color:#6B7280; line-height:1.6; }

/* ── CTA ── */
.cta-section { padding:80px 60px; background:#EDE9FF; border-top:1px solid rgba(139,92,246,0.1); position:relative; z-index:1; }
.cta-inner { background:linear-gradient(135deg,rgba(139,92,246,0.08),rgba(196,181,253,0.1)); border:1px solid rgba(139,92,246,0.22); border-radius:20px; padding:56px 48px; text-align:center; }
.cta-title { font-size:clamp(1.5rem,3vw,2rem); font-weight:800; color:#1E1245; margin-bottom:14px; }
.cta-desc { font-size:1rem; color:#6B7280; margin-bottom:32px; }
.cta-buttons { display:flex; justify-content:center; gap:14px; flex-wrap:wrap; }

/* ── Footer ── */
.footer { padding:30px 60px; background:#E9E4FF; border-top:1px solid rgba(139,92,246,0.12); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; position:relative; z-index:1; }
.footer-text { font-size:0.82rem; color:#9CA3AF; }
.footer-brand { font-size:0.9rem; font-weight:700; color:#7C3AED; }
.footer-admin { font-size:0.75rem; color:rgba(139,92,246,0.25); text-decoration:none; transition:color 0.2s; }
.footer-admin:hover { color:#7C3AED; }

@media (max-width:900px) {
    .hero { flex-direction:column; padding:48px 24px 40px; }
    .hero-right { max-width:100%; width:100%; }
    .nav { padding:16px 24px; }
    .features, .how-section, .cta-section, .footer { padding-left:24px; padding-right:24px; }
    .cv-deco { display:none; }
}
</style>
""")

st.html("""
<canvas id="cvLeft"  style="position:fixed;top:0;left:0;width:52px;height:100vh;pointer-events:none;z-index:0;"></canvas>
<canvas id="cvRight" style="position:fixed;top:0;right:0;width:52px;height:100vh;pointer-events:none;z-index:0;"></canvas>
<script>
(function(){
  var colors=['#8B5CF6','#A78BFA','#C4B5FD','#7C3AED'];
  function rnd(a,b){return a+Math.random()*(b-a);}
  function pick(arr){return arr[Math.floor(Math.random()*arr.length)];}
  function makeP(H){
    return {
      type: pick(['line','line','dot','dot','doc','bar']),
      y: H + rnd(0,500), speed: rnd(0.35,0.7),
      color: pick(colors), w: rnd(12,26),
      x: rnd(4,18), alpha: rnd(0.13,0.22)
    };
  }
  function draw(ctx,p){
    ctx.globalAlpha=p.alpha;
    ctx.fillStyle=p.color;
    ctx.strokeStyle=p.color;
    ctx.lineWidth=1.5;
    if(p.type==='line'){
      ctx.beginPath();ctx.rect(p.x,p.y,p.w,3);ctx.fill();
      ctx.globalAlpha=p.alpha*0.6;
      ctx.beginPath();ctx.rect(p.x,p.y+8,p.w*0.65,3);ctx.fill();
    } else if(p.type==='dot'){
      [0,10,20].forEach(function(o){
        ctx.globalAlpha=p.alpha*(1-o*0.02);
        ctx.beginPath();ctx.arc(p.x+4,p.y+o,3,0,Math.PI*2);ctx.fill();
      });
    } else if(p.type==='doc'){
      ctx.globalAlpha=p.alpha;
      ctx.strokeRect(p.x,p.y,20,25);
      ctx.fillRect(p.x+3,p.y+5,12,2);
      ctx.fillRect(p.x+3,p.y+10,9,2);
      ctx.fillRect(p.x+3,p.y+15,11,2);
    } else {
      [[0,14],[8,9],[16,18]].forEach(function(b,i){
        ctx.globalAlpha=p.alpha*(0.7+i*0.1);
        ctx.fillRect(p.x+b[0],p.y+18-b[1],6,b[1]);
      });
    }
    ctx.globalAlpha=1;
  }
  function lane(id){
    var el=document.getElementById(id);
    if(!el)return;
    var H=window.innerHeight;
    el.width=52;el.height=H;
    var ctx=el.getContext('2d');
    var ps=Array.from({length:8},function(){return makeP(H);});
    // stagger start positions
    ps.forEach(function(p,i){p.y=rnd(0,H);});
    (function tick(){
      ctx.clearRect(0,0,52,H);
      ps.forEach(function(p){
        p.y-=p.speed;
        if(p.y<-60){Object.assign(p,makeP(H));p.y=H+10;}
        draw(ctx,p);
      });
      requestAnimationFrame(tick);
    })();
  }
  window.addEventListener('load',function(){lane('cvLeft');lane('cvRight');});
})();
</script>
""")

st.html("""
<div class="ticker">
  <span class="ticker-inner">
    &#128161; Currently optimized for IT &amp; Computer Science resumes &#8212; Developer, Data Scientist, DevOps, Business Analyst &amp; more. Results may vary for non-IT domains. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &#128161; Currently optimized for IT &amp; Computer Science resumes &#8212; Developer, Data Scientist, DevOps, Business Analyst &amp; more. Results may vary for non-IT domains.
  </span>
</div>
""")

st.html("""
<nav class="nav">
  <a class="nav-brand" href="#">
    <div class="nav-brand-icon">&#128196;</div>
    ResumeAI
  </a>
  <div class="nav-actions">
    <a class="btn-outline" href="/Login">Login</a>
    <a class="btn-outline" href="/Admin">&#128737; Admin</a>
    <a class="btn-primary" href="/Register">Get Started</a>
  </div>
</nav>
""")

st.html("""
<section class="hero">
  <div class="hero-left">
    <div class="hero-badge"><div class="badge-dot"></div>AI-powered resume intelligence</div>
    <h1 class="hero-title">Analyze, Score &amp;<br><span>Generate</span> your resume<br>with AI</h1>
    <p class="hero-desc">Upload your PDF resume. Our ML model scans your skills, predicts the best job roles, checks ATS compatibility, and gives you a score instantly.</p>
    <div class="hero-buttons">
      <a class="btn-hero-primary" href="/Dashboard">&#8593; Analyze Resume</a>
      <a class="btn-hero-secondary" href="/Generator">&#10022; Generate Resume</a>
    </div>
  </div>
  <div class="hero-right">
    <div class="resume-card">
      <div class="match-badge">&#129302; Data Scientist match</div>
      <div class="card-name">Aishwarya Poojari</div>
      <div class="card-role">Data Science &nbsp;|&nbsp; Entry Level</div>
      <div class="section-label">Skill Match</div>
      <div class="skill-row"><div class="skill-info"><span>Python</span><span>95%</span></div><div class="skill-bar-bg"><div class="skill-bar-fill" style="width:95%"></div></div></div>
      <div class="skill-row"><div class="skill-info"><span>SQL</span><span>82%</span></div><div class="skill-bar-bg"><div class="skill-bar-fill" style="width:82%"></div></div></div>
      <div class="skill-row"><div class="skill-info"><span>ML</span><span>88%</span></div><div class="skill-bar-bg"><div class="skill-bar-fill" style="width:88%"></div></div></div>
      <div class="section-label" style="margin-top:18px">Detected Skills</div>
      <div class="tags-row"><span class="tag">Python</span><span class="tag">SQL</span><span class="tag">Scikit-learn</span><span class="tag">Pandas</span><span class="tag">Communication</span></div>
      <div class="card-footer">
        <div class="ats-badge">&#10003; ATS compatible</div>
        <div style="text-align:right"><div class="ats-num">87%</div><div class="ats-label">ATS Score / Resume strength</div></div>
      </div>
    </div>
    <div style="text-align:center;margin-top:14px;"><div class="score-pill">&#128202; Score: <span>87 / 100</span></div></div>
  </div>
</section>
""")

st.html("""
<section class="features">
  <div class="features-grid">
    <div class="feature-card"><div class="feature-icon">&#128269;</div><div class="feature-title">Resume scanning</div><div class="feature-desc">Extracts text from your PDF resume using advanced pdfplumber parsing.</div></div>
    <div class="feature-card"><div class="feature-icon">&#10024;</div><div class="feature-title">Skill detection</div><div class="feature-desc">Matches 50+ technical and soft skills against a curated skills database.</div></div>
    <div class="feature-card"><div class="feature-icon">&#129302;</div><div class="feature-title">Job role prediction</div><div class="feature-desc">Naive Bayes ML model trained on thousands of resumes predicts your best-fit role.</div></div>
    <div class="feature-card"><div class="feature-icon">&#128203;</div><div class="feature-title">ATS compatibility</div><div class="feature-desc">Checks if your resume passes Applicant Tracking Systems used by top companies.</div></div>
  </div>
</section>
""")

st.html("""
<section class="how-section">
  <div class="section-header">
    <div class="section-eyebrow">How it works</div>
    <h2 class="section-title">From upload to insights in seconds</h2>
  </div>
  <div class="steps-grid">
    <div class="step-card"><div class="step-num">1</div><div class="step-title">Upload your PDF</div><div class="step-desc">Drop your resume PDF into the analyzer dashboard.</div></div>
    <div class="step-card"><div class="step-num">2</div><div class="step-title">Text extraction</div><div class="step-desc">pdfplumber pulls every word, preserving layout and structure.</div></div>
    <div class="step-card"><div class="step-num">3</div><div class="step-title">Skill and role analysis</div><div class="step-desc">TF-IDF vectorization plus Naive Bayes identifies skills and predicts your job category.</div></div>
    <div class="step-card"><div class="step-num">4</div><div class="step-title">Score and feedback</div><div class="step-desc">Get your ATS score, missing skills list, and actionable improvement tips.</div></div>
    <div class="step-card"><div class="step-num">5</div><div class="step-title">Generate or improve</div><div class="step-desc">Use the Generator to create a polished, ATS-ready resume in one click.</div></div>
  </div>
</section>
""")

st.html("""
<section class="cta-section">
  <div class="cta-inner">
    <h2 class="cta-title">Ready to land your dream job?</h2>
    <p class="cta-desc">Join thousands of job seekers who improved their resumes with AI-powered feedback.</p>
    <div class="cta-buttons">
      <a class="btn-hero-primary" href="/Register">Create free account</a>
      <a class="btn-hero-secondary" href="/Login">Sign in</a>
    </div>
  </div>
</section>
""")

st.html("""
<footer class="footer">
  <div class="footer-brand">&#128196; ResumeAI</div>
  <div class="footer-text">Built with Python &#183; Streamlit &#183; Scikit-learn &#183; pdfplumber</div>
  <div class="footer-text">&#169; 2025 Aishwarya Poojari</div>
  <a class="footer-admin" href="/Admin">&#128737; Admin</a>
</footer>
""")
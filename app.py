import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Delta Studio | Yaratıcı ve Dijital Çözümler",
    layout="wide",
    page_icon="🎬",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Space+Grotesk:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body,.stApp{font-family:'Space Grotesk',sans-serif;background:#040410;color:#c0cce0;overflow-x:hidden}
#MainMenu,header[data-testid="stHeader"],footer{visibility:hidden !important}
.block-container{padding:0 !important;max-width:100% !important}
section[data-testid="stSidebar"]{display:none !important}
div[data-testid="stDecoration"]{display:none !important}
.stMarkdown{position:relative;z-index:1}
.ds-bg{position:fixed;inset:0;z-index:0;pointer-events:none;background:radial-gradient(ellipse 900px 700px at 10% 5%,rgba(0,212,255,.06) 0%,transparent 70%),radial-gradient(ellipse 700px 900px at 90% 95%,rgba(123,47,255,.08) 0%,transparent 70%),radial-gradient(ellipse 500px 500px at 55% 45%,rgba(255,0,110,.04) 0%,transparent 70%),#040410}
.ds-grid-lines{position:fixed;inset:0;z-index:0;pointer-events:none;background-image:linear-gradient(rgba(0,212,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,.025) 1px,transparent 1px);background-size:72px 72px}
h1,h2,h3,h4,h5{font-family:'Orbitron',sans-serif}
.ds-tag{display:inline-flex;align-items:center;gap:10px;font-family:'Share Tech Mono',monospace;font-size:10px;color:#00d4ff;letter-spacing:4px;text-transform:uppercase;margin-bottom:18px}
.ds-tag::before{content:'//';opacity:.45}
.ds-tag::after{content:'';width:48px;height:1px;background:linear-gradient(90deg,#00d4ff,transparent)}
.ds-heading{font-family:'Orbitron',sans-serif;font-size:clamp(26px,3vw,46px);font-weight:900;color:#fff;line-height:1.15;margin-bottom:18px;letter-spacing:.5px}
.ds-heading .grad{background:linear-gradient(135deg,#00d4ff 0%,#7b2fff 55%,#ff006e 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.ds-heading .stroke{color:transparent;-webkit-text-stroke:1.5px #00d4ff}
.ds-lead{font-size:16px;color:rgba(192,204,224,.55);line-height:1.85;max-width:580px}
.ds-nav{position:sticky;top:0;z-index:999;height:70px;display:flex;align-items:center;justify-content:space-between;padding:0 72px;background:rgba(4,4,16,.82);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);border-bottom:1px solid rgba(0,212,255,.12)}
.ds-nav-logo{font-family:'Orbitron',sans-serif;font-size:20px;font-weight:900;letter-spacing:5px;text-transform:uppercase;color:#fff;display:flex;align-items:center;gap:8px}
.ds-nav-logo::before{content:'◈';font-size:16px;color:#00d4ff}
.ds-nav-logo em{color:#00d4ff;font-style:normal}
.ds-nav-links{display:flex;align-items:center;gap:36px}
.ds-nav-links a{font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:600;letter-spacing:2.5px;text-transform:uppercase;color:rgba(192,204,224,.65);text-decoration:none;transition:color .3s;position:relative}
.ds-nav-links a::after{content:'';position:absolute;bottom:-6px;left:0;width:0;height:1px;background:linear-gradient(90deg,#00d4ff,#7b2fff);transition:width .3s}
.ds-nav-links a:hover{color:#00d4ff}
.ds-nav-links a:hover::after{width:100%}
.ds-nav-cta{border:1px solid rgba(0,212,255,.5) !important;color:#00d4ff !important;padding:7px 22px !important;border-radius:4px !important;transition:all .3s !important}
.ds-nav-cta:hover{background:rgba(0,212,255,.08) !important;box-shadow:0 0 18px rgba(0,212,255,.25) !important;color:#fff !important}
.ds-hero{min-height:calc(100vh - 70px);display:flex;align-items:center;padding:100px 72px 120px;position:relative;overflow:hidden;z-index:1}
.ds-hero-content{max-width:700px}
.ds-hero-badge{display:inline-flex;align-items:center;gap:10px;background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.2);padding:9px 22px;border-radius:100px;font-family:'Share Tech Mono',monospace;font-size:10px;color:#00d4ff;letter-spacing:3.5px;text-transform:uppercase;margin-bottom:36px}
.ds-hero-badge::before{content:'';width:7px;height:7px;border-radius:50%;background:#00d4ff;animation:blink 2s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.35;transform:scale(.75)}}
.ds-hero-title{font-family:'Orbitron',sans-serif;font-size:clamp(42px,5.5vw,86px);font-weight:900;line-height:1.08;color:#fff;letter-spacing:-1px;margin-bottom:28px}
.ds-hero-title .grad-line{display:block;background:linear-gradient(135deg,#00d4ff 0%,#7b2fff 50%,#ff006e 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.ds-hero-sub{font-size:17px;color:rgba(192,204,224,.5);line-height:1.9;max-width:500px;margin-bottom:52px}
.ds-hero-btns{display:flex;gap:18px;flex-wrap:wrap;align-items:center}
.ds-btn-primary{display:inline-flex;align-items:center;gap:10px;background:linear-gradient(135deg,#00d4ff,#7b2fff);color:#fff;padding:15px 38px;border-radius:6px;font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;transition:all .35s;box-shadow:0 8px 32px rgba(0,212,255,.2)}
.ds-btn-primary:hover{transform:translateY(-3px);box-shadow:0 16px 48px rgba(0,212,255,.35);filter:brightness(1.1)}
.ds-btn-ghost{display:inline-flex;align-items:center;gap:10px;background:transparent;color:rgba(192,204,224,.75);padding:15px 38px;border-radius:6px;font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;border:1px solid rgba(192,204,224,.15);transition:all .3s}
.ds-btn-ghost:hover{border-color:rgba(192,204,224,.4);color:#fff}
.ds-hero-stats{display:flex;gap:52px;margin-top:68px;padding-top:52px;border-top:1px solid rgba(192,204,224,.07);flex-wrap:wrap}
.ds-stat-val{font-family:'Orbitron',sans-serif;font-size:34px;font-weight:900;color:#fff;line-height:1}
.ds-stat-val em{color:#00d4ff;font-style:normal}
.ds-stat-lbl{font-family:'Share Tech Mono',monospace;font-size:10px;color:rgba(192,204,224,.38);letter-spacing:2.5px;text-transform:uppercase;margin-top:7px}
.ds-orbs{position:absolute;right:0;top:50%;transform:translateY(-50%);width:560px;height:560px;pointer-events:none;opacity:.18}
.ds-orb{position:absolute;border-radius:50%;animation:float 9s ease-in-out infinite}
.ds-orb-1{width:380px;height:380px;background:radial-gradient(circle,#00d4ff,transparent 68%);top:0;right:0;animation-delay:0s}
.ds-orb-2{width:280px;height:280px;background:radial-gradient(circle,#7b2fff,transparent 68%);bottom:0;right:90px;animation-delay:2.5s}
.ds-orb-3{width:190px;height:190px;background:radial-gradient(circle,#ff006e,transparent 68%);top:90px;right:180px;animation-delay:5s}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-28px)}}
.ds-section{padding:120px 72px;position:relative;z-index:1}
.ds-section.dim{background:rgba(255,255,255,.012)}
.ds-sec-hdr{margin-bottom:72px}
.ds-divider{height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,.13),transparent);margin:0 72px;position:relative;z-index:1}
.ds-srv-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.ds-srv-card{background:rgba(255,255,255,.022);border:1px solid rgba(255,255,255,.06);border-radius:18px;padding:42px 38px 56px;position:relative;overflow:hidden;transition:all .4s cubic-bezier(.25,.46,.45,.94);cursor:default}
.ds-srv-card::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent 0%,#00d4ff 50%,transparent 100%);opacity:0;transition:opacity .4s}
.ds-srv-card:hover{background:rgba(0,212,255,.038);border-color:rgba(0,212,255,.22);transform:translateY(-10px);box-shadow:0 36px 72px rgba(0,0,0,.5),0 0 0 1px rgba(0,212,255,.1)}
.ds-srv-card:hover::after{opacity:1}
.ds-srv-icon{width:58px;height:58px;background:rgba(0,212,255,.09);border:1px solid rgba(0,212,255,.18);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:26px;margin-bottom:26px;transition:all .4s}
.ds-srv-card:hover .ds-srv-icon{background:rgba(0,212,255,.14);box-shadow:0 0 24px rgba(0,212,255,.25)}
.ds-srv-num{font-family:'Share Tech Mono',monospace;font-size:10px;color:rgba(0,212,255,.38);letter-spacing:2.5px;margin-bottom:12px}
.ds-srv-title{font-family:'Orbitron',sans-serif;font-size:14px;font-weight:700;color:#fff;margin-bottom:14px;line-height:1.45;letter-spacing:.3px}
.ds-srv-desc{font-size:13.5px;color:rgba(192,204,224,.48);line-height:1.75}
.ds-srv-arrow{position:absolute;bottom:30px;right:30px;width:34px;height:34px;border:1px solid rgba(0,212,255,.2);border-radius:50%;display:flex;align-items:center;justify-content:center;color:#00d4ff;font-size:15px;opacity:0;transform:translateX(-12px);transition:all .35s}
.ds-srv-card:hover .ds-srv-arrow{opacity:1;transform:translateX(0)}
.ds-case-grid{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.ds-case-card{background:rgba(255,255,255,.022);border:1px solid rgba(255,255,255,.06);border-radius:20px;padding:52px;position:relative;overflow:hidden;transition:all .4s}
.ds-case-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#00d4ff,#7b2fff,#ff006e);transform:scaleX(0);transform-origin:left;transition:transform .5s ease}
.ds-case-card:hover{background:rgba(0,212,255,.028);border-color:rgba(0,212,255,.16);transform:translateY(-5px)}
.ds-case-card:hover::after{transform:scaleX(1)}
.ds-case-client{font-family:'Share Tech Mono',monospace;font-size:10px;color:#00d4ff;letter-spacing:3.5px;text-transform:uppercase;margin-bottom:18px;display:flex;align-items:center;gap:8px}
.ds-case-client::before{content:'//';opacity:.45}
.ds-case-title{font-family:'Orbitron',sans-serif;font-size:19px;font-weight:700;color:#fff;margin-bottom:16px;line-height:1.35}
.ds-case-desc{font-size:14px;color:rgba(192,204,224,.5);line-height:1.82;margin-bottom:36px}
.ds-metrics{display:flex;gap:36px;flex-wrap:wrap}
.ds-metric-val{font-family:'Orbitron',sans-serif;font-size:30px;font-weight:900;background:linear-gradient(135deg,#00d4ff,#7b2fff);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;line-height:1}
.ds-metric-lbl{font-family:'Share Tech Mono',monospace;font-size:9px;color:rgba(192,204,224,.38);letter-spacing:1.5px;text-transform:uppercase;margin-top:6px}
.ds-testi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.ds-testi-card{background:rgba(255,255,255,.022);border:1px solid rgba(255,255,255,.06);border-radius:18px;padding:42px;position:relative;transition:all .4s}
.ds-testi-card::before{content:'"';position:absolute;top:16px;left:38px;font-family:'Orbitron',sans-serif;font-size:100px;font-weight:900;color:#00d4ff;opacity:.08;line-height:1;pointer-events:none}
.ds-testi-card:hover{background:rgba(123,47,255,.04);border-color:rgba(123,47,255,.22);transform:translateY(-7px);box-shadow:0 24px 56px rgba(123,47,255,.12)}
.ds-stars{color:#00d4ff;font-size:14px;letter-spacing:2px;margin-bottom:22px}
.ds-testi-text{font-size:14.5px;color:rgba(192,204,224,.68);line-height:1.82;font-style:italic;margin-bottom:30px}
.ds-testi-author{display:flex;align-items:center;gap:14px}
.ds-avatar{width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#7b2fff);display:flex;align-items:center;justify-content:center;font-family:'Orbitron',sans-serif;font-size:17px;font-weight:700;color:#fff;flex-shrink:0}
.ds-author-name{font-family:'Space Grotesk',sans-serif;font-size:14px;font-weight:700;color:#fff}
.ds-author-co{font-family:'Share Tech Mono',monospace;font-size:10px;color:rgba(0,212,255,.55);letter-spacing:1.5px;margin-top:3px}
.ds-contact-wrap{display:grid;grid-template-columns:1fr 1.2fr;gap:88px;align-items:start}
.ds-contact-item{display:flex;align-items:flex-start;gap:18px;margin-bottom:30px}
.ds-ci-icon{width:50px;height:50px;background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.18);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0}
.ds-ci-label{font-family:'Share Tech Mono',monospace;font-size:9px;color:rgba(0,212,255,.55);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:5px}
.ds-ci-val{font-size:15px;color:rgba(192,204,224,.82)}
.stTextInput>label,.stTextArea>label{font-family:'Share Tech Mono',monospace !important;font-size:10px !important;color:rgba(0,212,255,.6) !important;letter-spacing:2.5px !important;text-transform:uppercase !important}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:rgba(255,255,255,.03) !important;border:1px solid rgba(255,255,255,.08) !important;border-radius:8px !important;color:#c0cce0 !important;font-family:'Space Grotesk',sans-serif !important;font-size:15px !important;caret-color:#00d4ff !important;transition:all .3s !important}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border-color:rgba(0,212,255,.4) !important;background:rgba(0,212,255,.04) !important;box-shadow:0 0 0 3px rgba(0,212,255,.1) !important;outline:none !important}
div[data-testid="stFormSubmitButton"]>button{background:linear-gradient(135deg,#00d4ff,#7b2fff) !important;color:#fff !important;border:none !important;border-radius:8px !important;padding:16px 0 !important;width:100% !important;font-family:'Space Grotesk',sans-serif !important;font-size:13px !important;font-weight:700 !important;letter-spacing:2.5px !important;text-transform:uppercase !important;cursor:pointer !important;transition:all .3s !important}
div[data-testid="stFormSubmitButton"]>button:hover{opacity:.9 !important;box-shadow:0 10px 36px rgba(0,212,255,.35) !important;transform:translateY(-2px) !important}
.stSelectbox>label{font-family:'Share Tech Mono',monospace !important;font-size:10px !important;color:rgba(0,212,255,.6) !important;letter-spacing:2.5px !important;text-transform:uppercase !important}
.ds-footer{background:rgba(255,255,255,.012);border-top:1px solid rgba(255,255,255,.05);padding:88px 72px 42px;position:relative;z-index:1}
.ds-footer-grid{display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr;gap:56px;margin-bottom:72px}
.ds-footer-logo{font-family:'Orbitron',sans-serif;font-size:19px;font-weight:900;letter-spacing:5px;color:#fff;margin-bottom:22px}
.ds-footer-logo em{color:#00d4ff;font-style:normal}
.ds-footer-desc{font-size:13.5px;color:rgba(192,204,224,.38);line-height:1.85;max-width:290px;margin-bottom:30px}
.ds-socials{display:flex;gap:12px}
.ds-social{width:42px;height:42px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:9px;display:flex;align-items:center;justify-content:center;color:rgba(192,204,224,.45);text-decoration:none;font-size:16px;transition:all .3s}
.ds-social:hover{background:rgba(0,212,255,.1);border-color:rgba(0,212,255,.3);color:#00d4ff;transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,212,255,.2)}
.ds-footer-col h5{font-family:'Orbitron',sans-serif;font-size:11px;font-weight:700;color:#fff;letter-spacing:3px;text-transform:uppercase;margin-bottom:26px}
.ds-footer-links{display:flex;flex-direction:column;gap:14px}
.ds-footer-links a{font-size:13.5px;color:rgba(192,204,224,.38);text-decoration:none;display:flex;align-items:center;gap:8px;transition:color .3s}
.ds-footer-links a::before{content:'›';color:#00d4ff;opacity:0;transition:opacity .3s}
.ds-footer-links a:hover{color:rgba(192,204,224,.8)}
.ds-footer-links a:hover::before{opacity:1}
.ds-footer-bottom{border-top:1px solid rgba(255,255,255,.05);padding-top:34px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px}
.ds-copy{font-family:'Share Tech Mono',monospace;font-size:11px;color:rgba(192,204,224,.22);letter-spacing:1px}
.ds-status{display:flex;align-items:center;gap:8px;font-family:'Share Tech Mono',monospace;font-size:10px;color:rgba(192,204,224,.22);letter-spacing:1px}
.ds-status::before{content:'';width:7px;height:7px;border-radius:50%;background:#00d4ff;animation:blink 2s ease-in-out infinite}
.stImage img{border-radius:14px !important;border:1px solid rgba(255,255,255,.06) !important;transition:all .4s ease !important}
.stSuccess>div{background:rgba(0,212,255,.08) !important;border:1px solid rgba(0,212,255,.25) !important;border-radius:10px !important;color:#00d4ff !important}
.stError>div{background:rgba(255,0,110,.08) !important;border:1px solid rgba(255,0,110,.25) !important;border-radius:10px !important}
.stInfo>div{background:rgba(123,47,255,.08) !important;border:1px solid rgba(123,47,255,.25) !important;border-radius:10px !important}
@media(max-width:900px){.ds-nav{padding:0 24px}.ds-hero{padding:72px 24px 88px}.ds-section{padding:80px 24px}.ds-divider{margin:0 24px}.ds-footer{padding:72px 24px 36px}.ds-srv-grid{grid-template-columns:1fr}.ds-case-grid{grid-template-columns:1fr}.ds-testi-grid{grid-template-columns:1fr}.ds-contact-wrap{grid-template-columns:1fr;gap:48px}.ds-footer-grid{grid-template-columns:1fr 1fr;gap:32px}.ds-hero-title{font-size:clamp(36px,9vw,56px)}.ds-hero-stats{gap:28px}.ds-orbs{opacity:.08}.ds-nav-links{display:none}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="ds-bg"></div><div class="ds-grid-lines"></div>', unsafe_allow_html=True)

def send_email(isim, eposta, mesaj):
    gonderici_email = "deltajanss0@gmail.com"
    alici_email     = "deltajanss0@gmail.com"
    sifre           = "orputhixhpumhuzf"
    msg             = MIMEMultipart()
    msg['From']     = gonderici_email
    msg['To']       = alici_email
    msg['Subject']  = f"Delta Studio Web: Yeni Proje Talebi - {isim}"
    body = f"Web sitesinden yeni bir mesaj.\n\nİsim: {isim}\nE-posta: {eposta}\n\nMesaj:\n{mesaj}"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gonderici_email, sifre)
        server.sendmail(gonderici_email, alici_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return str(e)

st.markdown("""
<div class="ds-nav">
    <div class="ds-nav-logo">DELTA <em>STUDIO</em></div>
    <nav class="ds-nav-links">
        <a href="#hizmetler">Hizmetler</a>
        <a href="#hikayeler">Başarı Hikayeleri</a>
        <a href="#galeri">Galeri</a>
        <a href="#iletisim" class="ds-nav-cta">Teklif Al</a>
    </nav>
</div>
""", unsafe_allow_html=True)

try:
    _c1, _c2 = st.columns([1, 11])
    with _c1:
        st.image("logo.png", width=90)
except Exception:
    pass

st.markdown("""
<section class="ds-hero" id="hero">
  <div class="ds-hero-content">
    <div class="ds-hero-badge">Yaratıcı Dijital Ajans · Türkiye</div>
    <h1 class="ds-hero-title">Markanı<br><span class="grad-line">Geleceğe Taşı</span></h1>
    <p class="ds-hero-sub">Sosyal medya yönetiminden kurumsal kimliğe, yazılımdan video prodüksiyona — markanızın her boyutunu profesyonel bir vizyonla şekillendiriyoruz.</p>
    <div class="ds-hero-btns">
      <a href="#iletisim" class="ds-btn-primary">Projeye Başla →</a>
      <a href="#hikayeler" class="ds-btn-ghost">Başarı Hikayeleri</a>
    </div>
    <div class="ds-hero-stats">
      <div><div class="ds-stat-val">50<em>+</em></div><div class="ds-stat-lbl">Tamamlanan Proje</div></div>
      <div><div class="ds-stat-val">30<em>+</em></div><div class="ds-stat-lbl">Mutlu Müşteri</div></div>
      <div><div class="ds-stat-val">3<em>+</em></div><div class="ds-stat-lbl">Yıl Deneyim</div></div>
      <div><div class="ds-stat-val">6<em>K+</em></div><div class="ds-stat-lbl">Üretilen İçerik</div></div>
    </div>
  </div>
  <div class="ds-orbs">
    <div class="ds-orb ds-orb-1"></div>
    <div class="ds-orb ds-orb-2"></div>
    <div class="ds-orb ds-orb-3"></div>
  </div>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="ds-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<section class="ds-section" id="hizmetler">
  <div class="ds-sec-hdr">
    <div class="ds-tag">Hizmetlerimiz</div>
    <h2 class="ds-heading">Markanız İçin<br><span class="stroke">Tam Kapsamlı</span> Çözümler</h2>
    <p class="ds-lead">Yaratıcı düşünce ve teknolojik altyapıyı bir araya getirerek markanızı rakiplerinizden farklılaştırıyoruz.</p>
  </div>
  <div class="ds-srv-grid">
    <div class="ds-srv-card"><div class="ds-srv-icon">📱</div><div class="ds-srv-num">01 / HİZMET</div><div class="ds-srv-title">Sosyal Medya Yönetimi</div><div class="ds-srv-desc">Stratejik içerik planlaması, topluluk yönetimi ve analitik raporlama ile sosyal medya varlığınızı büyütüyoruz.</div><div class="ds-srv-arrow">→</div></div>
    <div class="ds-srv-card"><div class="ds-srv-icon">💻</div><div class="ds-srv-num">02 / HİZMET</div><div class="ds-srv-title">Özel Yazılım &amp; Yasopanel</div><div class="ds-srv-desc">İşletmenize özel yazılım çözümleri ve Yasopanel ile operasyonel süreçlerinizi dijitalleştiriyoruz.</div><div class="ds-srv-arrow">→</div></div>
    <div class="ds-srv-card"><div class="ds-srv-icon">🎨</div><div class="ds-srv-num">03 / HİZMET</div><div class="ds-srv-title">Kurumsal Kimlik Tasarımı</div><div class="ds-srv-desc">Logo, kimlik rehberi ve marka dili oluşturarak markanızı görsel açıdan güçlü bir konuma taşıyoruz.</div><div class="ds-srv-arrow">→</div></div>
    <div class="ds-srv-card"><div class="ds-srv-icon">📊</div><div class="ds-srv-num">04 / HİZMET</div><div class="ds-srv-title">Stratejik Pazarlama</div><div class="ds-srv-desc">Veri odaklı stratejiler ile hedef kitlenize ulaşıyor, dönüşüm oranlarınızı artırıyoruz.</div><div class="ds-srv-arrow">→</div></div>
    <div class="ds-srv-card"><div class="ds-srv-icon">🎬</div><div class="ds-srv-num">05 / HİZMET</div><div class="ds-srv-title">Video Prodüksiyon</div><div class="ds-srv-desc">Profesyonel ekipman ve yaratıcı ekibimizle markanızın hikayesini güçlü videolarla anlatıyoruz.</div><div class="ds-srv-arrow">→</div></div>
    <div class="ds-srv-card"><div class="ds-srv-icon">✨</div><div class="ds-srv-num">06 / HİZMET</div><div class="ds-srv-title">Yaratıcı İçerik Üretimi</div><div class="ds-srv-desc">Özgün içerikler üreterek markanızı hedef kitlenizle buluşturuyor, etkileşimi artırıyoruz.</div><div class="ds-srv-arrow">→</div></div>
  </div>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="ds-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<section class="ds-section dim" id="hikayeler">
  <div class="ds-sec-hdr">
    <div class="ds-tag">Başarı Hikayeleri</div>
    <h2 class="ds-heading">Gerçek Sonuçlar,<br><span class="grad">Ölçülebilir</span> Başarı</h2>
    <p class="ds-lead">Müşterilerimizle birlikte yarattığımız başarı hikayelerini inceleyin.</p>
  </div>
  <div class="ds-case-grid">
    <div class="ds-case-card">
      <div class="ds-case-client">Müşteri → Caffoine</div>
      <div class="ds-case-title">Sosyal Medya Etkileşiminde Rekor Artış</div>
      <div class="ds-case-desc">Caffoine markası için geliştirdiğimiz içerik stratejisi ile organik erişim ve etkileşim oranlarını dramatik biçimde artırdık.</div>
      <div class="ds-metrics">
        <div><div class="ds-metric-val">%45</div><div class="ds-metric-lbl">Etkileşim Artışı</div></div>
        <div><div class="ds-metric-val">3×</div><div class="ds-metric-lbl">Organik Erişim</div></div>
        <div><div class="ds-metric-val">6 ay</div><div class="ds-metric-lbl">Süre</div></div>
      </div>
    </div>
    <div class="ds-case-card">
      <div class="ds-case-client">Müşteri → Yasopanel</div>
      <div class="ds-case-title">Operasyonel Verimliliğin Dijital Dönüşümü</div>
      <div class="ds-case-desc">Yasopanel yazılımı ile işletmelerin operasyonel süreçlerini dijitalleştirdik, hata oranlarını minimize ettik.</div>
      <div class="ds-metrics">
        <div><div class="ds-metric-val">%60</div><div class="ds-metric-lbl">Hız Artışı</div></div>
        <div><div class="ds-metric-val">%85</div><div class="ds-metric-lbl">Hata Azalması</div></div>
        <div><div class="ds-metric-val">12 sa</div><div class="ds-metric-lbl">Kazanılan/Hafta</div></div>
      </div>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="ds-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<section class="ds-section" id="yorumlar">
  <div class="ds-sec-hdr">
    <div class="ds-tag">Müşteri Görüşleri</div>
    <h2 class="ds-heading">Onlar Ne <span class="grad">Diyor?</span></h2>
    <p class="ds-lead">Birlikte çalıştığımız markaların deneyimlerini keşfedin.</p>
  </div>
  <div class="ds-testi-grid">
    <div class="ds-testi-card"><div class="ds-stars">★★★★★</div><div class="ds-testi-text">"Delta Studio ile çalışmak markamızın dijital dönüşümünü hızlandırdı. Sosyal medya etkileşimimiz inanılmaz arttı."</div><div class="ds-testi-author"><div class="ds-avatar">K</div><div><div class="ds-author-name">Keyf-i Deniz Meyhane</div><div class="ds-author-co">// Restoran &amp; Eğlence</div></div></div></div>
    <div class="ds-testi-card"><div class="ds-stars">★★★★★</div><div class="ds-testi-text">"Otelimizin tanıtımı için hem video hem sosyal medya konusunda mükemmel iş çıkardılar. Rezervasyonlarımız arttı."</div><div class="ds-testi-author"><div class="ds-avatar">T</div><div><div class="ds-author-name">Tonoz Hotel</div><div class="ds-author-co">// Konaklama &amp; Turizm</div></div></div></div>
    <div class="ds-testi-card"><div class="ds-stars">★★★★★</div><div class="ds-testi-text">"Kurumsal kimliğimizi sıfırdan inşa ettiler. Hedef kitlemize profesyonel bir marka imajı yansıtmamıza yardımcı oldular."</div><div class="ds-testi-author"><div class="ds-avatar">M</div><div><div class="ds-author-name">Makri Travel</div><div class="ds-author-co">// Turizm &amp; Seyahat</div></div></div></div>
  </div>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="ds-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<section class="ds-section dim" id="galeri">
  <div class="ds-sec-hdr">
    <div class="ds-tag">Portföy</div>
    <h2 class="ds-heading">Çalışmalarımızdan<br><span class="stroke">Seçkiler</span></h2>
    <p class="ds-lead">Ürettiğimiz içerik ve projelerden bir seçki.</p>
  </div>
""", unsafe_allow_html=True)

filtre = st.selectbox("İçerik Filtrele", ["Tüm İçerikler", "Yalnızca Görseller", "Yalnızca Videolar"], key="gallery_filter")
medya_klasoru = "medya"
if os.path.exists(medya_klasoru):
    dosyalar  = os.listdir(medya_klasoru)
    gorseller = [f for f in dosyalar if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    videolar  = [f for f in dosyalar if f.lower().endswith(".mp4")]
    if filtre == "Tüm İçerikler":
        g, v = gorseller, videolar
    elif filtre == "Yalnızca Görseller":
        g, v = gorseller, []
    else:
        g, v = [], videolar
    if g:
        cols = st.columns(3)
        for i, gorsel in enumerate(g):
            with cols[i % 3]:
                st.image(os.path.join(medya_klasoru, gorsel), use_column_width=True)
    if v:
        for video in v:
            with open(os.path.join(medya_klasoru, video), "rb") as vf:
                st.video(vf.read())
    if not g and not v:
        st.info("Bu kategoride içerik bulunmuyor.")
else:
    st.info("Medya klasörü henüz eklenmemiş.")

st.markdown("</section>", unsafe_allow_html=True)
st.markdown('<div class="ds-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<section class="ds-section" id="iletisim">
  <div class="ds-sec-hdr">
    <div class="ds-tag">İletişim</div>
    <h2 class="ds-heading">Projenizi<br><span class="grad">Hayata Geçirelim</span></h2>
    <p class="ds-lead">Formu doldurun, en kısa sürede size dönelim.</p>
  </div>
  <div class="ds-contact-wrap">
    <div>
      <div class="ds-contact-item"><div class="ds-ci-icon">📧</div><div><div class="ds-ci-label">E-posta</div><div class="ds-ci-val">deltajanss0@gmail.com</div></div></div>
      <div class="ds-contact-item"><div class="ds-ci-icon">📍</div><div><div class="ds-ci-label">Konum</div><div class="ds-ci-val">Türkiye</div></div></div>
      <div class="ds-contact-item"><div class="ds-ci-icon">🕐</div><div><div class="ds-ci-label">Yanıt Süresi</div><div class="ds-ci-val">24 saat içinde</div></div></div>
    </div>
    <div>
""", unsafe_allow_html=True)

with st.form("iletisim_formu"):
    isim   = st.text_input("İsim / Kurum", placeholder="Örn: Caffoine Café")
    eposta = st.text_input("E-posta Adresiniz", placeholder="ornek@email.com")
    mesaj  = st.text_area("Proje Detayları", placeholder="Markanız hakkında bilgi verin...", height=160)
    gonder = st.form_submit_button("Teklif İste →")
    if gonder:
        if not isim or not eposta or not mesaj:
            st.error("Lütfen tüm alanları doldurun.")
        else:
            with st.spinner("Mesajınız iletiliyor..."):
                sonuc = send_email(isim, eposta, mesaj)
            if sonuc is True:
                st.success("Mesajınız başarıyla iletildi!")
            else:
                st.error(f"Hata: {sonuc}")

st.markdown("</div></div></section>", unsafe_allow_html=True)

st.markdown("""
<div class="ds-divider"></div>
<footer class="ds-footer">
  <div class="ds-footer-grid">
    <div>
      <div class="ds-footer-logo">DELTA <em>STUDIO</em></div>
      <div class="ds-footer-desc">Yaratıcı düşünce ve teknolojinin kesişiminde konumlanan Delta Studio, markaların dijital dünyada güçlü bir iz bırakmasına yardımcı olur.</div>
      <div class="ds-socials">
        <a href="https://www.instagram.com/deltastudio.tr/" target="_blank" class="ds-social">📷</a>
        <a href="https://www.youtube.com/@deltastudio" target="_blank" class="ds-social">▶</a>
        <a href="https://www.facebook.com/deltastudio.tr/" target="_blank" class="ds-social">f</a>
      </div>
    </div>
    <div class="ds-footer-col"><h5>Hizmetler</h5><div class="ds-footer-links"><a href="#hizmetler">Sosyal Medya</a><a href="#hizmetler">Özel Yazılım</a><a href="#hizmetler">Kurumsal Kimlik</a><a href="#hizmetler">Pazarlama</a><a href="#hizmetler">Video</a></div></div>
    <div class="ds-footer-col"><h5>Şirket</h5><div class="ds-footer-links"><a href="#hero">Hakkımızda</a><a href="#hikayeler">Başarı Hikayeleri</a><a href="#yorumlar">Referanslar</a><a href="#galeri">Galeri</a></div></div>
    <div class="ds-footer-col"><h5>İletişim</h5><div class="ds-footer-links"><a href="#iletisim">Teklif Al</a><a href="mailto:deltajanss0@gmail.com">E-posta Gönder</a></div></div>
  </div>
  <div class="ds-footer-bottom">
    <div class="ds-copy">© 2025 Delta Studio. Tüm hakları saklıdır.</div>
    <div class="ds-status">Aktif &amp; Proje Kabul Ediyor</div>
  </div>
</footer>
""", unsafe_allow_html=True)

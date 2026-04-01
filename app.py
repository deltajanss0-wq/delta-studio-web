import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit.components.v1 as components

# 1. Sayfa Ayarları
st.set_page_config(page_title="Delta Studio | Yaratıcı ve Dijital Çözümler", layout="wide", page_icon="🎬")

# 2. Özel CSS: Mirket Agency Mimarisi, Modern Layout, Tipografi ve MOBİL UYUM (Responsive)
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800;900&display=swap');
    
    /* Genel Ayarlar */
    .stApp { background-color: #050505; font-family: 'Montserrat', sans-serif; color: #fff; }
    
    /* Streamlit Varsayılanlarını Gizle */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 1rem !important; max-width: 1300px; }
    
    /* Navigasyon Barı */
    .navbar { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid #1a1a1a; margin-bottom: 60px; }
    .nav-logo h2 { margin:0; font-size:28px !important; letter-spacing: 2px; font-weight: 900 !important; }
    .nav-links { display: flex; gap: 35px; align-items: center; }
    .nav-links a { color: #fff; text-decoration: none; font-weight: 600; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; transition: 0.3s; }
    .nav-links a:hover { color: #E31B23; }
    .btn-teklif { background-color: #E31B23; color: #fff !important; padding: 12px 28px; border-radius: 50px; font-weight: 800 !important; transition: 0.3s; }
    .btn-teklif:hover { background-color: #b3151b; transform: scale(1.05); }

    /* Hero Section (Açılış Ekranı) */
    .hero { padding: 40px 0 100px 0; }
    .hero h1 { font-size: 70px !important; font-weight: 900 !important; line-height: 1.1 !important; margin-bottom: 25px !important; letter-spacing: -2px; }
    .hero p { font-size: 20px; color: #aaa; max-width: 650px; line-height: 1.6; margin-bottom: 40px; }
    
    /* Bölüm Başlıkları */
    .sec-tag { color: #E31B23; font-weight: 800; font-size: 15px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 5px; display: block; }
    .sec-title { font-size: 45px !important; font-weight: 900 !important; margin-top: 0 !important; margin-bottom: 50px !important; }

    /* Hizmet Kartları */
    .service-card { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 15px; padding: 40px 30px; transition: 0.4s ease; height: 100%; display: flex; flex-direction: column; justify-content: space-between;}
    .service-card:hover { border-color: #E31B23; transform: translateY(-10px); box-shadow: 0 15px 30px rgba(227,27,35,0.15); }
    .service-card i { font-size: 40px; color: #E31B23; margin-bottom: 25px; }
    .service-card h3 { font-size: 22px !important; margin-bottom: 15px !important; font-weight: 800 !important;}
    .service-card p { font-size: 15px; color: #888; margin-bottom: 30px; line-height: 1.6; font-family: 'Century Gothic', sans-serif;}
    .service-link { color: #fff; text-decoration: none; font-weight: 700; font-size: 14px; border-bottom: 2px solid #E31B23; padding-bottom: 3px; align-self: flex-start; transition: 0.3s;}
    .service-link:hover { color: #E31B23; }

    /* Başarı Hikayeleri */
    .story-card { background: #0a0a0a; border-left: 5px solid #E31B23; border-radius: 10px; padding: 35px; margin-bottom: 25px; border-top: 1px solid #1a1a1a; border-right: 1px solid #1a1a1a; border-bottom: 1px solid #1a1a1a; transition: 0.3s;}
    .story-card:hover { transform: translateX(10px); background: #111; }
    .story-card h3 { font-size: 26px !important; margin-bottom: 10px !important; font-weight: 800 !important;}
    .story-metric { color: #E31B23; font-weight: 800; font-size: 18px; margin-bottom: 15px; display: block; }
    
    /* Müşteri Yorumları */
    .testimonial-box { background: #0f0f0f; padding: 40px; border-radius: 20px; font-style: italic; position: relative; border: 1px solid #1a1a1a; height: 100%; font-family: 'Century Gothic', sans-serif;}
    .testimonial-box::before { content: '"'; font-size: 80px; color: #E31B23; position: absolute; top: 10px; left: 20px; font-family: Georgia, serif; opacity: 0.3; }
    .testimonial-text { font-size: 16px; color: #ccc; position: relative; z-index: 1; margin-bottom: 25px; line-height: 1.7;}
    .testimonial-author { font-weight: 800; color: #fff; font-style: normal; font-size: 16px; font-family: 'Montserrat', sans-serif;}
    .testimonial-company { color: #E31B23; font-size: 14px; font-style: normal; font-weight: 600; font-family: 'Montserrat', sans-serif;}

    /* Medya Galerisi */
    .media-container { background-color: #0a0a0a; padding: 5px; border-radius: 12px; border: 1px solid #1a1a1a; margin-bottom: 15px; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.4s; }
    .media-container:hover { border-color: #E31B23; transform: translateY(-8px); box-shadow: 0 12px 25px rgba(227, 27, 35, 0.25); }

    /* Form Input */
    .stTextInput input, .stTextArea textarea { background-color: #0f0f0f !important; color: #fff !important; border: 1px solid #222 !important; border-radius: 10px !important; padding: 18px !important; font-size: 16px !important; font-family: 'Century Gothic', sans-serif;}
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: #E31B23 !important; }
    div[data-testid="stFormSubmitButton"] > button { background: #E31B23 !important; color: white !important; border: none !important; border-radius: 50px !important; padding: 15px 30px !important; font-weight: 800 !important; width: 100%; text-transform: uppercase; font-size: 18px !important; transition: 0.3s !important; }
    div[data-testid="stFormSubmitButton"] > button:hover { background: #b3151b !important; transform: translateY(-3px) !important; box-shadow: 0 10px 20px rgba(227,27,35,0.3) !important;}

    /* Mega Footer */
    .mega-footer { background: #050505; border-top: 1px solid #1a1a1a; padding: 80px 0 30px 0; margin-top: 100px; }
    .footer-col h4 { color: #fff; font-size: 18px !important; font-weight: 800 !important; margin-bottom: 25px !important; }
    .footer-list { list-style: none; padding: 0; margin: 0; }
    .footer-list li { margin-bottom: 15px; }
    .footer-list a { color: #777; text-decoration: none; font-size: 15px; transition: 0.3s; font-weight: 500; font-family: 'Century Gothic', sans-serif;}
    .footer-list a:hover { color: #E31B23; padding-left: 8px; }
    .social-icons a { color: #fff; font-size: 20px; margin-right: 15px; background: #1a1a1a; width: 40px; height: 40px; display: inline-flex; justify-content: center; align-items: center; border-radius: 50%; transition: 0.3s; }
    .social-icons a:hover { background: #E31B23; transform: translateY(-3px); }
    .footer-bottom { text-align: center; border-top: 1px solid #1a1a1a; margin-top: 60px; padding-top: 25px; color: #555; font-size: 14px; font-family: 'Century Gothic', sans-serif;}
    
    .footer-flex-container { display: flex; flex-wrap: wrap; justify-content: space-between; max-width: 1200px; margin: 0 auto; padding: 0 20px; }

    /* =====================================================================
       MOBİL UYUM (RESPONSIVE) KALKANI - 768px Altı Ekranlar İçin Daralma 
       ===================================================================== */
    @media (max-width: 768px) {
        .navbar { flex-direction: column; gap: 20px; text-align: center; padding: 15px 0; margin-bottom: 30px;}
        .nav-links { flex-wrap: wrap; justify-content: center; gap: 15px; }
        .nav-links a { font-size: 13px; }
        .btn-teklif { padding: 10px 20px; font-size: 13px; }
        .hero { padding: 20px 0 50px 0; text-align: center; }
        .hero h1 { font-size: 40px !important; line-height: 1.2 !important; margin-bottom: 15px !important; letter-spacing: -1px; }
        .hero p { font-size: 16px !important; margin: 0 auto 30px auto; }
        .sec-title { font-size: 32px !important; margin-bottom: 30px !important; text-align: center; }
        .sec-tag { text-align: center; }
        .service-card { padding: 25px 20px; }
        .service-card h3 { font-size: 20px !important; }
        .service-card p { font-size: 14px; }
        .service-card i { font-size: 30px; margin-bottom: 15px; }
        .story-card { padding: 20px; }
        .story-card h3 { font-size: 20px !important; }
        .story-metric { font-size: 15px; }
        .testimonial-box { padding: 25px; text-align: center; }
        .testimonial-box::before { left: 50%; transform: translateX(-50%); top: -10px; font-size: 60px; }
        .testimonial-text { font-size: 14px; margin-top: 20px;}
        .mega-footer { padding: 50px 0 20px 0; margin-top: 50px; text-align: center; }
        .footer-flex-container { flex-direction: column; align-items: center; }
        .footer-col { margin-bottom: 40px !important; min-width: 100% !important; }
        .social-icons { justify-content: center; }
    }
</style>
""", unsafe_allow_html=True)

# ---- MAİL GÖNDERME FONKSİYONU ----
def send_email(isim, eposta, mesaj):
    gonderici_email = "deltajanss0@gmail.com"
    alici_email = "deltajanss0@gmail.com"
    sifre = "orputhixhpumhuzf" 
    msg = MIMEMultipart()
    msg['From'] = gonderici_email
    msg['To'] = alici_email
    msg['Subject'] = f"Delta Studio Web: Yeni Proje Talebi - {isim}"
    body = f"Web sitesinden yeni bir mesaj aldınız.\n\nİsim / Kurum: {isim}\nİletişim E-postası: {eposta}\n\nMesaj Detayı:\n{mesaj}"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gonderici_email, sifre)
        text = msg.as_string()
        server.sendmail(gonderici_email, alici_email, text)
        server.quit()
        return True
    except Exception as e:
        return str(e)

# ----------------------------------------------------
# 1. NAVBAR (HEADER)
# ----------------------------------------------------
st.markdown("""
<div class="navbar">
<div class="nav-logo">
<h2>DELTA STUDIO</h2>
</div>
<div class="nav-links">
<a href="#hizmetler">Hizmetler</a>
<a href="#hikayeler">Hikayeler</a>
<a href="#galeri">Galeri</a>
<a href="#iletisim" class="btn-teklif">Teklif İste</a>
</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. HERO SECTION
# ----------------------------------------------------
col_logo, col_text = st.columns([1, 4])
with col_logo:
    try:
        st.image("logo.png", width=160)
    except:
        pass

with col_text:
    st.markdown("""
    <div class="hero">
    <h1>Markanızın Dijital<br><span style="color:#E31B23;">Sesini Yükseltin.</span></h1>
    <p>Hedef kitlenizde yankı uyandıracak, etkileyici ve sonuç odaklı pazarlama çözümlerimizle markanızı zirveye taşıyoruz. Vizyonunuzu gerçeğe dönüştürmek için doğru yerdesiniz.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ----------------------------------------------------
# 3. HİZMETLER (MİRKET STYLE GRID)
# ----------------------------------------------------
st.markdown("<div id='hizmetler'></div>", unsafe_allow_html=True)
st.markdown("<span class='sec-tag'>#DELTA HİZMETLER</span><h2 class='sec-title'>Kreatif Çözümler</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="service-card">
    <div>
    <i class="fa-solid fa-hashtag"></i>
    <h3>Sosyal Medya Yönetimi</h3>
    <p>Ruha dokunan ve ilham veren vizyonunuzu sosyal medya platformlarına yansıtıyoruz. Yaratıcı stratejilerle markanızı zirveye taşıyoruz.</p>
    </div>
    <a href="#iletisim" class="service-link">İncele <i class="fa-solid fa-arrow-right" style="font-size:12px; margin-left:5px; margin-bottom:0; display:inline;"></i></a>
    </div>
    """, unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="service-card">
    <div>
    <i class="fa-solid fa-code"></i>
    <h3>Özel Yazılım & Yasopanel</h3>
    <p>Python tabanlı özel yönetim panelleriyle seyahat acentelerinin ve işletmelerin dijital otomasyon süreçlerini kusursuzlaştırıyoruz.</p>
    </div>
    <a href="#iletisim" class="service-link">İncele <i class="fa-solid fa-arrow-right" style="font-size:12px; margin-left:5px; margin-bottom:0; display:inline;"></i></a>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="service-card">
    <div>
    <i class="fa-solid fa-pen-nib"></i>
    <h3>Kurumsal Kimlik Tasarımı</h3>
    <p>Logo, menü, tabela ve dijital şablonlara kadar her detayda markanızın hikayesini anlatıyor, kurumsal algınızı güçlendiriyoruz.</p>
    </div>
    <a href="#iletisim" class="service-link">İncele <i class="fa-solid fa-arrow-right" style="font-size:12px; margin-left:5px; margin-bottom:0; display:inline;"></i></a>
    </div>
    """, unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="service-card">
    <div>
    <i class="fa-solid fa-bullseye"></i>
    <h3>Stratejik Pazarlama</h3>
    <p>Dijital dünyada hedef odaklı reklam kurguları ile markanızı daha görünür hale getiriyor, bütçenizi en verimli şekilde kullanıyoruz.</p>
    </div>
    <a href="#iletisim" class="service-link">İncele <i class="fa-solid fa-arrow-right" style="font-size:12px; margin-left:5px; margin-bottom:0; display:inline;"></i></a>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="service-card">
    <div>
    <i class="fa-solid fa-video"></i>
    <h3>Video Prodüksiyon</h3>
    <p>YouTube, Reels ve reklam filmleri için global standartlarda kurgu. Etkileyici geçişler ve profesyonel color grading ile sinematik işler.</p>
    </div>
    <a href="#iletisim" class="service-link">İncele <i class="fa-solid fa-arrow-right" style="font-size:12px; margin-left:5px; margin-bottom:0; display:inline;"></i></a>
    </div>
    """, unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="service-card">
    <div>
    <i class="fa-solid fa-wand-magic-sparkles"></i>
    <h3>Kreatif İçerik Üretimi</h3>
    <p>Farklı mecralara özel konsept metinler, tasarımlar ve hedef kitleyi harekete geçirecek sanatsal bir dijital bakış açısı sunuyoruz.</p>
    </div>
    <a href="#iletisim" class="service-link">İncele <i class="fa-solid fa-arrow-right" style="font-size:12px; margin-left:5px; margin-bottom:0; display:inline;"></i></a>
    </div>
    """, unsafe_allow_html=True)

st.write("<br><br><br>", unsafe_allow_html=True)

# ----------------------------------------------------
# 4. BAŞARI HİKAYELERİ (MİRKET STYLE)
# ----------------------------------------------------
st.markdown("<div id='hikayeler'></div>", unsafe_allow_html=True)
st.markdown("<span class='sec-tag'>#VAKA ANALİZLERİ</span><h2 class='sec-title'>Senfonilerdeki Başarımız</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="story-card">
<span class="story-metric">Caffoine'in Sıfırdan %45 Etkileşim Artışı Hikayesi</span>
<h3>Marka Mimarisi: Caffoine</h3>
<p style="color:#aaa; font-family: 'Century Gothic', sans-serif;">Sıfırdan bir kahve kültürü yaratmak... Logo tasarımından kurumsal kimliğe, sosyal medya lansmanından iç mekan görsel stratejisine kadar markanın sosyal medya etkileşimi hızla artarken, dijital dünyada dev bir yankı uyandırdı.</p>
</div>
<div class="story-card">
<span class="story-metric">Operasyonel Süreçlerde %60 Hızlanma Getirdi</span>
<h3>Teknoloji: Yasopanel Yazılımı</h3>
<p style="color:#aaa; font-family: 'Century Gothic', sans-serif;">Python tabanlı özel yönetim panelleriyle seyahat acenteleri dijitalde büyük bir başarıya imza attı. Yeniden tasarlanan altyapı, firmaların operasyonel iş yükünü hafifleterek satış grafiklerini zirveye taşıdı.</p>
</div>
""", unsafe_allow_html=True)

st.write("<br><br><br>", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. MÜŞTERİ YORUMLARI (TESTIMONIALS)
# ----------------------------------------------------
st.markdown("<span class='sec-tag'>#REFERANSLAR</span><h2 class='sec-title'>Ne Dediler?</h2>", unsafe_allow_html=True)

t1, t2, t3 = st.columns(3)
with t1:
    st.markdown("""
    <div class="testimonial-box">
    <p class="testimonial-text">Sosyal medya yönetimimizi Delta ekibine emanet etmek, verdiğimiz en doğru kararlardan biriydi. Kendi ekibimizden biriymiş gibi gösterdikleri özveri için teşekkür ederiz.</p>
    <div class="testimonial-author">Keyf-i Deniz Meyhane</div>
    <div class="testimonial-company">Yönetim Ekibi</div>
    </div>
    """, unsafe_allow_html=True)
with t2:
    st.markdown("""
    <div class="testimonial-box">
    <p class="testimonial-text">Sosyal medya ölçümlerimiz fırladı! Delta Studio ekibi dijital ortamı gerçekten anlıyor ve markamızı hayata geçirdi.</p>
    <div class="testimonial-author">Tonoz Hotel</div>
    <div class="testimonial-company">Pazarlama Departmanı</div>
    </div>
    """, unsafe_allow_html=True)
with t3:
    st.markdown("""
    <div class="testimonial-box">
    <p class="testimonial-text">Delta ile işbirliğimizde, operasyonel ve dijital süreçlerimizdeki başarının mimarı oldular. Stratejik bakış açıları muazzam.</p>
    <div class="testimonial-author">Makri Travel</div>
    <div class="testimonial-company">Yönetim Kurulu</div>
    </div>
    """, unsafe_allow_html=True)

st.write("<br><br><br>", unsafe_allow_html=True)

# ----------------------------------------------------
# 6. INSTAGRAM LIVE FEED
# ----------------------------------------------------
st.markdown("<div id='galeri'></div>", unsafe_allow_html=True)
st.markdown("<span class='sec-tag'>#BE A SOCIAL!</span><h2 class='sec-title'>Instagram'da Biz</h2>", unsafe_allow_html=True)

ig_col_left, ig_col_main, ig_col_right = st.columns([1, 2, 1])
ig_base_code = """
<blockquote class="instagram-media" data-instgrm-permalink="https://www.instagram.com/thestudiodelta/" data-instgrm-version="14" style=" background:#0d0d0d; border:1px solid #1a1a1a; border-radius:15px; box-shadow:0 0 10px rgba(0,0,0,0.5); margin: 1px; max-width:540px; min-width:326px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);">
<div style="padding:16px; text-align:center;">
<a href="https://www.instagram.com/thestudiodelta/" style=" background:#0d0d0d; line-height:0; padding:0 0; text-align:center; text-decoration:none; width:100%;" target="_blank">
<div style="padding-top: 40px; color:#fff; font-family:Arial; font-size:16px; font-weight:bold;">📸 Delta Studio Instagram İçeriği</div>
<div style="padding-top: 10px; color:#E31B23; font-family:Arial; font-size:14px;">Instagram'da İncele</div>
</a>
</div>
</blockquote>
<script async src="//www.instagram.com/embed.js"></script>
"""
with ig_col_main:
    components.html(ig_base_code, height=450, scrolling=False)

st.write("<br><br><br>", unsafe_allow_html=True)

# ----------------------------------------------------
# 7. MEDYA PORTFÖYÜ (DİNAMİK GALERİ)
# ----------------------------------------------------
st.markdown("<span class='sec-tag'>#PORTFÖY</span><h2 class='sec-title'>Medya Portföyü</h2>", unsafe_allow_html=True)
st.markdown("<p style='font-size:15px; color:#888; font-family: Century Gothic, sans-serif;'>Detaylı incelemek istediğiniz görselin sağ üst köşesindeki ikona tıklayarak tam ekran yapabilirsiniz.</p>", unsafe_allow_html=True)

medya_klasoru = "medya"

if not os.path.exists(medya_klasoru):
    os.makedirs(medya_klasoru)
    st.info("Sistem 'medya' adlı bir klasör oluşturdu. Lütfen tasarımlarınızı bu klasörün içine atıp sayfayı yenileyin.")
else:
    tum_dosyalar = [f for f in os.listdir(medya_klasoru) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4'))]
    
    if not tum_dosyalar:
        st.warning("'medya' klasörünüz şu an boş. Post ve Story tasarımlarınızı klasöre eklediğinizde burada otomatik görünecekler.")
    else:
        kategori = st.radio("Filtre:", ["Tüm İçerikler", "Sadece Görseller", "Sadece Videolar"], horizontal=True)
        st.write("---")
        
        gosterilecek_dosyalar = []
        for dosya in tum_dosyalar:
            if kategori == "Sadece Görseller" and dosya.lower().endswith(('.png', '.jpg', '.jpeg')):
                gosterilecek_dosyalar.append(dosya)
            elif kategori == "Sadece Videolar" and dosya.lower().endswith('.mp4'):
                gosterilecek_dosyalar.append(dosya)
            elif kategori == "Tüm İçerikler":
                gosterilecek_dosyalar.append(dosya)

        if not gosterilecek_dosyalar:
            st.info("Bu kategoride henüz bir tasarım bulunmuyor.")
        else:
            cols = st.columns(4) 
            for i, dosya in enumerate(gosterilecek_dosyalar):
                dosya_yolu = os.path.join(medya_klasoru, dosya)
                with cols[i % 4]:
                    st.markdown("<div class='media-container'>", unsafe_allow_html=True)
                    if dosya.lower().endswith('.mp4'):
                        st.video(dosya_yolu)
                    else:
                        st.image(dosya_yolu, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

st.write("<br><br><br>", unsafe_allow_html=True)

# ----------------------------------------------------
# 8. TEKLİF İSTE (CONTACT FORM)
# ----------------------------------------------------
st.markdown("<div id='iletisim'></div>", unsafe_allow_html=True)
st.markdown("<span class='sec-tag'>#İLETİŞİM</span><h2 class='sec-title'>Dijital Geleceğinizi Beraber Yazalım</h2>", unsafe_allow_html=True)

with st.form("contact_form", clear_on_submit=False):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        input_isim = st.text_input("Adınız Soyadınız / Markanız")
    with col_f2:
        input_email = st.text_input("E-posta Adresiniz")
        
    input_mesaj = st.text_area("Proje Detayları ve Hedefleriniz", height=150)
    
    submit_btn = st.form_submit_button("TEKLİF İSTE")
    
    if submit_btn:
        if not input_isim or not input_email or not input_mesaj:
            st.warning("Lütfen tüm alanları doldurunuz.")
        else:
            with st.spinner("Talebiniz uzman ekibimize iletiliyor..."):
                sonuc = send_email(input_isim, input_email, input_mesaj)
                if sonuc is True:
                    st.success("Talebiniz başarıyla ulaştı. Strateji ekibimiz en kısa sürede sizinle iletişime geçecektir.")
                else:
                    st.error(f"Sistem Hatası: {sonuc}")


# ----------------------------------------------------
# 9. MEGA FOOTER (MİRKET STYLE)
# ----------------------------------------------------
st.markdown("""
<div class="mega-footer">
<div class="footer-flex-container">
<div style="flex: 1; min-width: 250px; margin-bottom: 30px;">
<h2 style="margin:0; font-size:24px !important; margin-bottom: 20px !important;">DELTA STUDIO</h2>
<p style="font-size: 14px; max-width: 80%; font-family: 'Century Gothic', sans-serif;">Delta Studio, markanızın dijital varlığını güçlendiren yaratıcı bir sosyal medya ve dijital çözüm ajansı olarak hizmet vermektedir.</p>
<div class="social-icons" style="margin-top: 20px;">
<a href="https://www.instagram.com/thestudiodelta/" target="_blank"><i class="fa-brands fa-instagram"></i></a>
<a href="https://www.youtube.com/@DeltaAjanss" target="_blank"><i class="fa-brands fa-youtube"></i></a>
<a href="https://www.facebook.com/profile.php?id=61586644564480" target="_blank"><i class="fa-brands fa-facebook-f"></i></a>
</div>
</div>
<div style="flex: 1; min-width: 200px; margin-bottom: 30px;" class="footer-col">
<h4>Bizi Tanıyın</h4>
<ul class="footer-list">
<li><a href="#hizmetler">Biz Kimiz?</a></li>
<li><a href="#hikayeler">Başarı Hikayeleri</a></li>
<li><a href="#galeri">Medya Portföyü</a></li>
<li><a href="#iletisim">Teklif İste</a></li>
</ul>
</div>
<div style="flex: 1; min-width: 200px; margin-bottom: 30px;" class="footer-col">
<h4>Hizmetlerimiz</h4>
<ul class="footer-list">
<li><a href="#hizmetler">Sosyal Medya Yönetimi</a></li>
<li><a href="#hizmetler">Kurumsal Kimlik Tasarımı</a></li>
<li><a href="#hizmetler">Video Prodüksiyon</a></li>
<li><a href="#hizmetler">Özel Yazılım Çözümleri</a></li>
</ul>
</div>
<div style="flex: 1; min-width: 200px; margin-bottom: 30px;" class="footer-col">
<h4>İletişim Bilgileri</h4>
<ul class="footer-list">
<li><a href="mailto:deltajanss0@gmail.com"><i class="fa-regular fa-envelope" style="margin-right: 10px; color:#E31B23;"></i> deltajanss0@gmail.com</a></li>
<li><a href="#"><i class="fa-solid fa-location-dot" style="margin-right: 10px; color:#E31B23;"></i> Fethiye, Muğla / Türkiye</a></li>
</ul>
</div>
</div>
<div class="footer-bottom">
<p style="margin: 0; font-size:13px;">© 2026 Delta Studio. Yaratıcı ve Dijital Çözümler. Tüm Hakları Saklıdır.</p>
</div>
</div>
""", unsafe_allow_html=True)

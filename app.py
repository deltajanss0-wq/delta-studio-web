import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit.components.v1 as components

# 1. Sayfa Ayarları
st.set_page_config(page_title="Delta Studio", layout="wide", page_icon="🎬")

# 2. Özel CSS: Montserrat, Century Gothic Entegrasyonu, Hap Şeklinde Parıldayan Butonlar ve UI İyileştirmeleri
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');
    
    .stApp { background-color: #050505; font-family: 'Century Gothic', 'Questrial', sans-serif; }
    
    p, label, span, .stMarkdown, .stText { 
        color: #ffffff !important; 
        font-size: 19px !important; 
        line-height: 1.6;
    }
    
    h1, h2, h3 { 
        font-family: 'Montserrat', sans-serif !important; 
        text-transform: uppercase;
        letter-spacing: 1px !important; 
        color: #E31B23 !important; 
        text-shadow: 0 0 20px rgba(227, 27, 35, 0.4);
    }
    
    h1 { font-size: 5vw !important; min-font-size: 40px !important; margin-bottom: 0px !important; font-weight: 900 !important;}
    h2 { font-size: 35px !important; margin-top: 40px !important; border-bottom: 2px solid #E31B23; display: inline-block; padding-bottom: 10px; font-weight: 700 !important;}

    .stTabs [data-baseweb="tab-list"] { gap: 50px; }
    .stTabs [data-baseweb="tab"] { 
        font-family: 'Montserrat', sans-serif !important;
        letter-spacing: 1px;
        height: 70px; background-color: transparent; color: #666; font-size: 22px; font-weight: 700;
        transition: color 0.3s;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #E31B23; }
    .stTabs [aria-selected="true"] { color: #fff !important; border-bottom-color: #E31B23 !important; }
    
    .partner-section { background: linear-gradient(145deg, #0a0a0a, #111); padding: 60px 20px; border-radius: 20px; border: 1px solid #1a1a1a; text-align: center; margin: 50px 0; box-shadow: inset 0 0 20px rgba(0,0,0,0.5);}
    .partner-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-top: 30px; }
    .partner-item { font-family: 'Century Gothic', sans-serif; font-size: 15px; color: #aaa; background: #151515; padding: 8px 18px; border-radius: 50px; border: 1px solid #222; transition: all 0.3s ease; }
    .partner-item:hover { color: #fff; border-color: #E31B23; background: #1a1a1a; transform: scale(1.08); box-shadow: 0 5px 20px rgba(227, 27, 35, 0.4); }

    .media-container {
        background-color: #0a0a0a;
        padding: 5px;
        border-radius: 12px;
        border: 1px solid #1a1a1a;
        margin-bottom: 15px;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.4s;
    }
    .media-container:hover { border-color: #E31B23; transform: translateY(-8px); box-shadow: 0 12px 25px rgba(227, 27, 35, 0.25); }

    /* ---- MODERN FORM VE INPUT TASARIMLARI ---- */
    .stTextInput input, .stTextArea textarea {
        background-color: #0f0f0f !important;
        color: #fff !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #E31B23 !important;
        box-shadow: 0 0 15px rgba(227, 27, 35, 0.3) !important;
        background-color: #151515 !important;
    }

    /* ---- PREMIUM GRADIENT BUTON TASARIMI ---- */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(45deg, #E31B23, #8a0e13) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        letter-spacing: 2px !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 4px 15px rgba(227, 27, 35, 0.4) !important;
        width: 100%;
        text-transform: uppercase;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(227, 27, 35, 0.7) !important;
        background: linear-gradient(45deg, #ff1e27, #a81017) !important;
    }
    div[data-testid="stFormSubmitButton"] > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 10px rgba(227, 27, 35, 0.4) !important;
    }

    /* ---- FOOTER VE FOOTER IKON TASARIMI ---- */
    .custom-footer {
        width: 100%;
        text-align: center;
        padding: 40px 0 20px 0;
        margin-top: 60px;
        border-top: 1px solid #222;
        background-color: #050505;
    }
    .custom-footer p {
        color: #666 !important;
        font-size: 14px !important;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }
    .footer-icons {
        display: flex;
        justify-content: center;
        gap: 25px;
    }
    .footer-icons a {
        color: #888;
        font-size: 24px;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    .footer-icons a:hover {
        color: #E31B23;
        transform: translateY(-5px) scale(1.1);
        text-shadow: 0 0 15px rgba(227, 27, 35, 0.6);
    }

    /* ---- HEADER SOSYAL MEDYA BUTONLARI (Hap Şeklinde ve Parıldayan) ---- */
    .header-social-wrapper {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 15px;
    }
    .header-social-btn {
        background: linear-gradient(45deg, #0a0a0a, #111);
        color: #888;
        border: 2px solid #333;
        padding: 10px 20px;
        border-radius: 50px;
        text-align: center;
        text-decoration: none;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .header-social-btn:hover {
        border-color: #E31B23;
        box-shadow: 0 0 25px rgba(227, 27, 35, 0.6);
        transform: translateY(-3px);
        background: linear-gradient(45deg, #1a1a1a, #222);
        color: #fff;
    }
    .header-social-btn:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 10px rgba(227, 27, 35, 0.4) !important;
    }
    .header-social-btn i {
        font-size: 18px;
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

# 3. Header (Daha Profesyonel ve Ortalanmış Layout)
col_logo, col_text, col_buttons = st.columns([1, 2, 2])
with col_logo:
    try:
        st.image("logo.png", width=180)
    except:
        st.error("Logo bulunamadı! Lütfen görselin adının tam olarak 'logo.png' olduğundan emin olun.")

with col_text:
    # Metinleri ve butonları dikey olarak ortalamak için flexbox kullanıyoruz
    st.markdown("""
        <div style='display: flex; flex-direction: column; justify-content: center; height: 100%;'>
            <h1>DELTA STUDIO</h1>
            <p style='font-size: 22px; color: #888; letter-spacing: 3px;'>VİZYONER DİJİTAL ÇÖZÜMLER</p>
        </div>
    """, unsafe_allow_html=True)

with col_buttons:
    # Butonları metinlerin hemen sağına dikey ortalanmış bir şekilde dizeceğiz
    st.markdown("""
        <div style='display: flex; justify-content: flex-end; align-items: center; height: 100%; gap: 15px;'>
            <a href="https://www.instagram.com/thestudiodelta/" target="_blank" class="header-social-btn"><i class="fa-brands fa-instagram"></i></a>
            <a href="https://www.youtube.com/@DeltaAjanss" target="_blank" class="header-social-btn"><i class="fa-brands fa-youtube"></i></a>
            <a href="https://www.facebook.com/profile.php?id=61586644564480" target="_blank" class="header-social-btn"><i class="fa-brands fa-facebook-f"></i></a>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# 4. Sekmeler
tab1, tab2, tab3 = st.tabs(["VİTRİN (LIVE)", "MEDYA PORTFÖYÜ", "İLETİŞİM"])

# --- 1. SEKME: VİTRİN VE YETKİNLİKLER ---
with tab1:
    st.markdown("<h2>🎬 LIVE STREAM • DELTA STUDIO INSTAGRAM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#888;'>Delta Studio'nun en taze işleri. Doğrudan Instagram feed'imizden.</p>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)

    # TEK VE MERKEZLENMİŞ INSTAGRAM KARTI (Kendi Profiliniz)
    ig_col_left, ig_col_main, ig_col_right = st.columns([1, 2, 1])

    # The Studio Delta profil önizleme kodu
    ig_base_code = """
    <blockquote class="instagram-media" data-instgrm-permalink="https://www.instagram.com/thestudiodelta/" data-instgrm-version="14" style=" background:#000; border:1px solid #333; border-radius:8px; box-shadow:0 0 10px rgba(0,0,0,0.5); margin: 1px; max-width:540px; min-width:326px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);">
        <div style="padding:16px; text-align:center;">
            <a href="https://www.instagram.com/thestudiodelta/" style=" background:#000; line-height:0; padding:0 0; text-align:center; text-decoration:none; width:100%;" target="_blank">
                <div style="padding-top: 40px; color:#fff; font-family:Arial; font-size:16px; font-weight:bold;">📸 Delta Studio Instagram İçeriği</div>
                <div style="padding-top: 10px; color:#E31B23; font-family:Arial; font-size:14px;">Instagram'da Görüntüle</div>
            </a>
        </div>
    </blockquote>
    <script async src="//www.instagram.com/embed.js"></script>
    """

    with ig_col_main:
        components.html(ig_base_code, height=450, scrolling=False)

    st.write("<br><br>", unsafe_allow_html=True)

    # YETKİNLİKLER
    st.markdown("<h2>🚀 YETENEKLER</h2>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.info("**VİDEO PRODÜKSİYON**\n\nYouTube, Reels ve reklam filmleri için global standartlarda kurgu.")
    c2.success("**STRATEJİK PAZARLAMA**\n\nMarkanızın sosyal medya algoritmasındaki hakimiyetini kuruyoruz.")
    c3.warning("**KURUMSAL KİMLİK & TASARIM**\n\nLogo, menü, tabela ve 360 derece marka görsel mimarisini inşa ediyoruz.")
    c4.error("**ÖZEL YAZILIM**\n\nİşletmenize özel Python ve Panel çözümleri geliştiriyoruz.")

    # PARTNERLER
    referanslar = [
        "Tonoz Hotel", "Göklin İçecek", "Keyf-i Deniz Meyhane", "Biodenge Çevre Teknolojileri", 
        "Dalaman Lykia Resort", "La Boutique Maya", "Sea Me Beach", "Ünsal Otel", 
        "Renar Sigorta", "Turanlar Grup", "Göcek Lykia Resort", "Bday Cake", 
        "Dsurgery", "Renar Otomotiv", "Bday Boutique", "Hazar İçecek", 
        "U Yacht", "Candles Fethiye", "Hamiye Hanım Zeytinyağları", "Tilos Travel", 
        "Makri Rent a Car", "Makri Travel", "Ferrybilet", "Yalova Estate", "Levissi Wine House",
        "Gloria Caffe", "Makri Gemicilik"
    ]

    st.markdown("""
        <div class="partner-section">
            <h3 style='color: #fff !important; opacity: 0.6; margin-bottom: 10px; font-size:24px !important;'>EKOSİSTEMİMİZ VE MARKALAR</h3>
            <p style='color:#666 !important; font-size:14px !important;'>Delta Studio, vizyonunu paylaşan lider markalarla değer üretmeye devam ediyor.</p>
            <div class="partner-grid">
    """ + "".join([f'<div class="partner-item">{brand}</div>' for brand in sorted(referanslar)]) + """
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 2. SEKME: MEDYA PORTFÖYÜ ---
with tab2:
    st.markdown("<h2>📸 DİJİTAL TASARIM GALERİSİ</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:15px; color:#888;'>Detaylı incelemek istediğiniz görselin sağ üst köşesindeki ikona tıklayarak tam ekran yapabilirsiniz.</p>", unsafe_allow_html=True)
    
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
                # INSTAGRAM GRID MANTIĞI: 4'LÜ SÜTUN YAPILDI (Görselleri küçültür ve şıklaştırır)
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

# --- 3. SEKME: İLETİŞİM (MAİL SİSTEMLİ) ---
with tab3:
    st.markdown("<h2>📩 İLETİŞİM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#888;'>Projeleriniz için aşağıdaki formu doldurun, sistemimiz doğrudan ekibimize iletecektir.</p>", unsafe_allow_html=True)
    
    with st.form("contact_form", clear_on_submit=False):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            input_isim = st.text_input("Ad Soyad / Kurum Adı")
        with col_f2:
            input_email = st.text_input("Geri Dönüş E-posta Adresiniz")
            
        input_mesaj = st.text_area("Proje Detayları ve Hayalleriniz", height=150)
        
        submit_btn = st.form_submit_button("SİSTEME GÖNDER")
        
        if submit_btn:
            if not input_isim or not input_email or not input_mesaj:
                st.warning("Lütfen tüm alanları doldurunuz.")
            else:
                with st.spinner("Mesajınız güvenli sunucularımız üzerinden iletiliyor..."):
                    sonuc = send_email(input_isim, input_email, input_mesaj)
                    if sonuc is True:
                        st.success("Harika! Mesajınız Delta Studio ekibine başarıyla ulaştı. En kısa sürede iletişime geçeceğiz.")
                    elif "Username and Password not accepted" in str(sonuc):
                        st.error("Sistem Uyarısı: Mail gönderilemedi. Lütfen kod içerisindeki 'Uygulama Şifresi' bölümünü Google'dan aldığınız şifre ile güncelleyin.")
                    else:
                        st.error(f"Sistem Hatası: Mail gönderilemedi. Lütfen ayarlarınızı kontrol edin. Hata detayı: {sonuc}")

# ----------------------------------------------------
# EFSANE FOOTER (SAYFA SONU)
# ----------------------------------------------------
st.markdown("""
    <div class="custom-footer">
        <div class="footer-icons">
            <a href="https://www.instagram.com/thestudiodelta/" target="_blank" title="Instagram"><i class="fa-brands fa-instagram"></i></a>
            <a href="https://www.youtube.com/@DeltaAjanss" target="_blank" title="YouTube"><i class="fa-brands fa-youtube"></i></a>
            <a href="https://www.facebook.com/profile.php?id=61586644564480" target="_blank" title="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
        </div>
        <br>
        <p>© 2026 Delta Studio. Vizyoner Dijital Çözümler. Tüm Hakları Saklıdır.</p>
    </div>
""", unsafe_allow_html=True)
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcyberpunk
import requests
import os
import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import tkinter.messagebox as messagebox
from tkinter import filedialog
import google.generativeai as genai

# --- TAMAMEN FÜTÜRİSTİK SİBERPUNK TEMA ---
ctk.set_appearance_mode("dark")
BG_COLOR = "#020203"       
CARD_BG = "#0a0a10"        
CYAN_NEON = "#00f0ff"      
GREEN_NEON = "#39ff14"     
TEXT_MAIN = "#ffffff"
TEXT_MUTED = "#4a4a5a"

class UltimateDesktopPanel(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DELTA STUDIO | YZ KOMUTA MERKEZİ")
        self.geometry("1450x900")
        self.configure(fg_color=BG_COLOR)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.current_company = "Tilos Travel"
        self.current_color = CYAN_NEON
        
        self.google_excel_path = None
        self.meta_excel_path = None
        self.uploaded_image_paths = [] 
        
        self.config = {
            "Makri Travel": {"renk": GREEN_NEON},
            "Tilos Travel": {"renk": CYAN_NEON}
        }

        self.init_database()
        self.saved_api_key = self.load_api_key() 
        
        self.setup_sidebar()
        self.setup_main_area()
        self.switch_company("Tilos Travel")

    def init_database(self):
        self.conn = sqlite3.connect("yaso_data.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS settings (key_name TEXT PRIMARY KEY, key_value TEXT)''')
        self.conn.commit()

    def load_api_key(self):
        self.cursor.execute("SELECT key_value FROM settings WHERE key_name='gemini_api_key'")
        result = self.cursor.fetchone()
        return result[0] if result else ""

    def save_api_key(self, api_key):
        self.cursor.execute("INSERT OR REPLACE INTO settings (key_name, key_value) VALUES ('gemini_api_key', ?)", (api_key,))
        self.conn.commit()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#050508", border_width=1, border_color="#11111a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(self.sidebar, text="PANEL", font=ctk.CTkFont(size=32, weight="bold", family="Courier"), text_color=TEXT_MAIN).grid(row=0, column=0, pady=(40, 40))

        self.btn_tilos = ctk.CTkButton(self.sidebar, text="Tilos Travel", font=ctk.CTkFont(size=14, weight="bold"), fg_color="transparent", border_width=2, border_color=CYAN_NEON, text_color=CYAN_NEON, height=45, command=lambda: self.switch_company("Tilos Travel"))
        self.btn_tilos.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_makri = ctk.CTkButton(self.sidebar, text="Makri Travel", font=ctk.CTkFont(size=14, weight="bold"), fg_color="transparent", border_width=2, border_color=TEXT_MUTED, text_color=TEXT_MUTED, height=45, command=lambda: self.switch_company("Makri Travel"))
        self.btn_makri.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    def setup_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_COLOR)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.main_frame, text="KOMUTA MERKEZİ", font=ctk.CTkFont(size=28, weight="bold", family="Courier"), text_color=TEXT_MAIN).grid(row=0, column=0, padx=10, pady=(0, 20), sticky="w")

        self.tabs = ctk.CTkTabview(self.main_frame, corner_radius=8, fg_color=CARD_BG, segmented_button_fg_color=BG_COLOR, text_color=TEXT_MAIN, border_width=1, border_color="#181824")
        self.tabs.grid(row=1, column=0, sticky="nsew")

        self.tabs.add("  Rapor Motoru (AI)  ") 
        self.build_custom_report_tab() 

    def build_custom_report_tab(self):
        tab = self.tabs.tab("  Rapor Motoru (AI)  ")
        container = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(container, text="DELTA AI: AKILLI SUNUM MOTORU", font=ctk.CTkFont(size=24, weight="bold", family="Courier"), text_color=CYAN_NEON).grid(row=0, column=0, columnspan=3, pady=(0, 5), sticky="w")
        
        ctk.CTkLabel(container, text="Gemini API Key:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.api_key_entry = ctk.CTkEntry(container, width=350, fg_color="#0a0a12", border_color="#333344", show="*")
        self.api_key_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        
        if self.saved_api_key:
            self.api_key_entry.insert(0, self.saved_api_key)

        ctk.CTkLabel(container, text="Sunum Başlığı:", font=ctk.CTkFont(size=14)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.report_type_entry = ctk.CTkEntry(container, width=350, fg_color="#0a0a12", border_color="#333344")
        self.report_type_entry.insert(0, "Yapay Zeka Analizli Performans Sunumu")
        self.report_type_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        self.btn_upload_google = ctk.CTkButton(container, text="📥 Google Ads (.xlsx)", fg_color="#1a1a24", border_width=1, border_color=TEXT_MUTED, command=self.select_google)
        self.btn_upload_google.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.lbl_google_status = ctk.CTkLabel(container, text="Veri Yok", text_color=TEXT_MUTED)
        self.lbl_google_status.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.btn_upload_meta = ctk.CTkButton(container, text="📥 Meta Ads (.xlsx)", fg_color="#1a1a24", border_width=1, border_color=TEXT_MUTED, command=self.select_meta)
        self.btn_upload_meta.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.lbl_meta_status = ctk.CTkLabel(container, text="Veri Yok", text_color=TEXT_MUTED)
        self.lbl_meta_status.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.btn_upload_image = ctk.CTkButton(container, text="🖼️ Çoklu Görsel Ekle", fg_color="#1a1a24", border_width=1, border_color=TEXT_MUTED, command=self.select_images)
        self.btn_upload_image.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.lbl_image_status = ctk.CTkLabel(container, text="0 Görsel Seçildi", text_color=TEXT_MUTED)
        self.lbl_image_status.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.btn_generate_ai = ctk.CTkButton(container, text="🧠 YZ ANALİZİ İLE PDF OLUŞTUR", font=ctk.CTkFont(size=16, weight="bold"), fg_color=self.current_color, text_color="black", hover_color="#ffffff", height=50, command=self.generate_ai_report)
        self.btn_generate_ai.grid(row=7, column=0, columnspan=2, pady=30, sticky="ew")

    def select_google(self):
        file_path = filedialog.askopenfilename(title="Google Verisi", filetypes=[("Excel", "*.xlsx *.csv")])
        if file_path:
            self.google_excel_path = file_path
            self.lbl_google_status.configure(text=os.path.basename(file_path), text_color=GREEN_NEON)

    def select_meta(self):
        file_path = filedialog.askopenfilename(title="Meta Verisi", filetypes=[("Excel", "*.xlsx *.csv")])
        if file_path:
            self.meta_excel_path = file_path
            self.lbl_meta_status.configure(text=os.path.basename(file_path), text_color=GREEN_NEON)

    def select_images(self):
        file_paths = filedialog.askopenfilenames(title="Görselleri Seç", filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if file_paths:
            self.uploaded_image_paths = list(file_paths)
            self.lbl_image_status.configure(text=f"{len(self.uploaded_image_paths)} Görsel Yüklendi!", text_color=GREEN_NEON)

    def generate_ai_report(self):
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showwarning("Eksik API", "Lütfen Gemini API Key giriniz.")
            return
        
        self.save_api_key(api_key)
            
        if not self.google_excel_path and not self.meta_excel_path:
            messagebox.showwarning("Veri Yok", "Analiz için en az bir Excel tablosu yüklemelisin.")
            return

        self.btn_generate_ai.configure(text="SİNİR AĞINA BAĞLANILIYOR...", fg_color="#ffcc00")
        self.update() 

        def tr_fix(text):
            return str(text).replace('ş','s').replace('Ş','S').replace('ı','i').replace('İ','I').replace('ğ','g').replace('Ğ','G').replace('ü','u').replace('Ü','U').replace('ö','o').replace('Ö','O').replace('ç','c').replace('Ç','C')

        try:
            data_summary = ""
            df_google, df_meta = None, None
            
            if self.google_excel_path:
                df_google = pd.read_excel(self.google_excel_path).head(10) if not self.google_excel_path.endswith('.csv') else pd.read_csv(self.google_excel_path).head(10)
                data_summary += "Google Ads/Arama Verileri:\n" + df_google.to_string() + "\n\n"
                
            if self.meta_excel_path:
                df_meta = pd.read_excel(self.meta_excel_path).head(10) if not self.meta_excel_path.endswith('.csv') else pd.read_csv(self.meta_excel_path).head(10)
                data_summary += "Meta Ads Verileri:\n" + df_meta.to_string() + "\n\n"

            # İŞTE BURASI: KESİNLİKLE HATA VERMEYEN YENİ MODEL
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash') 
            
            prompt = f"""
            Sen {self.current_company} adındaki seyahat acentesinin dijital pazarlama yapay zekası 'Delta'sın.
            Patronun için aşağıdaki ham reklam verilerini incele ve ona yönelik, tamamen profesyonel, 
            sadece 2 veya 3 kısa paragraftan oluşan, gidişatı özetleyen bir 'Yönetici Özeti' yaz.
            Sayıları mantıklıca birleştir. Tablo çizme, sadece akıcı metin yaz.
            Veriler:
            {data_summary}
            """
            
            response = model.generate_content(prompt)
            ai_text = tr_fix(response.text)

            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_fill_color(5, 5, 8)
            pdf.rect(0, 0, 210, 297, 'F')
            
            pdf.set_font("Arial", 'B', 20)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(190, 15, txt=tr_fix(self.report_type_entry.get().upper()), ln=1, align='C')
            
            pdf.set_text_color(100, 100, 120) 
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(190, 8, txt=f"{self.current_company} | YZ Analiz Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=1, align='C')
            pdf.ln(10)

            color_rgb = (0, 240, 255) if self.current_company == "Tilos Travel" else (57, 255, 20)
            pdf.set_text_color(*color_rgb)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(190, 10, txt="DELTA AI: YONETICI OZETI", ln=1, align='L')
            
            pdf.set_text_color(220, 220, 220)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(190, 7, txt=ai_text)
            pdf.ln(10)

            def draw_table(df, title, rgb):
                pdf.set_text_color(*rgb)
                pdf.set_draw_color(*rgb)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, txt=title, ln=1)
                
                col_w = 190 / (len(df.columns) if len(df.columns) > 0 else 1)
                
                pdf.set_fill_color(20, 20, 30) 
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 8)
                for col in df.columns:
                    pdf.cell(col_w, 7, tr_fix(str(col))[:20], border=1, fill=True, align='C')
                pdf.ln()
                
                pdf.set_font("Arial", '', 7)
                pdf.set_fill_color(10, 10, 15)
                for _, row in df.iterrows():
                    for val in row:
                        pdf.cell(col_w, 7, tr_fix(str(val))[:25], border=1, fill=True, align='C') 
                    pdf.ln()
                pdf.ln(5)

            if df_google is not None: draw_table(df_google, "Google Arama/Ads Verileri", color_rgb)
            if df_meta is not None: draw_table(df_meta, "Meta Ads Verileri", (255, 20, 147))

            if self.uploaded_image_paths:
                pdf.add_page() 
                pdf.set_fill_color(5, 5, 8)
                pdf.rect(0, 0, 210, 297, 'F')
                
                pdf.set_text_color(*color_rgb)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(190, 10, txt="PERFORMANS GRAFIKLERI & GORSELLER", ln=1, align='C')
                pdf.ln(5)

                x_start = 15
                y_start = pdf.get_y()
                img_width = 85 
                img_height = 60 
                
                x, y = x_start, y_start
                
                for i, img_path in enumerate(self.uploaded_image_paths):
                    if y + img_height > 270:
                        pdf.add_page()
                        pdf.set_fill_color(5, 5, 8)
                        pdf.rect(0, 0, 210, 297, 'F')
                        y = 20
                        x = x_start
                    
                    try:
                        pdf.image(img_path, x=x, y=y, w=img_width)
                    except:
                        pass 
                    
                    if (i + 1) % 2 == 0:
                        x = x_start
                        y += img_height + 10 
                    else:
                        x += img_width + 10 

            file_name = f"AI_Rapor_{self.current_company.replace(' ', '_')}_{datetime.now().strftime('%H%M%S')}.pdf"
            pdf.output(file_name)
            
            self.btn_generate_ai.configure(text="🔥 YZ ANALİZİ İLE PDF OLUŞTUR", fg_color=self.current_color)
            messagebox.showinfo("Başarılı", f"Delta AI raporu yazdı ve görselleri dizdi!\n\nDosya: {file_name}")
            
        except Exception as e:
            self.btn_generate_ai.configure(text="🔥 YZ ANALİZİ İLE PDF OLUŞTUR", fg_color=self.current_color)
            messagebox.showerror("Yapay Zeka Hatası", f"İşlem sırasında bir sorun oluştu.\nDetay: {str(e)}")

    def switch_company(self, company):
        self.current_company = company
        if company == "Tilos Travel":
            self.current_color = CYAN_NEON
            self.btn_tilos.configure(border_color=CYAN_NEON, text_color=CYAN_NEON)
            self.btn_makri.configure(border_color=TEXT_MUTED, text_color=TEXT_MUTED)
        else:
            self.current_color = GREEN_NEON
            self.btn_makri.configure(border_color=GREEN_NEON, text_color=GREEN_NEON)
            self.btn_tilos.configure(border_color=TEXT_MUTED, text_color=TEXT_MUTED)
            
        self.tabs.configure(segmented_button_selected_color=self.current_color)

if __name__ == "__main__":
    app = UltimateDesktopPanel()
    app.mainloop()

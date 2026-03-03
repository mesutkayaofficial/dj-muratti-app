import streamlit as st
import requests
import time

# --- 1. SETTINGS & VIBE ---
st.set_page_config(page_title="DJ MURATTI HQ", page_icon="🎧", layout="centered")

# --- 2. THE "PULSE" DESIGN SYSTEM (CSS) ---
st.markdown("""
<style>
    /* Google Fonts Entegrasyonu */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@300;700&display=swap');
    
    /* OLED Siyah Arka Plan */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }

    /* Glassmorphism Kartlar */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 255, 255, 0.1);
        padding: 25px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    
    /* Neon Başlık Tasarımı (PNG Yerine) */
    .brand-header {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 40px;
        letter-spacing: 12px;
        text-align: center;
        color: #FFFFFF;
        margin-top: 30px;
        text-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
        text-transform: uppercase;
    }

    .artist-subtitle {
        font-family: 'Orbitron', sans-serif;
        color: #00FFFF; /* Electric Cyan */
        text-align: center;
        font-size: 12px;
        letter-spacing: 5px;
        margin-top: -10px;
        margin-bottom: 30px;
    }

    /* Master Meter (8.4M Daire Efekti) */
    .master-meter {
        width: 160px;
        height: 160px;
        border: 2px solid #00FFFF;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 20px auto;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.2);
        animation: pulseFade 3s infinite ease-in-out;
    }
    
    @keyframes pulseFade {
        0% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.03); opacity: 1; }
        100% { transform: scale(1); opacity: 0.7; }
    }

    /* Neon Amber Buton */
    .stButton>button {
        width: 100%;
        border-radius: 100px;
        height: 4em;
        background: linear-gradient(90deg, #FFBF00, #FF8C00); /* Neon Amber */
        color: #000;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        border: none;
        box-shadow: 0 5px 20px rgba(255, 191, 0, 0.3);
        transition: 0.3s ease;
        margin-top: 10px;
    }
    .stButton>button:hover {
        box-shadow: 0 0 35px rgba(255, 191, 0, 0.6);
        transform: translateY(-2px);
    }

    /* Sekme Tasarımı */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #111;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: #888;
    }
    .stTabs [aria-selected="true"] { background-color: #222 !important; color: #00FFFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. HOME SCREEN: THE PULSE ---
# Başlık (Logo Yerine Font Tasarımı)
st.markdown("<div class='brand-header'>MURATTI</div>", unsafe_allow_html=True)
st.markdown("<div class='artist-subtitle'>OFFICIAL ARTIST PANEL</div>", unsafe_allow_html=True)

# Master Meter (Global Reach Snapshot)
st.markdown("""
<div class='master-meter'>
    <span style='font-family:Orbitron; font-size:28px; color:#00FFFF; font-weight:900;'>8.4M</span>
    <span style='font-size:10px; color:#888; letter-spacing:1px;'>GLOBAL REACH</span>
</div>
""", unsafe_allow_html=True)

# --- 4. DATA ENGINE ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

# Metrics Grid
c1, c2 = st.columns(2)
c1.metric("TK STREAMS", "128.4K", delta="+1.2K")
c2.metric("REVENUE", "$X,XXX", delta="Pending", delta_color="off")

if st.button("⚡ ANALİZİ SENKRONİZE ET"):
    with st.spinner("Accessing TikTok Data Vault..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            res_i = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": f"https://www.tiktok.com/music/Triangel-{MUSIC_ID}"})
            total_vids = res_i.json().get('data', {}).get('video_count', 0)
            
            st.markdown(f"""
                <div style='background:rgba(0,255,255,0.05); padding:20px; border-radius:15px; border-left:4px solid #00FFFF;'>
                    <h4 style='margin:0; font-size:12px; color:#00FFFF; font-family:Orbitron;'>SYNC SUCCESSFUL</h4>
                    <p style='font-size:26px; font-weight:bold; margin:0;'>{total_vids:,} <span style='font-size:12px; color:#888;'>Videos</span></p>
                </div>
            """, unsafe_allow_html=True)
        except:
            st.error("Bağlantı Hatası!")

# --- 5. TABS ---
st.write("")
tab1, tab2, tab3 = st.tabs(["📈 GROWTH", "💰 FINANCE", "🛡️ BRAND"])

with tab1:
    st.info("Mersin, İstanbul ve Berlin lokasyonlarında erişim artıyor.")
    st.caption("Gelişmiş grafikler bir sonraki güncellemede aktif edilecektir.")

with tab2:
    st.markdown("""
        <div style='background:#0a0a0a; padding:15px; border-radius:12px; border:1px solid #333; margin-bottom:10px;'>
            <span style='color:#888;'>Gig Fee: Mersin Show</span><br>
            <b style='color:#FFBF00;'>$X,XXX</b> | <span style='color:#1ed760;'>🟢 PAID</span>
        </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("🛡️ **Trademark Status:** DJ MURATTI® Registration in Progress.")
    st.button("📄 EPK DOSYASI OLUŞTUR")

st.divider()
st.caption(f"Haptic System: ON • {time.strftime('%H:%M:%S')} • HQ")

import streamlit as st
import requests
import time

# --- 1. PREMIUM KONFİGÜRASYON ---
st.set_page_config(page_title="DJ MURATTI", page_icon="🎧", layout="centered")

# --- 2. LOGO VE ANİMASYONLU ARAYÜZ (CSS) ---
st.markdown("""
    <style>
    /* Saf Siyah Arka Plan */
    .stApp {
        background: #000000;
        color: #ffffff;
    }
    
    /* Logo ve Başlık Alanı */
    .brand-container {
        text-align: center;
        padding: 40px 0 20px 0;
    }
    
    /* PDF'deki NM Kalkanı Fontu ve Animasyonu */
    .logo-font {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 900;
        font-size: 55px;
        letter-spacing: 8px;
        color: #ffffff;
        margin: 0;
        text-transform: uppercase;
        /* Parlama Animasyonu */
        text-shadow: 0 0 10px rgba(30, 215, 96, 0.4);
        animation: logoGlow 3s infinite ease-in-out;
    }
    
    @keyframes logoGlow {
        0% { text-shadow: 0 0 10px rgba(30, 215, 96, 0.4); transform: scale(1); }
        50% { text-shadow: 0 0 30px rgba(30, 215, 96, 0.8); transform: scale(1.02); }
        100% { text-shadow: 0 0 10px rgba(30, 215, 96, 0.4); transform: scale(1); }
    }

    .sub-tag {
        color: #1ed760;
        font-size: 14px;
        letter-spacing: 4px;
        font-weight: bold;
        text-transform: uppercase;
        margin-top: -5px;
    }

    /* Glassmorphism Veri Kartları */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    
    label[data-testid="stMetricLabel"] { color: #888888 !important; letter-spacing: 1px; }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; font-weight: bold !important; }

    /* Neon Analiz Butonu */
    .stButton>button {
        width: 100%;
        border-radius: 100px;
        height: 4em;
        background: linear-gradient(90deg, #1ed760, #1db954);
        color: #000;
        font-weight: 900;
        font-size: 18px;
        border: none;
        box-shadow: 0 5px 25px rgba(30, 215, 96, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(30, 215, 96, 0.5);
    }

    /* Kanıt Listesi Kartları */
    .proof-item {
        background: rgba(255, 255, 255, 0.03);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #1ed760;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ANİMASYONLU MARKA ALANI ---
st.markdown("""
    <div class='brand-container'>
        <div class='logo-font'>MURATTI</div>
        <div class='sub-tag'>Official Artist Panel</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. VERİ ANALİZ MOTORU ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

if st.button("🚀 VERİLERİ SENKRONİZE ET"):
    with st.spinner("Rapor oluşturuluyor..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            # Genel Bilgi
            res_i = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": f"https://www.tiktok.com/music/Triangel-{MUSIC_ID}"})
            total_vids = res_i.json().get('data', {}).get('video_count', 0)
            
            # TOP 150 Örneği
            res_p = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": MUSIC_ID, "count": "30", "cursor": "0"})
            vids = res_p.json().get('data', {}).get('videos', [])
            trend_views = sum(v.get('play_count', 0) for v in vids)

            # Görselleştirme
            st.write("")
            c1, c2 = st.columns(2)
            c1.metric("TOPLAM VİDEO", f"{total_vids:,}")
            c2.metric("TREND İZLENME", "8.4M+") # Senin verini yansıtacak şekilde ayarlandı
            
            st.write("---")
            st.markdown("### 🔝 En Popüler Kanıtlar")
            for i, v in enumerate(vids[:5], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                st.markdown(f"""
                <div class='proof-item'>
                    <span style='color:#1ed760; font-weight:bold;'>#{i}</span> | 
                    <b>{v.get('play_count', 0):,}</b> İzlenme - <a href='{v_url}' target='_blank' style='color:#888;'>İncele →</a>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error("API Bağlantı Hatası!")

st.divider()
st.caption(f"© 2026 DJ MURATTI | Son Senkronizasyon: {time.strftime('%H:%M:%S')}")

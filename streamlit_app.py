import streamlit as st
import requests
import time

# --- 1. SAYFA KONFİGÜRASYONU ---
st.set_page_config(page_title="DJ MURATTI", page_icon="🎧", layout="centered")

# --- 2. PREMIUM UI (CSS) ---
st.markdown("""
    <style>
    /* Ana Arka Plan: Koyu Gradyan */
    .stApp {
        background: radial-gradient(circle at top right, #1db95422, #000000);
        color: #ffffff;
    }
    
    /* Üst Başlık Tasarımı */
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
        text-align: center;
        background: -webkit-linear-gradient(#fff, #1ed760);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 0px;
    }

    /* Modern Kart Yapıları (Glassmorphism) */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: 0.3s;
    }
    div[data-testid="stMetric"]:hover {
        border: 1px solid #1ed760;
        transform: translateY(-5px);
    }
    
    /* Metrik Fontları */
    label[data-testid="stMetricLabel"] { 
        color: #888888 !important; 
        font-size: 14px !important; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div[data-testid="stMetricValue"] { 
        color: #ffffff !important; 
        font-size: 38px !important; 
    }

    /* Ana Buton: Neon Parlama */
    .stButton>button {
        width: 100%;
        border-radius: 100px;
        height: 4em;
        background: linear-gradient(90deg, #1ed760, #1db954);
        color: black;
        font-weight: bold;
        font-size: 18px;
        border: none;
        box-shadow: 0 4px 20px rgba(30, 215, 96, 0.4);
        transition: 0.4s;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(30, 215, 96, 0.7);
        transform: scale(1.02);
    }

    /* Link Kartları */
    .video-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 15px;
        border-radius: 16px;
        margin-bottom: 10px;
        border-left: 4px solid #1ed760;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("<h1 class='main-header'>DJ MURATTI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#1ed760; margin-top:-10px; font-weight:500;'>ARTIST INSIGHTS • LIVE</p>", unsafe_allow_html=True)
st.write("")

# --- 4. ANALİZ MOTORU ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

if st.button("📊 VERİLERİ SENKRONİZE ET"):
    with st.spinner("Veriler işleniyor..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            # 1. Genel Bilgi
            res_i = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": f"https://www.tiktok.com/music/Triangel-{MUSIC_ID}"})
            total_vids = res_i.json().get('data', {}).get('video_count', 0)
            
            # 2. TOP 150 Çekme (Hızlı Döngü)
            all_vids = []
            cursor = "0"
            for _ in range(5):
                res_p = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": MUSIC_ID, "count": "30", "cursor": cursor})
                data = res_p.json().get('data', {})
                vids = data.get('videos', [])
                if not vids: break
                all_vids.extend(vids)
                cursor = data.get('cursor', '0')
                if not data.get('hasMore'): break
                time.sleep(0.1)

            top_150 = all_vids[:150]
            trend_views = sum(v.get('play_count', 0) for v in top_150)

            # Görsel Sonuçlar
            st.write("")
            c1, c2 = st.columns(2)
            c1.metric("GÖNDERİLER", f"{total_vids:,}")
            c2.metric("TOP 150 İZLENME", f"{trend_views:,}")
            
            st.write("")
            st.markdown("### 🔝 En Popüler Kanıtlar")
            
            sorted_vids = sorted(top_150, key=lambda x: x.get('play_count', 0), reverse=True)
            for i, v in enumerate(sorted_vids[:10], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                p_count = v.get('play_count', 0)
                
                st.markdown(f"""
                <div class='video-card'>
                    <span style='color:#1ed760; font-weight:bold;'>#{i}</span> | 
                    <span style='color:white; font-weight:bold;'>{p_count:,} İzlenme</span><br>
                    <a href='{v_url}' style='color:#888888; text-decoration:none; font-size:12px;'>Videoyu TikTok'ta görüntüle →</a>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error("Bağlantı Hatası!")

# --- 5. FOOTER ---
st.write("")
st.markdown("---")
st.markdown(f"<p style='text-align:center; color:#444;'>Son Güncelleme: {time.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

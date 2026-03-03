import streamlit as st
import requests
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="DJ MURATTI", page_icon="🎧", layout="centered")

# --- 2. ANİMASYONLU PREMIUM TASARIM ---
st.markdown("""
<style>
    /* Saf Siyah Arka Plan */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Animasyonlu Logo Alanı */
    .logo-container {
        text-align: center;
        padding: 40px 0 20px 0;
    }
    
    .logo-animation {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 900;
        font-size: 50px;
        letter-spacing: 10px;
        color: #ffffff;
        text-transform: uppercase;
        /* Parlama ve Hareket Animasyonu */
        animation: murattiGlow 3s infinite ease-in-out;
        display: inline-block;
    }
    
    @keyframes murattiGlow {
        0% { text-shadow: 0 0 10px rgba(30, 215, 96, 0.3); transform: scale(1); opacity: 0.8; }
        50% { text-shadow: 0 0 30px rgba(30, 215, 96, 0.8); transform: scale(1.05); opacity: 1; }
        100% { text-shadow: 0 0 10px rgba(30, 215, 96, 0.3); transform: scale(1); opacity: 0.8; }
    }

    .tagline { 
        text-align: center; color: #1ed760; font-weight: bold; 
        letter-spacing: 4px; font-size: 14px; margin-top: -10px;
    }

    /* Modern Kartlar */
    div[data-testid="stMetric"] { 
        background-color: rgba(255, 255, 255, 0.05); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        padding: 25px; border-radius: 25px; text-align: center; 
    }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; font-size: 32px !important; }

    /* Neon Buton */
    .stButton>button { 
        width: 100%; border-radius: 100px; height: 4em; 
        background: linear-gradient(90deg, #1ed760, #1db954); 
        color: #000; font-weight: 800; border: none; font-size: 16px;
        box-shadow: 0 4px 20px rgba(30, 215, 96, 0.3);
    }
    
    .card { 
        background: rgba(255, 255, 255, 0.03); padding: 15px; 
        border-radius: 15px; margin-bottom: 10px; border-left: 5px solid #1ed760; 
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ANİMASYONLU ÜST PANEL ---
st.markdown("""
<div class="logo-container">
    <div class="logo-animation">MURATTI</div>
    <div class="tagline">ARTIST ANALYTICS DASHBOARD</div>
</div>
""", unsafe_allow_html=True)
st.write("")

# --- 4. VERİ MOTORU ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

if st.button("📊 ANALİZİ BAŞLAT"):
    with st.spinner("Veriler senkronize ediliyor..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            # Genel Bilgi
            res_i = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": f"https://www.tiktok.com/music/Triangel-{MUSIC_ID}"})
            total_vids = res_i.json().get('data', {}).get('video_count', 0)
            
            # Trend İzlenme Örneği
            res_p = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": MUSIC_ID, "count": "30", "cursor": "0"})
            vids = res_p.json().get('data', {}).get('videos', [])
            
            st.write("")
            c1, c2 = st.columns(2)
            c1.metric("GÖNDERİ", f"{total_vids:,}")
            c2.metric("İZLENME", "8.4M+") 

            st.write("---")
            st.markdown("### 🔝 Popüler Kanıtlar")
            for i, v in enumerate(vids[:5], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                st.markdown(f"""
                <div class="card">
                    <b>#{i}</b> | {v.get('play_count', 0):,} İzlenme<br>
                    <a href="{v_url}" target="_blank" style="color:#1ed760; text-decoration:none; font-size:12px;">TikTok'ta Gör →</a>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.error("Bağlantı kesildi!")

st.divider()
st.caption(f"© 2026 DJ MURATTI | {time.strftime('%H:%M:%S')}")

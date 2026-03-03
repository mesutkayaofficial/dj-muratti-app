import streamlit as st
import requests
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="DJ MURATTI", page_icon="🎧")

# --- 2. TASARIM ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-text { 
        text-align: center; font-size: 45px; font-weight: 900; 
        letter-spacing: 8px; color: #ffffff; margin-top: 20px;
        text-shadow: 0 0 15px rgba(30, 215, 96, 0.5);
    }
    .tagline { text-align: center; color: #1ed760; font-weight: bold; letter-spacing: 2px; font-size: 14px; }
    div[data-testid="stMetric"] { 
        background-color: #0a0a0a; border: 1px solid #222; 
        padding: 20px; border-radius: 20px; text-align: center; 
    }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; font-size: 32px !important; }
    .stButton>button { 
        width: 100%; border-radius: 50px; height: 3.5em; 
        background: linear-gradient(90deg, #1ed760, #1db954); 
        color: #000; font-weight: bold; border: none; font-size: 16px;
    }
    .card { 
        background: #0a0a0a; padding: 15px; border-radius: 15px; 
        margin-bottom: 10px; border-left: 5px solid #1ed760; 
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BAŞLIK ---
st.markdown('<div class="logo-text">MURATTI</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">ARTIST ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)
st.write("")

# --- 4. VERİ MERKEZİ ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

if st.button("📊 ANALİZİ BAŞLAT"):
    with st.spinner("Veriler işleniyor..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            # Genel Bilgi
            res_i = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": f"https://www.tiktok.com/music/Triangel-{MUSIC_ID}"})
            total_vids = res_i.json().get('data', {}).get('video_count', 0)
            
            # Trend İzlenme
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
                    <a href="{v_url}" target="_blank" style="color:#1ed760; text-decoration:none; font-size:12px;">Videoyu İncele →</a>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.error("API hatası! Lütfen tekrar deneyin.")

st.divider()
st.caption(f"© 2026 DJ MURATTI | {time.strftime('%H:%M:%S')}")

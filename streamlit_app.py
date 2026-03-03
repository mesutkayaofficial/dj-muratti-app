import streamlit as st
import requests
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="DJ MURATTI HQ", page_icon="🎧", layout="centered")

def giris_kontrol():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if not st.session_state.auth:
        st.markdown("<h1 style='text-align: center; color: #00ff00; font-family: sans-serif;'>DJ MURATTI HQ</h1>", unsafe_allow_html=True)
        sifre = st.text_input("Erişim Anahtarı", type="password")
        if st.button("SİSTEME GİRİŞ"):
            if sifre == "MURATTI2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Yetkisiz Erişim!")
        st.stop()

giris_kontrol()

# --- 2. MODERN DARK UI (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    div[data-testid="stMetric"] {
        background-color: #0a0a0a;
        border: 1px solid #1ed760;
        padding: 25px;
        border-radius: 20px;
    }
    label[data-testid="stMetricLabel"] { color: #aaaaaa !important; font-size: 18px !important; }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; font-size: 32px !important; }
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        height: 3.5em;
        background-color: #1ed760;
        color: black;
        font-weight: bold;
        border: none;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    hr { border-color: #333333; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BAŞLIK ---
st.markdown("<h1 style='text-align: center; color: white;'>DJ MURATTI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #1ed760;'>REAL-TIME ANALYTICS</p>", unsafe_allow_html=True)
st.write("")

# --- 4. VERİ MOTORU ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa" 
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_LINK = "https://www.tiktok.com/music/Triangel-Violin-Classic-7087325412228859906"

if st.button("📊 VERİLERİ GÜNCELLE"):
    with st.spinner(""):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            # Info
            res_info = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": MUSIC_LINK})
            info = res_info.json().get('data', {})
            
            # Posts (İzlenme toplama)
            res_p = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": "7087325412228859906", "count": "30", "cursor": "0"})
            vids = res_p.json().get('data', {}).get('videos', [])
            izlenme = sum(v.get('play_count', 0) for v in vids)
            
            st.write("")
            c1, c2 = st.columns(2)
            c1.metric("TOPLAM VİDEO", f"{info.get('video_count', 0):,}")
            c2.metric("TREND İZLENME", f"{izlenme:,}")
            
            st.write("")
            st.toast("Veriler başarıyla çekildi.")
            
        except Exception as e:
            st.error("Bağlantı sağlanamadı.")

st.write("")
st.divider()
st.caption(f"Son Senkronizasyon: {time.strftime('%H:%M:%S')}")

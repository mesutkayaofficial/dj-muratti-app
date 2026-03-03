import streamlit as st
import requests
import time

# --- 1. GÜVENLİK VE AYARLAR ---
st.set_page_config(page_title="DJ MURATTI HQ", page_icon="🎧", layout="centered")

def giris_kontrol():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    
    if not st.session_state.auth:
        st.markdown("<h1 style='text-align: center; color: #1ed760; font-family: sans-serif;'>DJ MURATTI HQ</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white;'>Lütfen erişim anahtarınızı giriniz.</p>", unsafe_allow_html=True)
        
        sifre = st.text_input("", type="password", placeholder="Şifre...")
        if st.button("SİSTEME GİRİŞ YAP"):
            if sifre == "MURATTI2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Hatalı Şifre!")
        st.stop()

giris_kontrol()

# --- 2. MODERN UI TASARIMI ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    div[data-testid="stMetric"] {
        background-color: #0a0a0a;
        border: 1px solid #1ed760;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
    }
    label[data-testid="stMetricLabel"] { color: #aaaaaa !important; font-size: 16px !important; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; font-size: 36px !important; font-weight: bold !important; }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background-color: #1ed760;
        color: black;
        font-weight: bold;
        border: none;
        letter-spacing: 1px;
        margin-top: 10px;
    }
    hr { border-color: #222222; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST PANEL ---
st.markdown("<h1 style='text-align: center; color: white; margin-bottom:0;'>DJ MURATTI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #1ed760; font-weight: bold;'>LIVE PERFORMANCE TRACKER</p>", unsafe_allow_html=True)
st.write("")

# --- 4. VERİ ÇEKME MOTORU ---
try:
    API_KEY = st.secrets["api_key"]
except:
    API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"

HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_LINK = "https://www.tiktok.com/music/Triangel-Violin-Classic-7087325412228859906"

if st.button("🔄 VERİLERİ ŞİMDİ GÜNCELLE"):
    with st.spinner(""):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            res_info = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": MUSIC_LINK})
            info = res_info.json().get('data', {})
            
            res_p = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": "7087325412228859906", "count": "30", "cursor": "0"})
            vids = res_p.json().get('data', {}).get('videos', [])
            izlenme = sum(v.get('play_count', 0) for v in vids)
            
            st.write("")
            c1, c2 = st.columns(2)
            c1.metric("TOPLAM VİDEO", f"{info.get('video_count', 0):,}")
            c2.metric("TREND İZLENME", f"{izlenme:,}")
            
            st.write("")
            st.toast("Veriler güncellendi!", icon="

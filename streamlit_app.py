import streamlit as st
import requests
import time

# --- 1. GÜVENLİK ---
st.set_page_config(page_title="DJ MURATTI HQ", page_icon="🎧")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🎧 DJ MURATTI HQ")
    sifre = st.text_input("Erişim Şifresi", type="password")
    if st.button("Giriş Yap"):
        if sifre == "MURATTI2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Hatalı!")
    st.stop()

# --- 2. TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    div[data-testid="stMetric"] { background-color: #0a0a0a; border: 1px solid #1ed760; padding: 20px; border-radius: 15px; }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; }
    .stButton>button { width: 100%; border-radius: 50px; background-color: #1ed760; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("DJ MURATTI")
st.write("TikTok Performans Takibi")

# --- 3. VERİ ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
URL = "https://www.tiktok.com/music/Triangel-Violin-Classic-7087325412228859906"

if st.button("VERİLERİ GÜNCELLE"):
    with st.spinner("Lütfen bekleyin..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            res = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": URL})
            info = res.json().get('data', {})
            
            st.write("")
            c1, c2 = st.columns(2)
            c1.metric("VİDEO SAYISI", f"{info.get('video_count', 0):,}")
            c2.metric("DURUM", "AKTİF")
            st.success("Veriler başarıyla çekildi.")
        except:
            st.error("Bağlantı hatası!")

st.divider()
st.caption(f"Sistem Zamanı: {time.strftime('%H:%M:%S')}")

import streamlit as st
import requests
import time

# --- GÜVENLİK AYARI ---
def giris_kontrol():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if not st.session_state.auth:
        st.title("🔐 DJ MURATTI Özel Panel")
        sifre = st.text_input("Giriş Şifresi", type="password")
        if st.button("Giriş Yap"):
            if sifre == "MURATTI2026": # Şifren bu, istersen değiştirebilirsin
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Hatalı şifre!")
        st.stop()

giris_kontrol()

# --- TASARIM ---
st.set_page_config(page_title="DJ MURATTI App", page_icon="🎧")
st.markdown("<style>.stButton>button {width:100%; border-radius:20px; background-color:#00ff00; color:black; font-weight:bold;}</style>", unsafe_allow_html=True)

st.title("🎧 DJ MURATTI Analytics")
st.subheader("TikTok Telif & Performans Takibi")

# --- VERİ ÇEKME ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa" # Senin RapidAPI Key'in
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_LINK = "https://www.tiktok.com/music/Triangel-Violin-Classic-7087325412228859906"

if st.button("📊 GÜNCEL VERİLERİ GETİR"):
    with st.spinner("TikTok taranıyor..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            # 1. Genel Bilgi
            res_info = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": MUSIC_LINK})
            info = res_info.json().get('data', {})
            
            # 2. İzlenme Taraması (Popüler Videolar)
            res_p = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": "7087325412228859906", "count": "30", "cursor": "0"})
            vids = res_p.json().get('data', {}).get('videos', [])
            
            izlenme = sum(v.get('play_count', 0) for v in vids)
            
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("Toplam Video", f"{info.get('video_count', 0):,}")
            c2.metric("Trend İzlenme", f"{izlenme:,}")
            st.success(f"Güncelleme Başarılı: {time.strftime('%H:%M')}")
            st.info("Bu veriler dava sürecinde kanıt dökümü olarak kullanılabilir.")
        except Exception as e:
            st.error(f"Hata: {e}")

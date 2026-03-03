import streamlit as st
import requests
import time

# --- 1. GÜVENLİK ---
st.set_page_config(page_title="DJ MURATTI TOP 150", page_icon="🎧")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='color: #1ed760;'>DJ MURATTI HQ</h1>", unsafe_allow_html=True)
    sifre = st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        if sifre == "MURATTI2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Hatalı!")
    st.stop()

# --- 2. TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000; }
    div[data-testid="stMetric"] { background-color: #0a0a0a; border: 1px solid #1ed760; padding: 20px; border-radius: 15px; }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; }
    .stButton>button { width: 100%; border-radius: 50px; background-color: #1ed760; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("DJ MURATTI")
st.subheader("TOP 150 Performans Takibi")

# --- 3. VERİ AYARLARI ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

if st.button("🚀 TOP 150 ANALİZİNİ BAŞLAT"):
    with st.spinner("150 Video taranıyor..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            # Genel Bilgi
            res_i = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": f"https://www.tiktok.com/music/Triangel-{MUSIC_ID}"})
            total_vids = res_i.json().get('data', {}).get('video_count', 0)
            
            # TOP 150 Döngüsü
            all_vids = []
            cursor = "0"
            for _ in range(5):
                res_p = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": MUSIC_ID, "count": "30", "cursor": cursor})
                data = res_p.json().get('data', {})
                vids = data.get('videos', [])
                if not vids: break
                all_vids.extend(vids)
                cursor = data.get('cursor')
                if not data.get('hasMore'): break
                time.sleep(0.3)

            top_150 = all_vids[:150]
            trend_views = sum(v.get('play_count', 0) for v in top_150)

            c1, c2 = st.columns(2)
            c1.metric("TOPLAM VİDEO", f"{total_vids:,}")
            c2.metric("TOP 150 İZLENME", f"{trend_views:,}")
            
            st.write("---")
            st.markdown("### 🔗 En Popüler Kanıt Linkleri")
            sorted_vids = sorted(top_150, key=lambda x: x.get('play_count', 0), reverse=True)
            for i, v in enumerate(sorted_vids[:10], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                st.markdown(f"{i}. **{v.get('play_count', 0):,}** İzlenme - [Link]({v_url})")

        except Exception as e:
            st.error(f"Sistem Hatası: {e}")

st.divider()
st.caption(f"DJ MURATTI | Son Sorgu: {time.strftime('%H:%M:%S')}")

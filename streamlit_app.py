import streamlit as st
import requests
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="DJ MURATTI ANALYTICS", page_icon="🎧", layout="centered")

# --- 2. MODERN DARK TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    div[data-testid="stMetric"] {
        background-color: #0a0a0a;
        border: 1px solid #1ed760;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    label[data-testid="stMetricLabel"] { color: #aaaaaa !important; font-size: 14px !important; }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; font-size: 32px !important; font-weight: bold !important; }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background-color: #1ed760;
        color: black;
        font-weight: bold;
        border: none;
        text-transform: uppercase;
    }
    hr { border-color: #222222; }
    </style>
    """, unsafe_allow_html=True)

st.title("DJ MURATTI")
st.subheader("TOP 150 Performans Takibi")

# --- 3. VERİ AYARLARI ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

# --- 4. ANALİZ MOTORU ---
if st.button("🚀 TOP 150 VERİLERİNİ GETİR"):
    with st.spinner("TikTok taranıyor, lütfen bekleyin..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            # 1. Toplam Video Sayısı
            res_i = requests.get(f"https://{HOST}/music/info", headers=headers, params={"url": f"https://www.tiktok.com/music/Triangel-{MUSIC_ID}"})
            total_vids = res_i.json().get('data', {}).get('video_count', 0)
            
            # 2. TOP 150 İzlenme Taraması
            all_vids = []
            cursor = "0"
            for _ in range(5): # 5 sayfa çekerek 150 videoya ulaşır
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

            # Sonuçları Göster
            st.write("")
            col1, col2 = st.columns(2)
            col1.metric("TOPLAM VİDEO", f"{total_vids:,}")
            col2.metric("TOP 150 İZLENME", f"{trend_views:,}")
            
            st.write("---")
            st.markdown("### 🔗 En Popüler Kanıt Videoları")
            
            # İzlenmeye göre sırala ve ilk 10'u listele
            sorted_vids = sorted(top_150, key=lambda x: x.get('play_count', 0), reverse=True)
            for i, v in enumerate(sorted_vids[:10], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                st.markdown(f"{i}. **{v.get('play_count', 0):,}** İzlenme - [Link]({v_url})")

        except Exception as e:
            st.error(f"Sistem Hatası: {e}")

st.divider()
st.caption(f"DJ MURATTI | Canlı Analiz Sistemi | {time.strftime('%H:%M:%S')}")

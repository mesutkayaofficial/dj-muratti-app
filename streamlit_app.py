import streamlit as st
import requests
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="DJ MURATTI", page_icon="🎧")

# --- 2. OLED DARK DESIGN ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    .brand { 
        text-align: center; font-family: 'Helvetica Neue', sans-serif; 
        font-size: 40px; font-weight: 900; letter-spacing: 10px; 
        padding: 30px 0; color: #ffffff;
        text-shadow: 0 0 20px rgba(30, 215, 96, 0.4);
    }
    div[data-testid="stMetric"] { 
        background-color: #0a0a0a; border: 1px solid #1ed760; 
        padding: 20px; border-radius: 20px; text-align: center; 
    }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; font-size: 32px !important; }
    .stButton>button { 
        width: 100%; border-radius: 100px; height: 4em; 
        background: linear-gradient(90deg, #1ed760, #1db954); 
        color: #000; font-weight: bold; border: none; font-size: 16px;
    }
    .proof-card { 
        background: #0a0a0a; padding: 12px; border-radius: 12px; 
        margin-bottom: 8px; border-left: 4px solid #00FFFF; font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BAŞLIK ---
st.markdown('<div class="brand">MURATTI</div>', unsafe_allow_html=True)

# --- 4. VERİ MOTORU ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

if st.button("🚀 TOP 150 ANALİZİNİ BAŞLAT"):
    with st.spinner("150 Video taranıyor, lütfen bekleyin..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            all_vids = []
            cursor = "0"
            
            # 150 videoya ulaşmak için 5 sayfa çekiyoruz (Her sayfa 30 video)
            for _ in range(5):
                res = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": MUSIC_ID, "count": "30", "cursor": cursor})
                data = res.json().get('data', {})
                vids = data.get('videos', [])
                if not vids: break
                all_vids.extend(vids)
                cursor = data.get('cursor', '0')
                if not data.get('hasMore'): break
                time.sleep(0.2)

            # Sadece ilk 150 videoyu al ve toplam izlenmeyi hesapla
            top_150 = all_vids[:150]
            total_views_150 = sum(v.get('play_count', 0) for v in top_150)

            # Üst Metrik Paneli
            st.write("")
            st.metric("TOP 150 TOPLAM İZLENME", f"{total_views_150:,}")
            
            # En Popüler 50 Video Listesi
            st.write("---")
            st.subheader("🔝 En Popüler 50 Kanıt Videosu")
            
            # İzlenmeye göre sırala
            sorted_vids = sorted(top_150, key=lambda x: x.get('play_count', 0), reverse=True)
            
            for i, v in enumerate(sorted_vids[:50], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                st.markdown(f"""
                <div class="proof-card">
                    <b style="color:#00FFFF;">#{i}</b> | <b>{v.get('play_count', 0):,}</b> İzlenme <br>
                    <a href="{v_url}" target="_blank" style="color:#1ed760; text-decoration:none;">Videoyu TikTok'ta Aç →</a>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error("Veri çekme sırasında bir hata oluştu.")

st.divider()
st.caption(f"DJ MURATTI | Canlı Veri Sistemi | {time.strftime('%H:%M:%S')}")

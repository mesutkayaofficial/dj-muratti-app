import streamlit as st
import requests
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="DJ MURATTI Analytics", page_icon="🎧", layout="centered")

# Streamlit arayüzünü temizleyen stil
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0 !important;}
    .stButton>button {
        width: 100%; border-radius: 100px; height: 3.5em; 
        background: linear-gradient(90deg, #00f5ff, #1ed760); 
        color: #000; font-weight: bold; border: none; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. VERİ MOTORU ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

# Senin HTML Tasarımın (Buraya doğrudan gömüldü - Dosya hatası vermez)
def get_dashboard_html(total_views="8.4M", video_items=""):
    # Senin gönderdiğin HTML şablonunun başlangıcı
    html_start = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Syne:wght@400;800&display=swap" rel="stylesheet">
    <style>
      :root {{ --bg: #04060f; --surface: #0b0e1a; --cyan: #00f5ff; --green: #1ed760; --text: #e8eaf6; --muted: #5a6180; }}
      body {{ background: var(--bg); font-family: 'Syne', sans-serif; color: var(--text); margin: 0; padding: 0; }}
      .container {{ padding: 20px; max-width: 500px; margin: auto; padding-bottom: 100px; }}
      .header {{ text-align: center; padding: 40px 0; font-family: 'Orbitron'; letter-spacing: 10px; font-weight: 900; font-size: 32px; color: #fff; }}
      .pulse-card {{ background: var(--surface); border: 1px solid rgba(255,255,255,0.06); padding: 30px; border-radius: 32px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 40px rgba(0,0,0,0.5); }}
      .pulse-value {{ font-size: 48px; font-weight: 800; color: var(--cyan); margin: 10px 0; }}
      .section-title {{ font-family: 'Orbitron'; font-size: 14px; letter-spacing: 2px; color: var(--cyan); margin-bottom: 20px; text-transform: uppercase; }}
      .video-item {{
        background: var(--surface); padding: 18px; border-radius: 20px; margin-bottom: 12px; 
        display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255,255,255,0.05);
      }}
      .video-rank {{ font-weight: 800; color: var(--muted); font-size: 12px; margin-right: 10px; }}
      .video-views {{ font-weight: 700; color: var(--green); }}
      .video-user {{ font-weight: 700; font-size: 14px; }}
      .bottom-nav {{ position: fixed; bottom: 0; left: 0; right: 0; background: rgba(11,14,26,0.9); backdrop-filter: blur(20px); display: flex; justify-content: space-around; padding: 20px; border-top: 1px solid rgba(255,255,255,0.05); z-index: 1000; }}
    </style>
    </head>
    <body>
    <div class="container">
      <div class="header">MURATTI</div>
      <div class="pulse-card">
        <div style="font-size: 11px; color: var(--muted); letter-spacing: 2px; font-weight: 700;">TOP 150 TOTAL VIEWS</div>
        <div class="pulse-value">{total_views}</div>
        <div style="font-size: 11px; color: var(--green); font-weight: 600;">SYSTEM LIVE</div>
      </div>
      <div class="section-title">🔝 Top 50 Proof List</div>
      <div class="video-list">
    """
    
    html_end = """
      </div>
    </div>
    <div class="bottom-nav">
      <span>🏠</span><span>📊</span><span>🎵</span><span>⚙️</span>
    </div>
    </body>
    </html>
    """
    return html_start + video_items + html_end

# --- 3. ANALİZ BAŞLATICI ---
if st.button("🚀 CANLI ANALİZİ BAŞLAT"):
    with st.spinner("Senkronize ediliyor..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            all_vids = []
            cursor = "0"
            for _ in range(5): # 150 video için 5 sayfa
                res = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": MUSIC_ID, "count": "30", "cursor": cursor})
                data = res.json().get('data', {})
                vids = data.get('videos', [])
                if not vids: break
                all_vids.extend(vids)
                cursor = data.get('cursor', '0')
                if not data.get('hasMore'): break
                time.sleep(0.1)

            top_150 = all_vids[:150]
            total_sum = sum(v.get('play_count', 0) for v in top_150)
            
            # Milyon formatı (8.4M gibi)
            display_views = f"{total_sum/1000000:.2f}M" if total_sum > 1000000 else f"{total_sum:,}"

            # Video Kartlarını Oluştur
            video_html = ""
            sorted_vids = sorted(top_150, key=lambda x: x.get('play_count', 0), reverse=True)
            for i, v in enumerate(sorted_vids[:50], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                video_html += f"""
                <div class="video-item">
                    <div style="display:flex; align-items:center;">
                        <span class="video-rank">#{i}</span>
                        <div>
                            <div class="video-user">@{u_id}</div>
                            <div style="font-size:10px;"><a href="{v_url}" target="_blank" style="color:#5a6180; text-decoration:none;">WATCH TIKTOK →</a></div>
                        </div>
                    </div>
                    <div class="video-views">{v.get('play_count', 0):,}</div>
                </div>
                """
            st.components.v1.html(get_dashboard_html(display_views, video_html), height=1200, scrolling=True)
            
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
else:
    # İlk açılış (Boş Dashboard)
    st.components.v1.html(get_dashboard_html(), height=800)

st.caption(f"DJ MURATTI | {time.strftime('%H:%M:%S')}")

import streamlit as st
import requests
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="DJ MURATTI", page_icon="🎧", layout="centered")

# --- 2. VERİ MOTORU ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

# Senin HTML Tasarımın (Buraya doğrudan gömüldü)
def get_html_layout(total_views="8.4M", video_rows=""):
    # HTML tasarımının başlangıcı
    html_start = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
      :root { --bg: #04060f; --surface: #0b0e1a; --cyan: #00f5ff; --green: #1ed760; --text: #e8eaf6; --muted: #5a6180; }
      body { background: var(--bg); font-family: 'Syne', sans-serif; color: var(--text); margin: 0; padding: 0; }
      .container { padding: 20px; max-width: 500px; margin: auto; padding-bottom: 100px; }
      .header { text-align: center; padding: 40px 0; font-family: 'Orbitron'; letter-spacing: 10px; font-weight: 900; font-size: 32px; color: #fff; text-shadow: 0 0 20px rgba(0,245,255,0.3); }
      .pulse-card { background: var(--surface); border: 1px solid rgba(255,255,255,0.06); padding: 30px; border-radius: 32px; text-align: center; position: relative; overflow: hidden; margin-bottom: 25px; }
      .pulse-value { font-size: 48px; font-weight: 800; color: var(--cyan); font-family: 'Syne'; margin: 10px 0; }
      .booking-list { margin-top: 30px; }
      .booking-row { background: var(--surface); padding: 18px; border-radius: 20px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; border: 1px solid var(--border); }
      .booking-date { font-size: 11px; color: var(--muted); font-weight: 700; text-transform: uppercase; }
      .booking-time { font-weight: 700; color: var(--green); }
      .venue-name { font-weight: 700; font-size: 15px; }
      .venue-city { font-size: 12px; color: var(--muted); }
      .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; background: rgba(11,14,26,0.8); backdrop-filter: blur(20px); display: flex; justify-content: space-around; padding: 20px; border-top: 1px solid rgba(255,255,255,0.05); }
      .nav-icon { font-size: 20px; }
    </style>
    </head>
    <body>
    <div class="container">
      <div class="header">MURATTI</div>
      <div class="pulse-card">
        <div style="font-size: 12px; color: var(--muted); letter-spacing: 2px; font-weight: 700;">TOP 150 TOTAL VIEWS</div>
        <div class="pulse-value">""" + total_views + """</div>
        <div style="font-size: 12px; color: var(--green); font-weight: 600;">LIVE SYSTEM ACTIVE</div>
      </div>
      <div class="booking-list">
    """
    
    html_end = """
      </div>
    </div>
    <div class="bottom-nav">
      <div class="nav-item">🏠</div>
      <div class="nav-item">📊</div>
      <div class="nav-item">🎵</div>
      <div class="nav-item">⚙️</div>
    </div>
    </body>
    </html>
    """
    
    return html_start + video_rows + html_end

# --- 3. UYGULAMA MANTIĞI ---

if st.button("🚀 ANALİZİ BAŞLAT"):
    with st.spinner("TikTok Veri Kasası Açılıyor..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            all_vids = []
            cursor = "0"
            for _ in range(5):
                res = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": MUSIC_ID, "count": "30", "cursor": cursor})
                data = res.json().get('data', {})
                vids = data.get('videos', [])
                if not vids: break
                all_vids.extend(vids)
                cursor = data.get('cursor', '0')
                if not data.get('hasMore'): break
                time.sleep(0.1)

            top_150 = all_vids[:150]
            total_views_sum = sum(v.get('play_count', 0) for v in top_150)
            
            video_html = ""
            sorted_vids = sorted(top_150, key=lambda x: x.get('play_count', 0), reverse=True)
            for i, v in enumerate(sorted_vids[:50], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                video_html += f"""
                <div class="booking-row">
                    <div>
                        <div class="booking-date">RANK #{i}</div>
                        <div class="booking-time">{v.get('play_count', 0):,} VIEWS</div>
                    </div>
                    <div>
                        <div class="venue-name">@{u_id}</div>
                        <div class="venue-city"><a href="{v_url}" target="_blank" style="color:#5a6180; text-decoration:none;">TIKTOK LINK →</a></div>
                    </div>
                </div>
                """
            st.markdown(get_html_layout(f"{total_views_sum:,}", video_html), unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
else:
    # Başlangıç Ekranı
    st.markdown(get_html_layout(), unsafe_allow_html=True)

st.divider()
st.caption(f"© 2026 DJ MURATTI | {time.strftime('%H:%M:%S')}")

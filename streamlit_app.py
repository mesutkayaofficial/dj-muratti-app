import streamlit as st
import requests
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="DJ MURATTI", page_icon="🎧", layout="centered")

# --- 2. VERİ MOTORU ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

# HTML İskeleti (Senin gönderdiğin tasarıma göre uyarlandı)
def render_dashboard(total_views, video_list_html):
    html_content = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Syne:wght@400;800&display=swap');
        :root {{
            --bg: #04060f; --surface: #0b0e1a; --cyan: #00f5ff; --green: #1ed760; --text: #e8eaf6;
        }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Syne', sans-serif; }}
        .header {{ text-align: center; padding: 30px 0; font-family: 'Orbitron'; letter-spacing: 8px; font-size: 32px; color: #fff; }}
        .stats-box {{ 
            background: var(--surface); border: 1px solid var(--cyan); 
            padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px;
            box-shadow: 0 0 20px rgba(0, 245, 255, 0.2);
        }}
        .views-val {{ font-size: 40px; font-weight: 800; color: var(--cyan); }}
        .video-item {{
            background: rgba(255,255,255,0.03); padding: 15px; border-radius: 12px;
            margin-bottom: 10px; border-left: 4px solid var(--green); display: flex; justify-content: space-between;
        }}
        .video-item a {{ color: var(--green); text-decoration: none; font-size: 12px; }}
    </style>
    <div class="header">MURATTI</div>
    <div class="stats-box">
        <div style="font-size: 12px; color: #888; letter-spacing: 2px;">TOP 150 TOTAL VIEWS</div>
        <div class="views-val">{total_views:,}</div>
    </div>
    <div style="margin-top: 30px;">
        <h3 style="font-family: Orbitron; font-size: 14px; margin-bottom: 15px; color: var(--cyan);">🔝 TOP 50 PROOF LIST</h3>
        {video_list_html}
    </div>
    """
    return st.markdown(html_content, unsafe_allow_html=True)

# --- 3. UYGULAMA MANTIĞI ---
if st.button("🚀 RUN TOP 150 ANALYTICS"):
    with st.spinner("Syncing with Global Database..."):
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
            total_views = sum(v.get('play_count', 0) for v in top_150)
            
            # Video Listesini HTML'e çevir
            video_rows = ""
            sorted_vids = sorted(top_150, key=lambda x: x.get('play_count', 0), reverse=True)
            for i, v in enumerate(sorted_vids[:50], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                video_rows += f"""
                <div class="video-item">
                    <div><b>#{i}</b> | {v.get('play_count', 0):,} Views</div>
                    <a href="{v_url}" target="_blank">OPEN →</a>
                </div>
                """
            
            render_dashboard(total_views, video_rows)
            
        except:
            st.error("Connection Failed.")
else:
    # Başlangıç Ekranı (Senin HTML temanda)
    st.markdown("""
    <div style="text-align:center; padding:100px 0;">
        <h1 style="font-family:Orbitron; color:#fff; letter-spacing:10px;">MURATTI</h1>
        <p style="color:#00f5ff; font-family:Syne; letter-spacing:3px;">ARTIST ANALYTICS SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption(f"© 2026 DJ MURATTI | {time.strftime('%H:%M:%S')}")

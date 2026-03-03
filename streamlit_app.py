import streamlit as st
import requests
import time

# --- 1. SAYFA VE STİL AYARLARI ---
st.set_page_config(page_title="DJ MURATTI Analytics", page_icon="🎧", layout="centered")

# Streamlit'in kendi arayüzünü gizleyip sadece senin tasarımını öne çıkarıyoruz
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0 !important;}
    .stButton>button {
        width: 100%; border-radius: 100px; height: 3.5em; 
        background: linear-gradient(90deg, #00f5ff, #1ed760); 
        color: #000; font-weight: bold; border: none; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. VERİ ÇEKME MOTORU ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

def fetch_tiktok_data():
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
    all_vids = []
    cursor = "0"
    
    # Toplam 150 video için 5 sayfa çekiyoruz (Her sayfa 30 video)
    for _ in range(5):
        try:
            res = requests.get(f"https://{HOST}/music/posts", headers=headers, params={"music_id": MUSIC_ID, "count": "30", "cursor": cursor})
            data = res.json().get('data', {})
            vids = data.get('videos', [])
            if not vids: break
            all_vids.extend(vids)
            cursor = data.get('cursor', '0')
            if not data.get('hasMore'): break
            time.sleep(0.1)
        except:
            break
    return all_vids

# --- 3. HTML DİNAMİKLEŞTİRME ---
def render_custom_html(total_views, video_list_html):
    with open("dj-muratti-analytics.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # 1. Gauge Value (Merkezdeki büyük rakam) Güncelleme
    # Örnek HTML'deki "76.3K" değerini bulup değiştiriyoruz
    html_content = html_content.replace('<div class="gauge-value">76.3K</div>', f'<div class="gauge-value">{total_views}</div>')
    
    # 2. Bölüm Başlığını "Top 50 Video" olarak güncelleme
    html_content = html_content.replace('🔝 Top 10 Video', '🔝 Top 50 Video')

    # 3. Video Listesini (videos-card içini) temizleyip yeni listeyi basma
    # HTML'deki ilk video-item'dan sonuncusuna kadar olan kısmı senin gerçek verilerinle değiştirir
    import re
    # videos-card içindeki içeriği temizlemek için regex veya string operasyonu
    start_marker = '<div class="section-header">'
    end_marker = '</div>\n\n    '
    
    parts = html_content.split('<div class="videos-card">')
    if len(parts) > 1:
        sub_parts = parts[1].split('')
        # Yeni içerik: Header + Dinamik Liste
        new_card_content = f"""
        <div class="section-header">
            <div class="section-title">🔝 Top 50 Video (Sıralı)</div>
            <div class="see-all">Toplam Analiz: 150</div>
        </div>
        {video_list_html}
        """
        html_content = parts[0] + '<div class="videos-card">' + new_card_content + '' + sub_parts[1]

    return html_content

# --- 4. ANA EKRAN ---
if st.button("🚀 CANLI ANALİZİ BAŞLAT"):
    with st.spinner("Veriler işleniyor..."):
        vids = fetch_tiktok_data()
        if vids:
            top_150 = vids[:150]
            total_sum = sum(v.get('play_count', 0) for v in top_150)
            
            # Milyon formatına çevirme (opsiyonel)
            if total_sum > 1000000:
                display_sum = f"{total_sum/1000000:.2f}M"
            else:
                display_sum = f"{total_sum:,}"

            # Video Kartları HTML'ini Oluştur
            video_html = ""
            sorted_vids = sorted(top_150, key=lambda x: x.get('play_count', 0), reverse=True)
            max_val = sorted_vids[0].get('play_count', 1) # Bar genişliği için en yüksek değer
            
            for i, v in enumerate(sorted_vids[:50], 1):
                views = v.get('play_count', 0)
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                bar_width = int((views / max_val) * 100)
                
                # Senin tasarımındaki video-item yapısına uygun üretim
                video_html += f"""
                <div class="video-item" onclick="window.open('{v_url}', '_blank')">
                    <div class="video-rank {'top' if i<=3 else ''}">#{i}</div>
                    <div class="video-thumb">🎵</div>
                    <div class="video-info">
                        <div class="video-user"><span>@{u_id}</span></div>
                        <div class="video-views">{views:,} izlenme</div>
                    </div>
                    <div class="video-bar-wrap">
                        <div class="video-bar"><div class="video-bar-fill" style="width:{bar_width}%"></div></div>
                        <div class="video-views-big">{views/1000:.0f}K</div>
                    </div>
                </div>
                """
            
            # Sonucu Render Et
            final_view = render_custom_html(display_sum, video_html)
            st.components.v1.html(final_view, height=1200, scrolling=True)
        else:
            st.error("Veri çekilemedi.")
else:
    # Başlangıçta senin hazırladığın boş tasarımı gösteriyoruz
    with open("dj-muratti-analytics.html", "r", encoding="utf-8") as f:
        st.components.v1.html(f.read(), height=1200, scrolling=True)

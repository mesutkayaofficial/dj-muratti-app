import streamlit as st
import requests
import time
import os

# --- 1. AYARLAR ---
st.set_page_config(page_title="DJ MURATTI", page_icon="🎧", layout="centered")

# --- 2. VERİ MOTORU ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.p.rapidapi.com"
MUSIC_ID = "7087325412228859906"

# HTML dosyasını okuyan ve verileri enjekte eden fonksiyon
def get_custom_dashboard(total_views="---", video_items_html=""):
    try:
        # Yüklediğin HTML dosyasını oku
        with open("dj-muratti-analytics.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # 8.4M olan yeri gerçek toplam izlenme ile değiştiriyoruz
        final_html = html_content.replace("8.4M", str(total_views))
        
        # Video listesi varsa, HTML'deki 'booking-list' içine enjekte et
        if video_items_html:
            marker = '<div class="booking-list">'
            if marker in final_html:
                parts = final_html.split(marker)
                # Örnek verileri temizleyip gerçek verileri yerleştiriyoruz
                content_after = parts[1].split("</div>", 1)[1] if "</div>" in parts[1] else ""
                final_html = parts[0] + marker + video_items_html + "</div>" + content_after
        
        return final_html
    except Exception as e:
        return f"<div style='color:white; padding:20px;'>HTML Dosyası Yüklenemedi: {e}</div>"

# --- 3. ANA UYGULAMA MANTIĞI ---

# Ana Sayfada Analiz Butonu
if st.button("🚀 TOP 150 ANALİZİNİ BAŞLAT"):
    with st.spinner("TikTok Data Vault ile senkronize ediliyor..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            all_vids = []
            cursor = "0"
            # 150 video çekmek için döngü
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
            
            # HTML tasarımındaki 'booking-row' yapısına uygun 50 video
            video_rows = ""
            sorted_vids = sorted(top_150, key=lambda x: x.get('play_count', 0), reverse=True)
            for i, v in enumerate(sorted_vids[:50], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                
                video_rows += f"""
                <div class="booking-row">
                    <div>
                        <div class="booking-date">RANK #{i}</div>
                        <div class="booking-time" style="color:#1ed760;">{v.get('play_count', 0):,} VIEWS</div>
                    </div>
                    <div>
                        <div class="venue-name">@{u_id}</div>
                        <div class="venue-city"><a href="{v_url}" target="_blank" style="color:#5a6180; text-decoration:none;">TIKTOK LINK →</a></div>
                    </div>
                    <div class="booking-fee" style="color:#00f5ff;">LIVE</div>
                </div>
                """
            
            # Sonucu göster
            st.markdown(get_custom_dashboard(f"{total_views_sum:,}", video_rows), unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
else:
    # Başlangıçta boş tasarım
    st.markdown(get_custom_dashboard(), unsafe_allow_html=True)

# --- 4. KAPANIŞ ---
st.write("")
st.divider()
st.caption(f"DJ MURATTI | System Active | {time.strftime('%H:%M:%S')}")

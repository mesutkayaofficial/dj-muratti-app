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

# HTML dosyasını yükleyen ve verileri enjekte eden fonksiyon
def get_custom_dashboard(total_views="---", video_items_html=""):
    try:
        # Yüklediğin HTML dosyasını oku
        with open("dj-muratti-analytics.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # HTML içindeki örnek verileri gerçek verilerle değiştir
        # '8.4M' olan yeri toplam izlenme ile değiştiriyoruz
        final_html = html_content.replace("8.4M", str(total_views))
        
        # Eğer video listesi oluştuysa, HTML'deki 'booking-list' içindeki örnekleri temizleyip gerçeğini basar
        if video_items_html:
            # HTML'indeki booking listesi başlangıcını bulup altına verileri ekliyoruz
            # Not: Bu kısım senin HTML yapındaki 'booking-row'ların olduğu yere enjekte edilir
            marker = '<div class="booking-list">'
            if marker in final_html:
                parts = final_html.split(marker)
                # Örnek verileri temizleyip sadece gerçek verileri koyuyoruz
                final_html = parts[0] + marker + video_items_html + "</div>" + parts[1].split("</div>", 1)[1]
        
        return final_html
    except Exception as e:
        return f"HTML dosyası okunamadı: {e}"

# --- 3. ANA UYGULAMA MANTIĞI ---

if st.button("🚀 ANALİZİ BAŞLAT"):
    with st.spinner("TikTok Data Vault ile senkronize ediliyor..."):
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        try:
            all_vids = []
            cursor = "0"
            # 150 video için 5 sayfa çekiyoruz
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
            
            # Senin HTML'indeki 'booking-row' tasarımına uygun 50 video kartı
            video_rows = ""
            sorted_vids = sorted(top_150, key=lambda x: x.get('play_count', 0), reverse=True)
            for i, v in enumerate(sorted_vids[:50], 1):
                u_id = v.get('author', {}).get('unique_id', 'user')
                v_url = f"https://www.tiktok.com/@{u_id}/video/{v.get('video_id')}"
                
                # Senin HTML tasarımındaki klas görünüme sadık kalarak:
                video_rows += f"""
                <div class="booking-row">
                    <div>
                        <div class="booking-date">RANK #{i}</div>
                        <div class="booking-time" style="color:var(--green);">{v.get('play_count', 0):,} VIEWS</div>
                    </div>
                    <div>
                        <div class="venue-name">@{u_id}</div>
                        <div class="venue-city"><a href="{v_url}" target="_blank" style="color:var(--muted); text-decoration:none;">TIKTOK LINK →</a></div>
                    </div>
                    <div class="booking-fee" style="color:var(--cyan);">LIVE</div>
                </div>
                """
            
            # Verileri enjekte et ve göster
            st.markdown(get_custom_dashboard(f"{total_views_sum:,}", video_rows), unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Veri çekme hatası: {e}")
else:
    # Başlangıçta senin boş tasarımın görünsün
    st.markdown(get_custom_dashboard(), unsafe_allow_html=True)

st.divider()
st.caption(f"DJ MURATTI | System Active | {time.strftime('%H:%M:%S')

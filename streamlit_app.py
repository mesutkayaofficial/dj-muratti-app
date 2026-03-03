import streamlit as st
import requests
import time

# --- 1. GÜVENLİK VE AYARLAR ---
st.set_page_config(page_title="DJ MURATTI HQ", page_icon="🎧", layout="centered")

def giris_kontrol():
    # Streamlit Cloud giriş bariyerini aşmak için session_state kullanımı
    if "auth" not in st.session_state:
        st.session_state.auth = False
    
    if not st.session_state.auth:
        st.markdown("<h1 style='text-align: center; color: #1ed760; font-family: sans-serif;'>DJ MURATTI HQ</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white;'>Lütfen erişim anahtarınızı giriniz.</p>", unsafe_allow_html=True)
        
        # Mobil uyumlu şifre girişi
        sifre = st.text_input("", type="password", placeholder="Şifre...")
        if st.button("SİSTEME GİRİŞ YAP"):
            if sifre == "MURATTI2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Hatalı Şifre!")
        st.stop()

giris_kontrol()

# --- 2. MODERN UI TASARIMI ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    div[data-testid="stMetric"] {
        background-color: #0a0a0a;
        border: 1px solid #1ed760;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
    }
    label[data-testid="stMetricLabel"] { color: #aaaaaa !important; font-size: 16px !important; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; font-size: 36px !important; font-weight: bold !important; }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background-color: #

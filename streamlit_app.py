import streamlit as st
import requests
import time
import pandas as pd

# --- 1. GÜVENLİK VE AYARLAR ---
st.set_page_config(page_title="DJ MURATTI TOP 150", page_icon="🎧", layout="centered")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #1ed760;'>DJ MURATTI HQ</h1>", unsafe_allow_html=True)
    sifre = st.text_input("Erişim Şifresi", type="password")
    if st.button("Giriş Yap"):
        if sifre == "MURATTI2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Hatalı Şifre!")
    st.stop()

# --- 2. MODERN DARK UI ---
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
    label[data-testid="stMetricLabel"] { color: #aaaaaa !important; }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; font-weight: bold !important; }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background-color: #1ed760;
        color: black;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("DJ MURATTI")
st.subheader("TOP 150 Performans & Arşiv")

# --- 3. AYARLAR ---
API_KEY = "49084773d8msh07a4a9c1ac5d484p108e2ejsn2cf663d07caa"
HOST = "tiktok-scraper7.

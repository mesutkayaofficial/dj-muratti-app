import streamlit as st
import requests
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="DJ MURATTI", page_icon="🎧", layout="centered")

# --- 2. ULTRA PREMIUM UI (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #111111, #000000);
        color: #ffffff;
    }
    
    /* Logo ve Marka Alanı */
    .brand-box {
        text-align: center;
        padding: 50px 0 30px 0;
    }
    
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 900;
        font-size: 52px;
        letter-spacing: 10px;
        color: #ffffff;
        text-transform: uppercase;
        margin-bottom: 0;
        animation: glow 3s infinite ease-in-out;
    }
    
    @keyframes glow {
        0% { text-shadow: 0 0 10px rgba(30, 215, 96, 0.2); }
        50% { text-shadow: 0 0 30px rgba(30, 215, 96, 0.7); transform: scale(1.02); }
        100% { text-shadow: 0 0 10px rgba(30, 215, 96, 0.2); }
    }

    .artist-tag {
        color: #1ed760;
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-top: 5px;
    }

    /* Modern Kartlar */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 25px;
        border-radius: 28px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    
    label[data-testid="stMetricLabel"] { color: #888888 !important; letter-spacing: 1px; }
    div[data-testid="stMetricValue"] { color: #1ed760 !important; font-size: 34px !important; }

    /* Neon Aksiyon Butonu */
    .stButton>button {
        width: 100%;
        border-radius: 100px;
        height: 4.2em;
        background: linear-gradient(90deg, #1ed760, #1db954);
        color: #000;
        font-weight: 900;
        font-size: 18px;
        border: none;
        box-shadow: 0 8px 25px rgba(30, 215, 96, 0.3);
        text-transform: uppercase

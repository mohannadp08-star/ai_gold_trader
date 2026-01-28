import streamlit as st
import yfinance as yf
import pandas as pd

@st.cache_data(ttl=3600)  # تخزين البيانات لمدة ساعة لتجنب Rate Limit
def fetch_gold_data():
    """
    تحميل بيانات الذهب (XAU/USD) من Yahoo Finance
    """
    try:
        df = yf.download("GC=F", period="60d", interval="1h")
        df = df.rename(columns={"Close": "XAU"})
        df = df[["XAU", "High", "Low"]].dropna()
        return df
    except Exception as e:
        st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
        return pd.DataFrame()  # إرجاع DataFrame فارغ عند الفشل

# data_fetch.py
import os
import pandas as pd
import yfinance as yf

CACHE_FILE = "gold_data.csv"

def fetch_gold_data():
    """
    تحميل بيانات الذهب (XAU/USD) من Yahoo Finance أو من ملف cache محلي
    لتجنب مشكلة Rate Limit.
    """
    if os.path.exists(CACHE_FILE):
        # قراءة البيانات من الملف المحلي
        df = pd.read_csv(CACHE_FILE, parse_dates=["Datetime"])
        print("📊 Loaded gold data from local cache.")
    else:
        try:
            # تحميل البيانات من Yahoo Finance
            df = yf.download("GC=F", period="60d", interval="1h").reset_index()
            df.rename(columns={"Close": "XAU"}, inplace=True)
            df.to_csv(CACHE_FILE, index=False)
            print("📊 Fetched gold data from Yahoo Finance and cached locally.")
        except Exception as e:
            print(f"❌ Failed to fetch gold data: {e}")
            df = pd.DataFrame()  # إرجاع DataFrame فارغ إذا فشل التحميل

    return df

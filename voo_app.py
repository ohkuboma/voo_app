import yfinance as yf
import pandas as pd
from datetime import date, timedelta
import streamlit as st

st.set_page_config(page_title="VOO 最頻値", page_icon="📈")
st.title("📈 VOO 過去30日間の最頻値（高値・安値）")

# 期間設定
today = date.today()
start_date = today - timedelta(days=30)

# データ取得
voo = yf.Ticker("VOO")
hist = voo.history(start=start_date, end=today + timedelta(days=1), interval="1d")

# 最頻値の算出
low_mode = hist["Low"].mode().iloc[0]
high_mode = hist["High"].mode().iloc[0]

# 表示
col1, col2 = st.columns(2)
col1.metric(label="🔻 安値 最頻値", value=f"${low_mode:.2f}")
col2.metric(label="🔺 高値 最頻値", value=f"${high_mode:.2f}")
st.caption(f"📅 更新日：{today}")

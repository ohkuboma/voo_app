import pandas as pd
from statistics import mode
import yfinance as yf
import streamlit as st

# VOO実データ読み込み関数（過去30営業日）
def load_voo_data():
    ticker = yf.Ticker("VOO")
    df = ticker.history(period="2mo")
    if df.empty:
        st.error("VOOのデータが取得できませんでした。")
        st.stop()
    df = df.tail(30).reset_index()
    return df[['Date', 'High', 'Low', 'Close']]

# 最頻高値・安値を求める関数
def get_voo_high_low_modes(buy_price=None):
    df = load_voo_data()
    highs = df['High'].round(2).tolist()
    lows = df['Low'].round(2).tolist()

    try:
        high_mode = mode(highs)
    except:
        high_mode = max(set(highs), key=highs.count)

    try:
        low_mode = mode(lows)
    except:
        low_mode = max(set(lows), key=lows.count)

    width_ratio = round((high_mode - low_mode) / low_mode * 100, 2)

    df['RangeRatio'] = ((df['High'] - df['Low']) / df['Low'] * 100).round(2)
    min_row = df.loc[df['RangeRatio'].idxmin()]
    max_row = df.loc[df['RangeRatio'].idxmax()]

    current_price = df.iloc[-1]['Close']

    profit_percent = None
    if buy_price is not None:
        try:
            profit_percent = round((current_price - buy_price) / buy_price * 100, 2)
        except ZeroDivisionError:
            st.error("買値が0のため利益計算できませんでした。")

    return {
        'most_frequent_high': high_mode,
        'most_frequent_low': low_mode,
        'width_ratio_percent': width_ratio,
        'min_range_day': min_row,
        'max_range_day': max_row,
        'current_price': current_price,
        'buy_price': buy_price,
        'profit_percent': profit_percent,
        'df': df
    }

# Streamlit アプリ
st.title("VOO 30日分析アプリ")

buy_price_input = st.number_input("買値を入力してください", min_value=0.0, step=0.1, value=600.0)

if st.button("計算する"):
    result = get_voo_high_low_modes(buy_price=buy_price_input)

    st.metric("最頻高値", result['most_frequent_high'])
    st.metric("最頻安値", result['most_frequent_low'])
    st.metric("値幅割合 (%)", result['width_ratio_percent'])
    st.metric("現在価格", round(result['current_price'], 2))

    if result['profit_percent'] is not None:
        st.metric("予想利益率 (%)", result['profit_percent'])

    st.subheader("📉 値幅の割合が最も小さい日")
    st.write(result['min_range_day'].to_frame().T)

    st.subheader("📈 値幅の割合が最も大きい日")
    st.write(result['max_range_day'].to_frame().T)

    st.subheader("📋 30営業日のデータ一覧")
    st.dataframe(result['df'])

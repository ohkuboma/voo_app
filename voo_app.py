    # 最頻データの表示（1行3列）
    col1, col2, col3 = st.columns(3)
    col1.metric("最頻高値", result['most_frequent_high'])
    col2.metric("最頻安値", result['most_frequent_low'])
    col3.metric("値幅割合 (%)", result['width_ratio_percent'])

    # 現在価格と利益（1行2列）
    col4, col5 = st.columns(2)
    col4.metric("現在価格", round(result['current_price'], 2))

    if result['profit_percent'] is not None:
        col5.metric("予想利益率 (%)", result['profit_percent'])

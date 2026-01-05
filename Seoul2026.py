import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 網頁基本設定
st.set_page_config(page_title="首爾行程規劃大師", layout="wide", page_icon="🗓️")

# 2. 初始化資料 (如果沒有存過的資料，就給一份預設的)
if 'itinerary_df' not in st.session_state:
    st.session_state.itinerary_df = pd.DataFrame([
        {"天數": "Day 1", "時間": "14:00", "行程內容": "抵達仁川機場", "備註": "購買 T-Money 卡"},
        {"天數": "Day 2", "時間": "10:00", "行程內容": "景福宮韓服體驗", "備註": "門票 ₩3,000 (穿韓服免費)"},
        {"天數": "Day 3", "時間": "11:00", "行程內容": "東廟市集", "備註": "週日限定"},
        {"天數": "Day 4", "時間": "09:00", "行程內容": "出發往春川", "備註": "搭乘 ITX 青春號"},
        {"天數": "Day 5", "時間": "13:00", "行程內容": "弘大商圈購物", "備註": ""},
        {"天數": "Day 6", "時間": "10:00", "行程內容": "樂天超市採買", "備註": "整理行李回程"},
    ])

# 3. 側邊欄
with st.sidebar:
    st.title("🇰🇷 旅遊管理後台")
    menu = st.radio("功能選單", ["📝 編輯行程", "🌦️ 查看天氣", "💰 旅費記帳"])
    st.divider()
    st.info("💡 編輯完行程後，記得點擊下方的『儲存變更』。")

# --- 功能：編輯行程 (這就是您要的網頁排行程功能) ---
if menu == "📝 編輯行程":
    st.header("🗓️ 規劃您的首爾行程")
    st.write("您可以直接點擊下方的表格進行修改、新增或刪除行數：")
    
    # 使用 st.data_editor 讓表格變成可編輯狀態
    edited_df = st.data_editor(
        st.session_state.itinerary_df, 
        num_rows="dynamic", # 允許使用者自行增加或減少行數
        use_container_width=True,
        column_config={
            "天數": st.column_config.SelectboxColumn(
                options=["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
            ),
            "時間": st.column_config.TimeColumn(format="HH:mm"),
        }
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 儲存並確認變更"):
            st.session_state.itinerary_df = edited_df
            st.success("行程已暫存成功！")
            
    with col2:
        # 下載功能，方便您存成 Excel 或手機備份
        csv = edited_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 下載行程備份 (Excel檔)",
            data=csv,
            file_name='seoul_trip_plan.csv',
            mime='text/csv',
        )

# --- 功能：查看天氣 (加上您要的 AccuWeather) ---
elif menu == "🌦️ 查看天氣":
    st.header("🌦️ 即時天氣預報")
    st.link_button("🌡️ 開啟 AccuWeather 詳細預報", 
                   "https://www.accuweather.com/zh/kr/seoul/226081/daily-weather-forecast/226081",
                   use_container_width=True)
    st.divider()
    st.metric("首爾今日預估", "-2 °C", "-5 °C")

# --- 功能：旅費記帳 ---
elif menu == "💰 旅費記帳":
    st.header("💰 旅費記帳 (匯率 1:46)")
    # (保留之前的記帳邏輯...)
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    
    with st.form("expense_form"):
        item = st.text_input("項目")
        amount = st.number_input("韓元 (KRW)", min_value=0)
        submitted = st.form_submit_button("新增支出")
        if submitted:
            st.session_state.expenses.append({"項目": item, "韓元": amount, "台幣": round(amount/46)})
    
    if st.session_state.expenses:
        st.table(pd.DataFrame(st.session_state.expenses))

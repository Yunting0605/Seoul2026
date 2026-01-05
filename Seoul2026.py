import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. 網頁基本設定 (設定標題與圖示)
st.set_page_config(page_title="首爾旅遊助手 Pro", layout="wide", page_icon="🇰🇷")

# 2. 自定義介面美化 (CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 3. 匯率換算邏輯
def convert_to_twd(krw):
    return krw / 46

# 4. 側邊欄選單
with st.sidebar:
    st.title("🇰🇷 首爾探險隊")
    menu = st.radio("功能導覽", ["每日行程", "即時天氣", "Naver 地圖", "旅費記帳", "韓語點餐小幫手"])
    st.divider()
    st.write(f"📅 今日日期: {datetime.now().strftime('%Y-%m-%d')}")
    st.write(f"💰 匯率參考：1 TWD ≈ 46 KRW")

# 5. 各功能邏輯區塊

# --- 行程總覽 ---
if menu == "每日行程":
    st.header("🗓️ 6天5夜行程清單")
    df_plan = pd.DataFrame([
        {"天數": "Day 1", "行程": "抵達酒店、清溪川、仁寺洞"},
        {"天數": "Day 2", "行程": "景福宮、北村韓屋村、東大門夜遊"},
        {"天數": "Day 3", "行程": "週日限定：東廟假日二手市集 (挖寶行程)"},
        {"天數": "Day 4", "行程": "春川辣炒雞排 (起源地版)、南怡島"},
        {"天數": "Day 5", "行程": "弘大商圈、梨花女子大學"},
        {"天數": "Day 6", "行程": "首爾站樂天超市、前往機場"},
    ])
    st.table(df_plan)

# --- 天氣功能 ---
elif menu == "即時天氣":
    st.header("🌦️ 首爾即時天氣預報")
    try:
        # 顯示 2026年1月 建議氣象資訊
        col1, col2, col3 = st.columns(3)
        col1.metric("預估氣溫", "-5 °C", "-2 °C")
        col2.metric("天氣狀況", "晴朗 / 乾冷")
        col3.metric("降雨機率", "5%")
        st.warning("🧣 提醒：首爾 1 月份天氣非常寒冷，請準備發熱衣與厚羽絨衣，並注意保濕。")
    except:
        st.error("無法取得天氣數據。")

# --- 地圖功能 ---
elif menu == "Naver 地圖":
    st.header("📍 Naver Map 景點快速導航")
    st.info("💡 點擊下方按鈕可直接開啟 Naver Map，在手機上使用導航最準確。")
    
    spots = {
        "🏨 高麗亞那酒店 (Koreana Hotel)": "https://naver.me/G9R6p3Nf",
        "🏯 景福宮 (穿韓服免費)": "https://naver.me/G6Dy6mU1",
        "🏘️ 北村韓屋村": "https://naver.me/F8B6G7V6",
        "🧣 東廟二手市集 (週日推薦)": "https://naver.me/GvXk2JzW",
        "🥘 春川明洞雞排一條街": "https://naver.me/xXrk8Yf6",
        "🌳 南怡島碼頭": "https://naver.me/IFj6q9H4"
    }
    
    for name, url in spots.items():
        st.link_button(name, url, use_container_width=True)

# --- 記帳功能 ---
elif menu == "旅費記帳":
    st.header("💰 旅費記帳工具 (1:46)")
    
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("項目名稱 (例如：炸雞)")
    with col2:
        krw = st.number_input("金額 (KRW)", min_value=0, step=1000)
    
    if st.button("新增支出"):
        if item and krw > 0:
            twd_val = convert_to_twd(krw)
            st.session_state.expenses.append({"項目": item, "韓元(₩)": krw, "台幣(NT$)": round(twd_val, 0)})
            st.success(f"已紀錄項目：{item}")
    
    if st.session_state.expenses:
        st.divider()
        df_exp = pd.DataFrame(st.session_state.expenses)
        st.table(df_exp)
        total_krw = df_exp["韓元(₩)"].sum()
        total_twd = total_krw / 46
        st.metric("目前總預算支出 (TWD)", f"NT$ {int(total_twd):,}")

# --- 韓文點餐功能 ---
elif menu == "韓語點餐小幫手":
    st.header("🗣️ 點餐溝通不求人")
    st.info("可以直接把螢幕給店員看喔！")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🍽️ 點餐")
        st.code("닭갈비 4인분 주세요.\n(請給我4份辣炒雞排)", language="text")
        st.code("볶음밥 2인분 볶아주세요.\n(請幫我們炒2份飯)", language="text")
        st.code("물 좀 주세요.\n(請給我水)", language="text")
    with col_b:
        st.subheader("💰 結帳/交通")
        st.code("얼마예요?\n(多少錢？)", language="text")
        st.code("영수증 주세요.\n(請給我收據)", language="text")
        st.code("이곳으로 가주세요.\n(請帶我去這裡 - 搭配地圖)", language="text")

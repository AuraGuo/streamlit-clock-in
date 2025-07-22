from datetime import datetime
import pytz
import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="簡易打卡系統", layout="centered")

RECORD_FILE = "clock_records.json"
DEFAULT_NAME = "Aura"  # 名字固定寫這

# 初始化
if not os.path.exists(RECORD_FILE):
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def get_now():
    tz = pytz.timezone("Asia/Taipei")
    return datetime.now(tz)

# 讀取紀錄
with open(RECORD_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

# 打卡動作
def save_record(name, action, date=None, time=None, is_manual=False):
    now = get_now()
    record_date = date if date else now.strftime("%Y-%m-%d")
    record_time = time if time else now.strftime("%H:%M:%S")

    note = "手動新增" if is_manual else ""

    new_record = {
        "name": name,
        "date": record_date,
        "time": record_time,
        "action": action,
        "note": note
    }
    records.insert(0, new_record)
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    st.success(f"{name} {action} 成功於 {record_date} {record_time}")
    st.rerun()



# 表單
st.title("☁ 簡易打卡系統")
st.markdown(f"☺ 使用者：**{DEFAULT_NAME}**")


with st.form("打卡表單", clear_on_submit=True):
    mode = st.selectbox("請選擇操作模式", ["即時打卡", "手動新增"])
    
    action = st.selectbox("打卡類型", ["上班", "下班"])

    manual_date = None
    manual_time = None
    
    if mode == "手動新增":
        col1, col2 = st.columns(2)
        manual_date = col1.date_input("選擇日期")
        manual_time = col2.time_input("選擇時間")

    submitted = st.form_submit_button("打卡！")
if submitted:
    is_manual = mode == "手動新增"
    if is_manual and (manual_date is None or manual_time is None):
        st.warning("請選擇日期與時間")
    else:
        save_record(
            DEFAULT_NAME,
            action,
            manual_date.strftime("%Y-%m-%d") if manual_date else None,
            manual_time.strftime("%H:%M:%S") if manual_time else None,
            is_manual=is_manual
        )

# 顯示紀錄
st.divider()
st.subheader("✉ 打卡紀錄")


# 刪除紀錄
def delete_record(index):
    if 0 <= index < len(records):
        del records[index]
        with open(RECORD_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        st.success("已刪除一筆紀錄")
        st.rerun()

DELETE_PASSWORD = "0000"  # 密碼可自行更換

if records:
    df = pd.DataFrame(records)

    #st.markdown("### 打卡紀錄")  # 表格標題

    # 加上表頭欄位
    header1, header2, header3, header4, header5, header6 = st.columns([2, 2, 2, 2, 2, 2])
    header1.markdown("**姓名**")
    header2.markdown("**日期**")
    header3.markdown("**時間**")
    header4.markdown("**類型**")
    header5.markdown("**備註**")
    header6.markdown("**操作**")
    
    for i, row in df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])
        col1.markdown(f"<div style='text-align: left'>{row['name']}</div>", unsafe_allow_html=True)
        col2.markdown(f"<div style='text-align: left'>{row['date']}</div>", unsafe_allow_html=True)
        col3.markdown(f"<div style='text-align: left'>{row['time']}</div>", unsafe_allow_html=True)
        col4.markdown(f"<div style='text-align: left'>{row['action']}</div>", unsafe_allow_html=True)
        col5.markdown(f"<div style='text-align: left'>{row.get('note', '')}</div>", unsafe_allow_html=True)
        with col6:
            if st.button("刪除", key=f"delete_{i}"):
                st.session_state["delete_index"] = i

    # 刪除密碼欄位顯示與處理邏輯
    if "delete_index" in st.session_state:
        st.warning(f"⚠️ 確認刪除第 {st.session_state['delete_index']+1} 筆資料")
        password = st.text_input("請輸入刪除密碼", type="password")
        if st.button("確認刪除"):
            if password == DELETE_PASSWORD:
                del records[st.session_state["delete_index"]]
                with open(RECORD_FILE, "w", encoding="utf-8") as f:
                    json.dump(records, f, ensure_ascii=False, indent=2)
                st.success("✅ 已刪除資料")
                del st.session_state["delete_index"]
                st.rerun()
            else:
                st.error("❌ 密碼錯誤")
else:
    st.info("目前尚無紀錄")

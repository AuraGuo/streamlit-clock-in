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
def save_record(action):
    now = get_now()
    new_record = {
        "name": DEFAULT_NAME,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "action": action,
    }
    records.insert(0, new_record)
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    st.success(f"{action} 成功於 {new_record['date']} {new_record['time']}")
    st.rerun()



# 表單
st.title("☁ 簡易打卡系統")
st.markdown(f"☺ 使用者：**{DEFAULT_NAME}**")


with st.form("打卡表單", clear_on_submit=True):
    action = st.selectbox("請選擇打卡類型", ["上班", "下班"])
    submitted = st.form_submit_button("打卡！")
    if submitted:
        save_record(action)

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
    for i, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        col1.write(row["name"])
        col2.write(row["date"])
        col3.write(row["time"])
        col4.write(row["action"])
        with col5:
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

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="簡易打卡系統", layout="centered")

RECORD_FILE = "clock_records.json"
DEFAULT_NAME = "Aura"  # 你的名字固定寫這

# 初始化
if not os.path.exists(RECORD_FILE):
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# 讀取紀錄
with open(RECORD_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

# 打卡動作
def save_record(action):
    now = datetime.now()
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

# 刪除紀錄
def delete_record(index):
    if 0 <= index < len(records):
        del records[index]
        with open(RECORD_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        st.success("已刪除一筆紀錄")
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

if records:
    for idx, record in enumerate(records):
        col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 2, 1])
        col1.write(record["name"])
        col2.write(record["date"])
        col3.write(record["time"])
        col4.write(record["action"])
        if col5.button("刪除", key=f"del-{idx}"):
            delete_record(idx)
else:
    st.info("目前尚無紀錄")

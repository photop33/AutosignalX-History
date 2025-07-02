import streamlit as st
import subprocess
import os
import pandas as pd
from datetime import datetime, time

PYTHON_PATH = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
LOG_PATH = os.path.join("logs", "monitor_output.txt")
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config.py"))

# טען קונפיג נוכחי
config_vars = {}
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    exec(f.read(), config_vars)

st.title("🧠 מערכת ניטור סיגנלים + בדיקת TP/SL")
st.code(f"🔧 Python Executable: {PYTHON_PATH}")

# --- הגדרות טווח ניתוח ואינטרוול בלבד ---
st.header("🛠️ הגדרות טווח ניתוח ואינטרוול")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("תאריך התחלה", value=pd.to_datetime(config_vars.get("start_time_str", datetime.now())))
    start_time = st.time_input("שעת התחלה", value=(pd.to_datetime(config_vars.get("start_time_str", datetime.now())).time() if config_vars.get("start_time_str") else time(0, 0)))
with col2:
    end_date = st.date_input("תאריך סיום", value=pd.to_datetime(config_vars.get("end_time_str", datetime.now())))
    end_time = st.time_input("שעת סיום", value=(pd.to_datetime(config_vars.get("end_time_str", datetime.now())).time() if config_vars.get("end_time_str") else time(23, 59)))

start_time_str = f"{start_date} {start_time.strftime('%H:%M')}"
end_time_str = f"{end_date} {end_time.strftime('%H:%M')}"

interval_options = ["1m", "5m", "15m", "30m", "1h", "4h", "8h", "12h", "1d", "1w", "1y"]
interval = st.selectbox("interval", interval_options, index=interval_options.index(config_vars.get("interval", "1d")) if config_vars.get("interval", "1d") in interval_options else 8)

symbol = st.text_input("symbol (השאר ריק לריצה על כל הסימבולים)", config_vars.get("symbol", ""))

if st.button("💾 שמור הגדרות ניטור"):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config_code = f.read()
    local_vars = {}
    exec(config_code, local_vars)

    local_vars["symbol"] = symbol if symbol.strip() else None
    local_vars["interval"] = interval
    local_vars["start_time_str"] = start_time_str
    local_vars["end_time_str"] = end_time_str

    def format_val(val):
        if val is None:
            return "None"
        if isinstance(val, str):
            return f'"{val}"'
        return str(val)

    config_txt = ""
    for k, v in local_vars.items():
        if k.startswith("__"):
            continue
        config_txt += f"{k} = {format_val(v)}\n"

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(config_txt)

    st.success("ההגדרות נשמרו!")

st.divider()

if st.button("🚀 הרץ ניטור וסגירת סיגנלים"):
    with st.spinner("🧠 מריץ startagy_program.py..."):
        os.makedirs("logs", exist_ok=True)
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            subprocess.run([PYTHON_PATH, "startagy_program.py"], stdout=f, stderr=subprocess.STDOUT, text=True)

    with st.spinner("📈 מריץ st_or_tp.py..."):
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            subprocess.run([PYTHON_PATH, "st_or_tp.py"], stdout=f, stderr=subprocess.STDOUT, text=True)

    st.subheader("📄 פלט ההרצה:")
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        st.code(f.read())

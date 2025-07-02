import pandas as pd
import streamlit as st
import os
import subprocess
from datetime import datetime, time
# נתיב config
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config.py"))
PYTHON_PATH = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
VOLATILE_FILE = os.path.join("logs", "volatile_symbols.txt")

# -- טען ערכים נוכחיים --
config_vars = {}
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    exec(f.read(), config_vars)

st.title("🔍 מערכת סריקה")
st.header("⚙️ הגדרות סריקה")

# --- SCAN_FROM ו-SCAN_TO באותה שורה עם תאריך ושעה ---
col1, col2 = st.columns(2)

with col1:
    scan_from_date = st.date_input("SCAN_FROM - תאריך", value=pd.to_datetime(config_vars.get("SCAN_FROM", datetime.now())))
    scan_from_time = st.time_input("שעה התחלה", value=(pd.to_datetime(config_vars.get("SCAN_FROM", datetime.now())).time() if config_vars.get("SCAN_FROM") else time(0, 0)))

with col2:
    scan_to_date = st.date_input("SCAN_TO - תאריך", value=pd.to_datetime(config_vars.get("SCAN_TO", datetime.now())))
    scan_to_time = st.time_input("שעה סיום", value=(pd.to_datetime(config_vars.get("SCAN_TO", datetime.now())).time() if config_vars.get("SCAN_TO") else time(23, 59)))

SCAN_FROM = f"{scan_from_date} {scan_from_time.strftime('%H:%M')}"
SCAN_TO = f"{scan_to_date} {scan_to_time.strftime('%H:%M')}"

# --- INTERVAL selectbox ---
interval_options = ["1m", "5m", "15m", "30m", "1h", "4h", "8h", "12h", "1d", "1w", "1y"]
INTERVAL = st.selectbox("INTERVAL", interval_options, index=interval_options.index(config_vars.get("INTERVAL", "1h")) if config_vars.get("INTERVAL", "1h") in interval_options else 4)

# --- שאר השדות ---
VOLATILITY_THRESHOLD = st.number_input("VOLATILITY_THRESHOLD (0 = כבוי)", value=config_vars.get("VOLATILITY_THRESHOLD") or 0.0)
PCT_CHANGE_THRESHOLD = st.number_input("PCT_CHANGE_THRESHOLD (0 = כבוי)", value=config_vars.get("PCT_CHANGE_THRESHOLD") or 0.0)
MIN_VOLUME = st.number_input("MIN_VOLUME", value=config_vars.get("MIN_VOLUME") or 0)
FILTER_MODE = st.selectbox("FILTER_MODE", ["AND", "OR"], index=0 if config_vars.get("FILTER_MODE") == "AND" else 1)

if st.button("💾 שמור הגדרות סריקה"):
    # קריאת כל הקונפיג, עדכון רק שדות נבחרים, שמירה חזרה (לא מוחקים שדות קיימים אחרים)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config_code = f.read()
    local_vars = {}
    exec(config_code, local_vars)
    # עדכון שדות
    local_vars["SCAN_FROM"] = SCAN_FROM
    local_vars["SCAN_TO"] = SCAN_TO
    local_vars["INTERVAL"] = INTERVAL
    local_vars["VOLATILITY_THRESHOLD"] = VOLATILITY_THRESHOLD
    local_vars["PCT_CHANGE_THRESHOLD"] = PCT_CHANGE_THRESHOLD
    local_vars["MIN_VOLUME"] = MIN_VOLUME
    local_vars["FILTER_MODE"] = FILTER_MODE

    def format_val(val):
        if isinstance(val, str):
            return f'"{val}"'
        return str(val)

    config_txt = ""
    for k, v in local_vars.items():
        if k.startswith("__"): continue
        config_txt += f"{k} = {format_val(v)}\n"

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(config_txt)

    st.success("ההגדרות נשמרו!")

st.divider()  # מפריד יפה בין אזור הגדרות לאזור ריצה

# ---- חלק תחתון: כפתור סריקה ----
st.header("🚀 הרצת סריקה בפועל")
st.code(f"🔧 Python Executable: {PYTHON_PATH}")

if st.button("🚀 הרץ סריקה (scan.py)"):
    with st.spinner("מריץ סריקה..."):
        result = subprocess.run([PYTHON_PATH, "scan.py"], capture_output=True, text=True)
        st.subheader("📄 פלט ההרצה:")
        st.code(result.stdout)
        if result.stderr:
            st.error(result.stderr)

        if os.path.exists(VOLATILE_FILE):
            st.subheader("🪙 מטבעות תנודתיים שנמצאו:")
            with open(VOLATILE_FILE, "r", encoding="utf-8") as f:
                symbols = f.read().splitlines()
                st.write(symbols)
        else:
            st.warning("⚠️ לא נמצא קובץ volatile_symbols.txt")

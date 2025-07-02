
import streamlit as st
import os
import ast

# נתיב לקובץ config.py
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config.py"))
st.title("⚙️ עריכת קובץ config.py")
st.caption(f"📄 נתיב: {CONFIG_PATH}")

if not os.path.exists(CONFIG_PATH):
    st.error("❌ הקובץ config.py לא נמצא.")
    st.stop()

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config_code = f.read()

# הפקה של משתנים רלוונטיים
config_vars = {}
exec(config_code, config_vars)

# קלטים רלוונטיים
st.subheader("🔍 הגדרות סריקה")
SCAN_FROM = st.text_input("SCAN_FROM", config_vars.get("SCAN_FROM", ""))
SCAN_TO = st.text_input("SCAN_TO", config_vars.get("SCAN_TO", ""))
INTERVAL = st.text_input("INTERVAL", config_vars.get("INTERVAL", ""))

st.subheader("⚙️ פילטרים")
VOLATILITY_THRESHOLD = st.number_input("VOLATILITY_THRESHOLD", value=config_vars.get("VOLATILITY_THRESHOLD") or 0.0)
PCT_CHANGE_THRESHOLD = st.number_input("PCT_CHANGE_THRESHOLD", value=config_vars.get("PCT_CHANGE_THRESHOLD") or 0.0)
MIN_VOLUME = st.number_input("MIN_VOLUME", value=config_vars.get("MIN_VOLUME") or 0)
FILTER_MODE = st.selectbox("FILTER_MODE", ["AND", "OR"], index=0 if config_vars.get("FILTER_MODE") == "AND" else 1)

st.subheader("🧠 אינדיקטורים")
symbol = st.text_input("symbol", config_vars.get("symbol", ""))
interval = st.text_input("interval", config_vars.get("interval", ""))
start_time_str = SCAN_FROM
end_time_str = SCAN_TO

st.subheader("🎯 אסטרטגיות")
ACTIVE_STRATEGIES = st.text_area("ACTIVE_STRATEGIES (רשימה מופרדת בפסיקים)", ", ".join(config_vars.get("ACTIVE_STRATEGIES", [])))

st.subheader("🛡️ הגדרות SL/TP")
SL_MULTIPLIER = st.number_input("SL_MULTIPLIER", value=config_vars.get("SL_MULTIPLIER", 1.5))
RR_RATIO = st.number_input("RR_RATIO", value=config_vars.get("RR_RATIO", 2.0))

if st.button("💾 שמור קובץ"):
    try:
        content = f"""# config.py

SCAN_FROM= "{SCAN_FROM}"
SCAN_TO= "{SCAN_TO}"
INTERVAL= "{INTERVAL}"

VOLATILITY_THRESHOLD = {VOLATILITY_THRESHOLD if VOLATILITY_THRESHOLD else 'None'}
PCT_CHANGE_THRESHOLD = {PCT_CHANGE_THRESHOLD}
MIN_VOLUME = {MIN_VOLUME}
FILTER_MODE = "{FILTER_MODE}"

symbol = "{symbol}"
interval = "{interval}"
start_time_str = SCAN_FROM
end_time_str = SCAN_TO

INDICATOR_CONDITIONS = {{
    "rsi": {{"oversold": 30, "overbought": 70}},
    "macd": {{"signal_diff_min": 0.0}}
}}

SL_MULTIPLIER = {SL_MULTIPLIER}
RR_RATIO = {RR_RATIO}

ACTIVE_STRATEGIES = [{", ".join([f'"{s.strip()}"' for s in ACTIVE_STRATEGIES.split(",") if s.strip()])}]

STRATEGY_THRESHOLDS = {{
    {chr(10).join([f'"{s.strip()}": 1,' for s in ACTIVE_STRATEGIES.split(",") if s.strip()])}
}}
"""
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        st.success("✅ הקובץ נשמר בהצלחה!")
    except Exception as e:
        st.error(f"שגיאה בשמירה: {e}")

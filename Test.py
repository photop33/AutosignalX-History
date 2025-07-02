import requests
from datetime import datetime
def to_ms(dt_str): return int(datetime.strptime(dt_str, "%Y-%m-%d %H:%M").timestamp() * 1000)

BINANCE_API = "https://api.binance.com"
symbol = "ETHUSDT"
interval = "1h"
start = "2025-06-27 00:00"
end = "2025-06-29 23:59"

params = {
    "symbol": symbol,
    "interval": interval,
    "startTime": to_ms(start),
    "endTime": to_ms(end),
    "limit": 1000
}

r = requests.get(f"{BINANCE_API}/api/v3/klines", params=params)
print(f"Status code: {r.status_code}")
data = r.json()
print(f"Number of candles: {len(data)}")
print(data[:3])  # תראה שלוש שורות לדוגמה

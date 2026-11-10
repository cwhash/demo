import json

import pandas as pd
import yfinance as yf

# ===== 可以現場修改的設定 =====
SYMBOL = "0050.TW"  # 2330.TW 台積電 / 2317.TW 鴻海 / 0050.TW 元大台灣50
NAME = "元大台灣50"
MA = [5, 20]        # 均線天數
SHOW = 1            # 顯示最近幾個月
# =============================

# 多抓 3 個月，讓均線一開始就有值
df = yf.Ticker(SYMBOL).history(period=f"{SHOW + 3}mo")
if df.empty:
    raise SystemExit(f"抓不到 {SYMBOL} 的資料")

for n in MA:
    df[f"MA{n}"] = df["Close"].rolling(n).mean()
df["Change"] = df["Close"].diff()
df["ChangePct"] = df["Close"].pct_change() * 100

df = df[df.index > df.index[-1] - pd.DateOffset(months=SHOW)]
df = df.drop(columns=["Dividends", "Stock Splits"], errors="ignore").round(2)
df.index = df.index.strftime("%Y-%m-%d")

data = {
    "symbol": SYMBOL,
    "name": NAME,
    "ma": MA,
    "rows": json.loads(df.reset_index().to_json(orient="records")),
}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

last = data["rows"][-1]
print(f"{NAME} {SYMBOL}：{len(data['rows'])} 筆，最新 {last['Date']} 收盤 {last['Close']}")

"""抓股價日 K、算均線，輸出 data.json 給 index.html 畫圖。

執行：python fetch.py
"""
import json
import os

import pandas as pd
import yfinance as yf

# ===== ✏️ Demo 可以現場修改的設定 =====
# 改完存檔，在終端機執行 python fetch.py，再重新整理預覽
SYMBOL = os.getenv("SYMBOL", "0050.TW")    # 股票代號：2330.TW 台積電 / 2317.TW 鴻海 / 0050.TW 元大台灣50
NAME = os.getenv("NAME", "元大台灣50")     # 網頁標題顯示的名稱
MA = [5, 20]                               # 均線天數，例如 [10, 60]
SHOW = 1                                   # 顯示最近幾個月，例如 3
# =====================================
# os.getenv 讓 CI 的 matrix 可以用環境變數換股票；沒設定時就用上面的預設值

# 多抓 3 個月，讓均線在顯示區間的第一天就有值
df = yf.Ticker(SYMBOL).history(period=f"{SHOW + 3}mo")
if df.empty:
    raise SystemExit(f"抓不到 {SYMBOL} 的資料")  # 結束碼非 0 → Actions 會變紅燈

# 計算均線、漲跌
for n in MA:
    df[f"MA{n}"] = df["Close"].rolling(n).mean()
df["Change"] = df["Close"].diff()
df["ChangePct"] = df["Close"].pct_change() * 100

# 只留最近 SHOW 個月
df = df[df.index > df.index[-1] - pd.DateOffset(months=SHOW)]
df = df.drop(columns=["Dividends", "Stock Splits", "Capital Gains"], errors="ignore").round(2)
df.index = df.index.strftime("%Y-%m-%d")

# 輸出 data.json
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

# GitHub Actions 的 Job Summary：寫進這個檔案的 Markdown 會顯示在執行結果頁
# 在本機或 Codespace 執行時沒有這個環境變數，就會略過
if summary := os.getenv("GITHUB_STEP_SUMMARY"):
    with open(summary, "a", encoding="utf-8") as f:
        f.write(
            f"### 📈 {NAME}（{SYMBOL}）\n\n"
            "| 日期 | 收盤 | 漲跌 | 成交量(張) |\n|---|---:|---:|---:|\n"
            f"| {last['Date']} | {last['Close']:,} | {last['Change']:+} ({last['ChangePct']:+}%) "
            f"| {last['Volume'] // 1000:,} |\n\n"
            f"共 {len(data['rows'])} 個交易日，均線 {', '.join(f'MA{n}' for n in MA)}\n"
        )

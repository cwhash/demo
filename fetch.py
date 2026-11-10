"""抓指定股票、指定區間的日 K，算均線，輸出 data.json 給 index.html 畫圖。

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
START = "2026-10-01"                       # 區間開始日（含）
END = "2026-10-31"                         # 區間結束日（含）
MA = [5, 20]                               # 均線天數，例如 [10, 60]
# =====================================
# os.getenv 讓 CI 的 matrix 可以用環境變數換股票；沒設定時就用上面的預設值

start, end = pd.Timestamp(START), pd.Timestamp(END)

# 往前多抓 120 天讓均線在區間第一天就有值；yfinance 的 end 不含當天，所以加 1 天
# auto_adjust=False：用原始收盤價，不受日後除權息調整影響，固定區間的數字才不會變
df = yf.Ticker(SYMBOL).history(
    start=start - pd.Timedelta(days=120), end=end + pd.Timedelta(days=1), auto_adjust=False
)
if df.empty:
    raise SystemExit(f"抓不到 {SYMBOL} 的資料")  # 結束碼非 0 → Actions 會變紅燈

# 計算均線、漲跌
for n in MA:
    df[f"MA{n}"] = df["Close"].rolling(n).mean()
df["Change"] = df["Close"].diff()
df["ChangePct"] = df["Close"].pct_change() * 100

# 只留 START ~ END
df.index = df.index.tz_localize(None)
df = df[df.index >= start]
if df.empty:
    raise SystemExit(f"{START} ~ {END} 之間沒有 {SYMBOL} 的交易資料")
df = df.drop(columns=["Adj Close", "Dividends", "Stock Splits", "Capital Gains"], errors="ignore").round(2)
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

first, last = data["rows"][0], data["rows"][-1]
print(f"{NAME} {SYMBOL}：{first['Date']} ~ {last['Date']} 共 {len(data['rows'])} 筆，最後收盤 {last['Close']}")

# GitHub Actions 的 Job Summary：寫進這個檔案的 Markdown 會顯示在執行結果頁
# 在本機或 Codespace 執行時沒有這個環境變數，就會略過
if summary := os.getenv("GITHUB_STEP_SUMMARY"):
    with open(summary, "a", encoding="utf-8") as f:
        f.write(
            f"### 📈 {NAME}（{SYMBOL}）\n\n"
            f"區間 {first['Date']} ~ {last['Date']}，共 {len(data['rows'])} 個交易日\n\n"
            "| 日期 | 收盤 | 漲跌 | 成交量(張) |\n|---|---:|---:|---:|\n"
            f"| {last['Date']} | {last['Close']:,} | {last['Change']:+} ({last['ChangePct']:+}%) "
            f"| {last['Volume'] // 1000:,} |\n"
        )

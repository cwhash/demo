# 股價看板 demo

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/cwhash/demo?quickstart=1)

台積電（2330）最近一個月的 K 線、均線與成交量。

- 網站：https://cwhash.github.io/demo/
- 資料：GitHub Actions 每個交易日 14:17（台灣時間）自動抓取 Yahoo Finance 日 K，產生 `data.json` 後直接部署到 GitHub Pages（資料不 commit 進 repo）

## 檔案

| 檔案 | 用途 |
|---|---|
| `fetch.py` | 抓資料、算均線，輸出 `data.json` |
| `index.html` | 讀 `data.json` 畫圖 |
| `.github/workflows/update.yml` | 排程 / 手動 / 合併後：抓資料 → 部署 Pages |
| `.github/workflows/ci.yml` | PR 時檢查 `fetch.py` 能正常產生資料 |
| `.devcontainer/devcontainer.json` | Codespaces 環境：自動安裝套件、抓資料、啟動預覽 |

## 在 Codespaces 試試看

點上方按鈕開啟 Codespace，網站會自動出現在右側預覽。改完程式後在終端機執行：

```bash
python fetch.py
```

再重新整理預覽即可。

- 換股票：`fetch.py` 的 `SYMBOL = "2317.TW"`、`NAME = "鴻海"`
- 改均線：`MA = [10, 60]`
- 改區間：`SHOW = 3`
- 改顏色：`index.html` 開頭的 `--up` / `--down`
- 分享預覽：Ports 面板 → 8000 → 右鍵 → Port Visibility → Public

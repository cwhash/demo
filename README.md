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

---

## Demo 流程（約 15 分鐘）

主軸：**Codespaces 負責「寫」，Actions 負責「跑」**。不用在本機裝任何東西就能改程式；改完之後的檢查、部署、每日更新全部自動完成。

### 1. 開場：看網站（2 分鐘）

1. 打開 https://cwhash.github.io/demo/
2. 說明：K 線、均線、成交量都是 GitHub Actions 自動抓的，沒有後端、沒有資料庫

### 2. GitHub Actions（3 分鐘）

1. 打開 repo 的 **Actions** 頁籤，看「更新資料並部署網站」的執行紀錄
2. 打開 `.github/workflows/update.yml`，講三種觸發方式：
   - `schedule`：每個交易日 14:17 自動跑（cron 用 UTC，所以寫 `17 6 * * 1-5`）
   - `workflow_dispatch`：手動按鈕
   - `push`：合併到 main 後自動部署；`paths-ignore` 讓只改 README 時不重跑
3. 按 **Run workflow** 手動觸發，點進去看 log：抓資料 → 部署 Pages，約 30 秒完成

### 3. Codespaces：一鍵開環境（2 分鐘）

1. 點 README 上的 **Open in GitHub Codespaces** 按鈕
2. 說明 `.devcontainer/devcontainer.json` 自動做了什麼：
   - 準備好 Python 3.12
   - 安裝套件、抓一次資料
   - 啟動網站並在右側開預覽

### 4. Codespaces：現場修改（4 分鐘）

每改完 `fetch.py` 就在終端機執行 `python fetch.py`，再重新整理預覽。

| 順序 | 修改 | 檔案 | 改成 |
|---|---|---|---|
| 1 | 換股票 | `fetch.py` | `SYMBOL = "2317.TW"`、`NAME = "鴻海"` |
| 2 | 改均線 | `fetch.py` | `MA = [10, 60]` |
| 3 | 改顏色 | `index.html` | `--up` / `--down` 對調（美股綠漲紅跌） |

### 5. Codespaces：分享 port（1 分鐘）

1. 打開下方 **Ports** 面板
2. 8000 → 右鍵 → **Port Visibility → Public**
3. 把網址給觀眾，用手機看正在修改的網站

### 6. 串起來：開 PR 跑 CI（3 分鐘）

1. 在 Codespace 左側 **Source Control** 面板開新分支、commit
2. 發 PR，回到 GitHub 看 `ci.yml` 自動執行
3. CI 綠燈 = 程式能正常抓到資料
4. ⚠️ 換了股票的 PR **不要合併**，否則正式網站會變成鴻海；展示完直接關閉 PR

### Demo 前檢查

- [ ] 14:30 後手動 Run workflow 一次，讓網站顯示當日收盤
- [ ] 預先開好一個 Codespace，確認預覽、分享 port、開 PR 都正常
- [ ] demo 結束後停止或刪除 Codespace，避免用掉免費額度

---

僅供展示，非投資建議。

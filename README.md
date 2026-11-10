# 股價看板 demo

[![更新資料並部署網站](https://github.com/cwhash/demo/actions/workflows/update.yml/badge.svg)](https://github.com/cwhash/demo/actions/workflows/update.yml)
[![CI](https://github.com/cwhash/demo/actions/workflows/ci.yml/badge.svg)](https://github.com/cwhash/demo/actions/workflows/ci.yml)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/cwhash/demo?quickstart=1)

台股最近一個月的 K 線、均線與成交量，用來展示 **GitHub Actions** 與 **Codespaces**。

- 網站：https://cwhash.github.io/demo/
- 資料：GitHub Actions 每個交易日 14:17（台灣時間）自動抓取 Yahoo Finance 日 K，產生 `data.json` 後直接部署到 GitHub Pages（資料不 commit 進 repo）

## 檔案

標有 ✏️ 的地方是 demo 時可以直接修改的設定。

| 檔案 | 用途 |
|---|---|
| `fetch.py` | 抓資料、算均線，輸出 `data.json`；在 Actions 裡另外寫 Job Summary |
| `index.html` | 讀 `data.json` 畫 K 線、卡片、表格 |
| `.github/workflows/update.yml` | 排程 / 手動 / 合併後：抓資料 → 部署 Pages |
| `.github/workflows/ci.yml` | PR 時用 matrix 同時檢查三檔股票 |
| `.devcontainer/devcontainer.json` | Codespaces 環境：自動安裝套件、抓資料、啟動預覽 |

## 可以修改的設定

| 想改什麼 | 檔案 | 改法 | 之後要做 |
|---|---|---|---|
| 換股票 | `fetch.py` | `SYMBOL`、`NAME`，例如 `"2330.TW"`、`"台積電"` | `python fetch.py` → 重新整理 |
| 改均線 | `fetch.py` | `MA = [10, 60]` | `python fetch.py` → 重新整理 |
| 改區間 | `fetch.py` | `SHOW = 3` | `python fetch.py` → 重新整理 |
| 改顏色 | `index.html` | `--up` / `--down` 對調 | 重新整理 |
| 表格天數 | `index.html` | `const ROWS = 10` | 重新整理 |
| 排程時間 | `update.yml` | `cron`（UTC，台灣時間 −8 小時） | commit 到 main |
| CI 測哪些股票 | `ci.yml` | `matrix.include` 增減 | 開 PR |
| 加工具到環境 | `devcontainer.json` | 取消 `features` 那行的註解 | Rebuild Container |

---

## Demo 流程（約 18 分鐘）

主軸：**Codespaces 負責「寫」，Actions 負責「跑」**。不用在本機裝任何東西就能改程式；改完之後的檢查、部署、每日更新全部自動完成。

### 1. 開場：看網站（2 分鐘）

1. 打開 https://cwhash.github.io/demo/
2. 說明：K 線、均線、成交量都是 GitHub Actions 自動抓的，沒有後端、沒有資料庫
3. 指出 README 最上方的狀態徽章：綠色代表最近一次執行成功

### 2. GitHub Actions（4 分鐘）

1. 打開 `.github/workflows/update.yml`，照著註解講：
   - **觸發條件**：`schedule` 排程、`workflow_dispatch` 手動、`push` 合併後自動部署；`paths-ignore` 讓只改 README 時不重跑
   - **權限**：只給需要的；`id-token` 讓部署不用存密碼
   - **steps**：大多直接套用 Marketplace 現成的 action，`cache: pip` 加速安裝
2. 打開 **Actions** 頁籤 → 「更新資料並部署網站」→ **Run workflow**
3. 跑完點進去，上方 **Summary** 直接顯示今天的收盤表格（Job Summary），不用翻 log
4. repo 首頁右側 **Deployments** 可以看到每次部署紀錄

### 3. Codespaces：一鍵開環境（2 分鐘）

1. 點 README 上的 **Open in GitHub Codespaces**
2. 打開 `.devcontainer/devcontainer.json`，照著註解講：基礎 image、建立時安裝套件並抓資料、自動開預覽

### 4. Codespaces：現場修改（4 分鐘）

1. **換股票**：`fetch.py` 的 `SYMBOL`、`NAME` → 終端機 `python fetch.py` → 重新整理預覽
2. **改均線**：`MA = [10, 60]` → `python fetch.py` → 重新整理
3. **改顏色**：`index.html` 的 `--up` / `--down` 對調 → 重新整理

### 5. Codespaces：分享 port（1 分鐘）

1. 打開下方 **Ports** 面板
2. 8000 → 右鍵 → **Port Visibility → Public**
3. 把網址給觀眾，用手機看正在修改的網站

### 6. 串起來：開 PR 跑 CI（3 分鐘）

1. 在 Codespace 左側 **Source Control** 面板開新分支、commit
2. 發 PR，回到 GitHub：`ci.yml` 用 **matrix** 同時跑三個 job（三檔股票平行檢查）
3. 點進任一個 job，Summary 一樣有該檔股票的收盤表格
4. ⚠️ 換了股票的 PR **不要合併**，否則正式網站也會跟著換；展示完直接關閉 PR

### 7. 加碼：環境即程式碼（2 分鐘）

1. `devcontainer.json` 取消 `"features"` 那行的註解，存檔
2. 右下角通知點 **Rebuild**（或 `Ctrl+Shift+P` → **Codespaces: Rebuild Container**）
3. 重建約 1–2 分鐘，趁空檔說明：這個檔案 commit 之後，團隊每個人開 Codespace 都會拿到同樣的環境
4. 完成後終端機輸入 `node -v`，Node.js 已經裝好
5. 改過的檔案都還在；重建後預覽會自動重新啟動

### Demo 前檢查

- [ ] 14:30 後手動 Run workflow 一次，讓網站顯示當日收盤
- [ ] 預先開好一個 Codespace，確認預覽、分享 port、開 PR 都正常
- [ ] 開一個測試 PR，確認 CI 三個 job 都綠燈，然後關閉
- [ ] demo 結束後停止或刪除 Codespace，避免用掉免費額度

# 股價看板 demo

[![CI](https://github.com/cwhash/demo/actions/workflows/ci.yml/badge.svg)](https://github.com/cwhash/demo/actions/workflows/ci.yml)
[![部署](https://github.com/cwhash/demo/actions/workflows/deploy.yml/badge.svg)](https://github.com/cwhash/demo/actions/workflows/deploy.yml)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/cwhash/demo?quickstart=1)

**Codespaces 負責「寫」，Actions 負責「跑」。**

網站：https://cwhash.github.io/demo/

---

## GitHub Actions

GitHub 內建的自動化工具：**某件事發生時，自動在雲端機器上執行指定的步驟**。
設定寫在 `.github/workflows/*.yml`，跟程式碼一起版本控制。

### 主要功能

| 功能 | 說明 | 本專案用在哪 |
|---|---|---|
| 觸發條件 | push、PR、排程（cron）、手動按鈕等 | `ci.yml`：PR 時；`deploy.yml`：合併後、手動 |
| CI（持續整合） | 每次改程式自動檢查，有問題就紅燈 | `ci.yml` 檢查 `fetch.py` 能否抓到資料 |
| CD（持續部署） | 檢查通過後自動部署 | `deploy.yml` 部署到 GitHub Pages |
| Matrix | 同一份設定用不同參數平行執行 | CI 同時檢查三檔股票 |
| Marketplace | 直接套用別人寫好的步驟 | `actions/checkout`、`setup-python`、`deploy-pages` |
| Job Summary | 執行結果頁顯示自訂的 Markdown 報告 | 顯示當日收盤表格 |

### 收費方式

| | 公開 repo | 私人 repo |
|---|---|---|
| GitHub 提供的標準機器 | **免費** | 每月免費額度：Free 方案 $12、Pro 方案 $18（美元） |
| 自己的機器（self-hosted） | 免費 | 免費 |

超過免費額度後依分鐘計費（美元／分鐘）：

| 機器 | 價格 | Free 方案 $12 約可用 |
|---|---|---|
| Linux 2 核 | $0.006 | 2,000 分鐘 |
| Windows 2 核 | $0.010 | 1,200 分鐘 |
| macOS | $0.062 | 190 分鐘 |

- 沒有綁信用卡：用完額度就停止，**不會被扣款**
- 有綁信用卡：可以設定預算上限，用到 90%、100% 時寄信通知
- 本專案是公開 repo，用 Linux 機器，**完全免費**

---

## GitHub Codespaces

**雲端開發環境**：在瀏覽器裡開一個完整的 VS Code，背後是一台雲端 Linux 機器。
本機什麼都不用裝，打開就能寫程式、跑程式。

### 主要功能

| 功能 | 說明 | 本專案用在哪 |
|---|---|---|
| 一鍵開環境 | 從 repo 頁面或 README 按鈕直接開啟 | README 上方的按鈕 |
| 環境即程式碼 | 用 `devcontainer.json` 定義環境，每個人打開都一樣 | 自動裝 Python 套件、抓資料、開預覽 |
| Port 轉發 | 在雲端跑的網站，直接在瀏覽器預覽 | 8000 port 自動開預覽 |
| 分享 port | 把預覽網址公開給別人看 | 讓觀眾用手機看正在改的網站 |
| 內建工具 | 已裝好 Git、`gh`，並且自動登入 | 終端機直接 `gh pr create` 發 PR |
| 可調整機器規格 | 2 核到 32 核，依需求選擇 | 本專案用預設的 2 核就夠 |

### 收費方式

**費用算在「開 Codespace 的人」身上**，不論 repo 是公開還是私人。

| 個人方案 | 每月免費運算 | 每月免費儲存 |
|---|---|---|
| Free | 120 core-hours（2 核機器約 60 小時） | 15 GB |
| Pro | 180 core-hours（2 核機器約 90 小時） | 20 GB |

超過免費額度後（美元）：

| 機器 | 每小時 |
|---|---|
| 2 核 | $0.18 |
| 4 核 | $0.36 |
| 8 核 | $0.72 |
| 儲存空間 | $0.07／GB／月 |

- 只有**執行中**才計算運算時間；閒置一段時間（預設 30 分鐘）會自動停止
- **停止後仍佔儲存空間**，不用的 Codespace 記得刪除
- 沒有綁信用卡：用完額度就無法開啟或繼續使用，**不會被扣款**

> 價格以 [GitHub 官方文件](https://docs.github.com/en/billing) 為準（2026 年 11 月查詢）。

---

## Demo 操作流程（約 9 分鐘）

### 1. 開 Codespace（1 分鐘）

點上方 **Open in GitHub Codespaces**。

> 💬 瀏覽器裡就是完整的 VS Code。套件自動裝好、資料自動抓好、預覽自動打開，這些都寫在 `.devcontainer/devcontainer.json`。

### 2. 改程式（1 分鐘）

打開 `fetch.py`，修改最上方 ✏️ 的設定：換成台積電、改看 2026 上半年：

```python
SYMBOL = os.getenv("SYMBOL", "2330.TW")
NAME = os.getenv("NAME", "台積電")
START = "2026-01-01"
END = "2026-06-30"
```

在終端機執行，再重新整理右側預覽：

```bash
python fetch.py
```

### 3. 分享預覽（1 分鐘）

下方 **Ports** 面板 → 8000 → 右鍵 → **Port Visibility → Public**，把網址給觀眾用手機打開。

> 💬 程式跑在雲端，所以可以直接分享給任何人看。

### 4. 發 PR（1 分鐘）

在終端機執行：

```bash
git checkout -b demo-change
git commit -am "換成台積電"
git push -u origin demo-change
gh pr create --fill
```

> 💬 `gh` 已經裝好、也自動登入了，不用另外設定。

### 5. 看 CI 綠燈（2 分鐘）

打開 PR 頁面，`ci.yml` 自動開始執行。

> 💬 等待時講：PR 一發出就自動觸發檢查。用 **matrix** 同時跑三個 job，平行檢查三檔股票。點進任一個 job，**Summary** 會顯示抓到的收盤表格。

約 30 秒後全部綠燈 ✅。

### 6. 合併 → 自動部署（2 分鐘）

在 PR 頁面按 **Merge**，到 **Actions** 頁籤看「部署網站」開始執行。

> 💬 等待時講：合併到 main 會觸發另一個 workflow，抓資料並部署到 GitHub Pages。這就是 CI/CD：CI 檢查、CD 部署。

約 30 秒後打開 https://cwhash.github.io/demo/ ，正式網站已經變成台積電 2026 上半年。

**總結：Codespaces 負責「寫」，Actions 負責「跑」。**

---

# 股價看板 demo

[![CI](https://github.com/cwhash/demo/actions/workflows/ci.yml/badge.svg)](https://github.com/cwhash/demo/actions/workflows/ci.yml)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/cwhash/demo?quickstart=1)

**Codespaces 負責「寫」，Actions 負責「跑」。**
不用在本機裝任何東西就能改程式；發 PR 後，GitHub Actions 自動檢查程式能不能正常運作。

網站：https://cwhash.github.io/demo/

---

## Demo 流程（約 5 分鐘）

### 1. 開 Codespace（1 分鐘）

點上方 **Open in GitHub Codespaces**。

環境會自動準備好：安裝套件、抓資料，網站預覽出現在右側。
這些都寫在 `.devcontainer/devcontainer.json`，每個人打開都是一樣的環境。

### 2. 改程式（1 分鐘）

打開 `fetch.py`，修改最上方 ✏️ 標示的設定，例如換股票：

```python
SYMBOL = os.getenv("SYMBOL", "2330.TW")
NAME = os.getenv("NAME", "台積電")
```

在終端機執行，再重新整理預覽：

```bash
python fetch.py
```

### 3. 發 PR（1 分鐘）

在終端機執行：

```bash
git checkout -b demo-change
git commit -am "換成台積電"
git push -u origin demo-change
gh pr create --fill
```

也可以用左側 **Source Control** 面板操作。

### 4. 看 CI 綠燈（2 分鐘）

打開 PR 頁面，`ci.yml` 自動開始執行，約 30 秒後出現綠燈 ✅。
程式寫壞了（例如股票代號打錯）就會變紅燈 ❌，合併之前就能發現問題。

展示完關閉 PR，不要合併。

---

## Demo 前檢查

- [ ] 先開好一個 Codespace，確認預覽會自動出現
- [ ] 預演一次步驟 3、4，確認 CI 綠燈，然後關閉 PR
- [ ] demo 結束後停止或刪除 Codespace，避免用掉免費額度

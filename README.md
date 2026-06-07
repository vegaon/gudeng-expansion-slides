# 家登精密花壇廠區擴展計畫 — 送審簡報（交接說明）

非都市土地（彰化縣花壇鄉三家段 668、672 地號）變更編定送審用的 Reveal.js 互動 HTML 簡報。
本檔為**換機／到公司接續修改**的交接說明。

- **線上版（GitHub Pages）**：https://vegaon.github.io/gudeng-expansion-slides/
- **GitHub Repo**：https://github.com/vegaon/gudeng-expansion-slides
- **本機路徑**：`L:\我的雲端硬碟\AntiGravity\家登\gudeng-expansion-slides\`（Google Drive，會自動同步）

---

## 一、到公司如何取得最新檔

**方法 A（建議）：Git clone**
```bash
git clone https://github.com/vegaon/gudeng-expansion-slides.git
cd gudeng-expansion-slides
```

**方法 B：直接用 Google Drive 同步的資料夾**
公司電腦若有登入同一個 Google Drive，路徑同上即可直接開啟編輯。
（注意：用 Drive 同步時，仍建議改完後 `git commit` / `git push` 保留版本。）

**方法 C：用本 ZIP 解壓**
解開 `家登簡報_打包.zip` 即得完整專案（含參考素材）。

---

## 二、預覽（本機看效果）

簡報是純前端，**不需安裝任何套件**，用 Python 內建伺服器即可：
```bash
cd gudeng-expansion-slides
python -m http.server 8000
```
瀏覽器開 `http://localhost:8000/index.html`。
（直接雙擊 index.html 也可，但部分瀏覽器對本機檔案的圖片載入較嚴格，建議用上面的伺服器方式。）

操作：方向鍵翻頁、按 `F` 全螢幕、按 `Esc` 總覽。

---

## 三、改投影片

所有內容都在 **`index.html`** 一個檔案裡（CSS、HTML、JS 都在內）。
每一頁是一個 `<section> ... </section>`，依序對應簡報頁碼，並有中文註解（如 `<!-- 14. 我們的破局方案 -->`）。

改完存檔 → 重新整理瀏覽器即可看到效果。

### 互動時程圖（第 12 頁「分期開發預定時程」）
此頁是**資料驅動**的：時程的階段、月數、相依關係都定義在 `index.html` 最底部
`<script>` 內的 `PHASES` 陣列。要增刪階段或改預設月數，改那裡即可，甘特圖、年月軸、
D-day 位置、超時示警都會自動重算。每個階段在頁面上也有自己的「月數調整桿」可即時模擬延誤。

關鍵常數：`DDAY = 54`（民國 120 年 1 月，自起點 115/07 起算第 54 個月）。

---

## 四、改完後重新部署上線

GitHub Pages 會在 push 後自動更新（約 1～2 分鐘）：
```bash
git add -A
git commit -m "修改說明"
git push
```
推上 `master` 分支即自動發佈到 https://vegaon.github.io/gudeng-expansion-slides/

---

## 五、檔案結構

```
gudeng-expansion-slides/
├── index.html          ← 簡報本體（內容、樣式、互動 JS 全在此）
├── images/             ← 背景底圖、扁平圖標、地籍分析圖、航照圖
│   ├── cover.png / purpose.png / ending.png   背景底圖（AI 生成）
│   ├── cadastral_analysis.png                 地籍分區分析圖
│   ├── aerial_669.png                         以 669 為中心的航照圖
│   └── icon_*.png                             各頁扁平圖標
├── make_aerial.py      ← 重新產生航照圖的腳本（見下）
├── crop_icons.py       ← 把 AI 圖標總表裁切去背的腳本
├── .claude/launch.json ← 本機預覽伺服器設定（給 Claude 預覽用，可略）
└── 參考素材/           ← （ZIP 版才有）計畫書、風險報告、文案、地號資料
```

---

## 六、輔助腳本

需要 Python 與 `Pillow`（`pip install pillow`）。

- **`make_aerial.py`** — 重新抓 NLSC 正射航照（PHOTO2）＋地籍界線（LANDSECT）拼接出
  `images/aerial_669.png`。要改縮放範圍或裁切尺寸，調腳本內的 `Z`（縮放層級）、
  `CROP_W/CROP_H`、`PARCELS`（地號座標與標記顏色）。座標來自 `鄰近地號資料.xlsx`。
  ```bash
  python make_aerial.py
  ```
- **`crop_icons.py`** — 將 draw 技能產生的「圖標總表」（4 圖一排）裁切成單一去背 PNG。
  只有要新增／重做圖標時才需要。

---

## 七、原始素材位置（同層 `家登/` 資料夾，或 ZIP 內 `參考素材/`）

- `家登擴廠專案計畫書.md` — 興辦事業計畫書定稿草案（各章節數據來源）
- `家登精密擴廠法規與卡關風險分析報告.md` — 法規對照、時程死結、破局方案（簡報敘事骨幹）
- `文案/家登毗鄰丁建變更_簡報文案.md` — 早期完整文案
- `鄰近地號資料.xlsx` — 13 筆鄰近地號座標／面積／使用類別（航照圖座標來源）

---

## 八、簡報結構與敘事（14 頁）

**前段（純兩期丁建變更的合規說明，刻意不提交通用地）**
1 封面｜2 計畫緣由｜3 申請人｜4 申請基地概況（含航照圖、第 4 條毗連認定）｜
5 鄰近土地｜6 法規依據｜7 分期開發規劃｜8 面積與比例合規性（1.27/1.11 倍）｜
9 土地使用強度｜10 環境影響與灌排分流｜11 山坡地與環境敏感｜12 分期開發時程（互動）

**結尾段（才揭露破局方案）**
13 關鍵挑戰（時程死結／國土法 D-day／交通／環評）｜14 我們採取的破局方案
（第一案 668 丁建＋第二案 672 改交通用地）

**設計重點**
- 用途為**送審/官方**：語氣為合規說明，非對業主推銷。
- 「672 改交通用地」是我方策略，**僅在結尾揭露**，前段完全不提。
- 第 12 頁時程刻意呈現：即使最樂觀，純丁建分期仍趕不上 D-day → 帶出第 14 頁破局方案。
- 配色：accent 橘 `#e8643a`、accent2 青 `#4fc3f7`、success 綠 `#81c784`、warn 琥珀 `#ffb74d`、深色背景。

---

## 九、待確認事項（送審前）

- 第 4 頁毗連認定寫「相隔道路寬度未逾 10 公尺」——請以實際路寬確認後再定稿。
- 第 12 頁 D-day 採文件所載「國土計畫法預計民國 120 年」——如有更精確公告日可調整 `DDAY`。

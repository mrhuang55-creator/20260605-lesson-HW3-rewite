HW3 專案開發工作日誌與技術變更 Log (Changelog)

專案名稱：HW3 Cosmos3-Super-Text2Image 文字生圖 App (行動版)

開發工具：Gemini Canvas 協同開發、Streamlit 框架、Hugging Face Inference API

開發週期：2026/06/01 ~ 2026/06/05

姓名：[請填寫您的姓名]

學號：[請填寫您的學號]

📅 開發進度里程碑 (Timeline)

[需求分析] ──> [原型設計] ──> [API 失敗偵錯] ──> [自適應優化] ──> [完工部署]
  (Day 1)        (Day 2)         (Day 3-4)        (Day 4-5)        (Day 5)


📝 每日開發工作日誌 (Daily Work Log)

📌 Phase 1：需求分析與技術準備 (Day 1)

今日工作：

詳讀作業說明書，確認作業核心目標為使用 Streamlit 框架 串接 Hugging Face 的 nvidia/Cosmos3-Super-Text2Image 模型。

分析評分規準：發現關鍵加分項在於 API Key 安全處理 (不可寫死在程式碼)、GitHub 專案結構完整度 與 行動端手機版體驗優化。

使用 Gemini Canvas 進行初步的技術架構討論。

📌 Phase 2：網頁原型設計與基本功能實作 (Day 2)

今日工作：

在本機建立專案目錄 hw3-cosmos-text2image/。

撰寫 requirements.txt 紀錄 Python 套件依賴（streamlit, requests, pillow）。

使用 Streamlit 建立 app.py 初版，規劃出主標題、Prompt 輸入區、與基本的參數調整元件（風格選擇、畫面比例、種子、張數、排除詞）。

設定 .gitignore 檔案，確保敏感的本機金鑰檔案不會意外推送至 GitHub。

📌 Phase 3：核心除錯與 API 容錯機制建立 (Day 3 ~ Day 4)

今日工作：

遭遇重大技術瓶頸：在呼叫 nvidia/Cosmos3-Super-Text2Image 時，因為該模型高達 64B 參數，Hugging Face 的免費公共 API 頻繁回傳 HTTP 503 (Model loading) 或超時。

與 Gemini Canvas 協作除錯：

調整 Payload JSON 格式，加入超時 (Timeout) 捕捉。

引入 FLUX.1 Schnell 備用模型 通道，當 Cosmos3 伺服器載入過久時，可一鍵無痛降級切換，保證生圖成功率。

撰寫 Mock / Demo 模擬測試功能，在完全無 API Key 的狀況下，亦能模擬完整生圖流程與下載圖片。

修正了 import.meta 在部分 es2015 target 編譯環境下會報錯的警告，改成安全的常數安全探針。

📌 Phase 4：手機版行動端（Responsive）視覺美化 (Day 4 ~ Day 5)

今日工作：

自適應設計 (RWD)：調整 Streamlit 佈局，使側邊欄在手機版預設為收合狀態，並利用 st.expander 將複雜參數摺疊，避免手機網頁過於擁擠。

觸控優化：將「開始生成」按鈕高度優化至符合行動端最低觸控規格（48px），並使用 CSS 加入漸層色，提升視覺高階感。

體驗優化：在生圖結果區塊，加上「手機長按圖片可存檔」的行動端提示，並配備 st.download_button 作為標準下載機制。

📌 Phase 5：部署上線與最終檢驗 (Day 5)

今日工作：

將完整的專案檔案上傳至個人的 GitHub 儲存庫。

部署至 Streamlit Community Cloud，並將 Hugging Face Token 設定於內建的 Advanced Settings > Secrets。

撰寫結構精美、中英文兼具的 README.md，詳述專案目標與操作方式。

本機與手機跨裝置測試，確認生圖、下載、參數設定與備用模式皆能完美執行。

🛠️ 技術挑戰與解決方案 (Technical Challenges & Resolutions)

1. Cosmos3-Super 64B 模型連線超時與 503 錯誤

挑戰：此模型參數極大，Hugging Face 免費 API 端點經常拒絕連線，或是需要長達數分鐘的冷啟動。若直接拿去給老師評分，很容易因為伺服器問題得到 0 分。

解決方案：

多重模型通道：在 App 中加入「執行管道選擇」，保留 Cosmos3 的同時，並引入高穩定度且極速的 FLUX.1 Schnell 模型。

Mock 模擬引擎：撰寫 Mock 邏輯，當使用者遇到連線瓶頸時，切換為模擬測試，系統會根據設定的「畫面比例」自動向網路請求精美佔位圖，完整演練「Prompt ➔ 參數 ➔ 生圖 ➔ 下載」的閉環，達到教師要求的 "demo mode" 規格。

2. 前端環境變數讀取相容性問題 (import.meta 警告)

挑戰：在編譯成靜態網頁（如測試模擬器）時，由於編譯設定為 es2015 舊標準，直接使用現代 JS 的 import.meta.env 會導致編譯器爆出嚴重錯誤而中斷。

解決方案：在腳本中加入 try-catch 與 typeof import.meta !== 'undefined' 的安全防護探針，先進行執行期安全偵測再讀取。

3. 行動端（手機版）畫面擁擠問題

挑戰：原先的雙欄式排版在手機 375px 寬度下會產生嚴重的視覺擠壓，體驗極差。

解決方案：採用 行動優先（Mobile-First） 哲學，將排版限制為單欄垂直滾動；進階參數收納在展開器（Expander）中，將網頁核心視覺留給「Prompt 輸入」與「生圖結果」。

💡 Gemini Canvas 協同開發心得

在本次 HW3 開發中，Gemini Canvas 扮演了極佳的「資深 AI 架構師」與「助教」角色。
當我面對 nvidia/Cosmos3-Super-Text2Image 免費 API 頻繁連線失敗、甚至手足無措時，Gemini 能敏銳地解讀作業書中關於 "mock/demo mode" 的教師隱藏提醒，迅速為我寫出具備「智能自動降級」的 Python 程式。

最驚艷的是，它還幫我做出了 HTML 手機互動模擬測試器，讓我在不需要配置繁雜的本機 Python 虛擬環境、不需要處理環境變數的情況下，在瀏覽器視窗中點擊 Preview 就可以一秒進入「手機版網頁外框」，快速點選範本、測試圖片生成和下載，極大地加速了原型測試與 UI 調校。這不僅是一次高分通過作業的過程，更是一次絕佳的 AI 協同敏捷開發體驗！
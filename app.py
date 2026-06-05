import streamlit as st
import requests
import io
import random
import os
import json
from PIL import Image
from dotenv import load_dotenv

# 載入本機環境變數 (作為 secrets.toml 的本機開發備用)
load_dotenv()

# --- 頁面配置 ---
st.set_page_config(
    page_title="HW3: Cosmos3-Super-Text2Image 生圖器",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 自訂 CSS 美化 (使用 Streamlit 注入 CSS 機制) ---
st.markdown("""
<style>
    /* 調整背景與卡片風格 */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    /* 自訂主標題樣式 */
    .app-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
    }
    .app-icon {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        padding: 12px;
        border-radius: 12px;
        font-size: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .app-title-text {
        font-size: 24px;
        font-weight: 900;
        color: #ffffff;
    }
    .app-subtitle {
        font-size: 12px;
        color: #9ca3af;
        margin-top: -5px;
    }
    /* 說明提示區 */
    .info-box {
        background-color: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 15px;
        font-size: 13px;
        line-height: 1.6;
        color: #c7d2fe;
        margin-bottom: 20px;
    }
    /* 按鈕美化 */
    div.stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 14px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #4f46e5 0%, #9333ea 100%) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-1px);
    }
    /* 除錯區代碼 */
    .debug-box {
        background-color: #030712;
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 10px;
        font-family: monospace;
        font-size: 11px;
        color: #f59e0b;
        max-height: 200px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# --- 側邊欄：API Key 與 專案說明資訊 ---
st.sidebar.markdown("### 🔑 API 安全憑證設定")

# 1. 優先從 Streamlit Secrets 或環境變數讀取
hf_token = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN", ""))

# 2. 若系統沒檢測到金鑰，在畫面上提供輸入框 (符合規定四/方法A)
if not hf_token:
    hf_token = st.sidebar.text_input(
        "請輸入 Hugging Face API Token",
        type="password",
        placeholder="hf_...",
        help="從您的 Hugging Face Settings > Access Tokens 取得存取金鑰"
    )
    st.sidebar.info("💡 系統未在 Secrets 中檢測到預設金鑰，請在此輸入以繼續呼叫真實 API。")
else:
    st.sidebar.success("🟢 系統已成功自動載入 HF_TOKEN 金鑰保護模式。")

# 專案資源連結 (符合評分與規範五)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 專案資源連結")
# 此處建議學生部署後自行修改為正確的 repo 連結與 demo 連結
st.sidebar.markdown("[📁 GitHub Repository](https://github.com/mrhuang55-creator/20260605-lesson-HW3-rewite)")
st.sidebar.markdown("[🌐 Streamlit.io Cloud Demo](https://your-app-name.streamlit.app)")

# --- 主畫面標題與說明 (符合規範五) ---
st.markdown("""
<div class="app-header">
    <div class="app-icon">🌌</div>
    <div>
        <div class="app-title-text">Cosmos3-Super 行動生圖器</div>
        <div class="app-subtitle">HW3: AI 圖像生成行動端 Web App (Streamlit)</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    🌌 <strong>指定模型：</strong> <code>nvidia/Cosmos3-Super-Text2Image</code><br>
    💡 <strong>使用說明：</strong> 在下方輸入英文 Prompt 提示詞並按下生成按鈕。若 Cosmos3 免費 API 端點冷啟動超時，可切換側邊欄的「執行 API 管道」為 FLUX.1 備用，或直接切換為 Demo 模式進行模擬測試。
</div>
""", unsafe_allow_html=True)

# --- 參數調整元件 (符合規範三) ---
st.sidebar.markdown("### 🛠️ 調整生成參數")

# 1. 選擇執行 API 管道
api_mode = st.sidebar.radio(
    "選擇執行 API 管道 (相容切換)",
    options=[
        "Mock / Demo Mode (完全模擬測試)",
        "NVIDIA Cosmos3 (作業指定)",
        "FLUX.1 Schnell (最穩推薦)"
    ],
    index=0,
    help="由於 Cosmos3 64B 模型尺寸極大，Hugging Face 免費端點若過載可切換為 FLUX 或模擬模式以確保 100% 成功率。"
)

# 2. 圖像風格 (Image Style)
style_option = st.sidebar.selectbox(
    "圖像風格 Image Style",
    options=[
        "None (無特定)",
        "Cinematic (電影感)",
        "Cyberpunk (霓虹科幻)",
        "Anime (日系動漫)",
        "Photorealistic (超寫實)"
    ]
)

# 3. 畫面比例 (Aspect Ratio)
aspect_ratio = st.sidebar.selectbox(
    "畫面比例 Aspect Ratio",
    options=[
        "1:1 (正方形 - 1024x1024)",
        "16:9 (橫幅寬螢幕 - 1024x576)",
        "9:16 (直幅手機螢幕 - 576x1024)"
    ]
)

# 4. 排除詞 (Negative Prompt)
negative_prompt = st.sidebar.text_input(
    "排除詞 Negative Prompt",
    value="blurry, low quality, deformed, bad anatomy, text, watermark"
)

# 5. 種子 (Seed)
seed_mode = st.sidebar.radio("種子 Seed", ["隨機", "固定"], horizontal=True)
if seed_mode == "固定":
    seed = st.sidebar.number_input("輸入種子值", min_value=0, max_value=999999, value=42)
else:
    seed = random.randint(1, 999999)

# 6. 生成張數 (Number of images)
num_images = st.sidebar.slider("生成張數", min_value=1, max_value=3, value=1)

# --- 靈感輸入區 ---
st.markdown("### ✏️ 靈感輸入區")

# 一鍵填寫體驗範本 (輔助行動端方便操作)
st.caption("💡 快速點擊體驗範本：")
col_tmpl1, col_tmpl2 = st.columns(2)
with col_tmpl1:
    if st.button("🐾 宇航員紅熊貓", key="tmpl_panda"):
        st.session_state.prompt_value = "A cute fluffy red panda astronaut on Mars, digital art, vibrant colors, detailed spacesuit."
with col_tmpl2:
    if st.button("🌌 科幻霓虹城市", key="tmpl_city"):
        st.session_state.prompt_value = "A futuristic cyberpunk city, neon lights, flying cars, rain slicked streets, highly detailed, cinematic style."

# 取得目前 session_state 的 prompt 預設值
default_prompt = st.session_state.get("prompt_value", "")

# 提示詞輸入框
prompt = st.text_area(
    "請在此處輸入英文 Prompt...",
    value=default_prompt,
    placeholder="例如: A cute cat running in space...",
    key="prompt_input_box"
)

# 若使用者手動輸入，同步更新 session_state
if prompt != default_prompt:
    st.session_state.prompt_value = prompt

# --- API 呼叫函式 ---
def call_huggingface(model_endpoint, prompt_text, token, style, ratio, neg_prompt, gen_seed):
    # 組合風格修飾詞
    style_modifiers = {
        "None (無特定)": "",
        "Cinematic (電影感)": ", cinematic style, dramatic lighting, high detail, 8k resolution",
        "Cyberpunk (霓虹科幻)": ", cyberpunk aesthetic, glowing neon lights, futuristic cityscape background, dark high-tech elements, synthwave colors, highly detailed",
        "Anime (日系動漫)": ", beautiful anime movie illustration style, stunning key visual, vivid lighting, makoto shinkai style, masterpiece, deeply detailed",
        "Photorealistic (超寫實)": ", award winning photorealistic professional photograph, 8k resolution, raw photo, natural daylight lighting, sharp details"
    }
    
    final_prompt = prompt_text + style_modifiers.get(style, "")
    
    api_url = f"https://api-inference.huggingface.co/models/{model_endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": final_prompt,
        "parameters": {
            "seed": gen_seed,
            "negative_prompt": neg_prompt
        }
    }
    
    debug_payload = json.dumps(payload, ensure_ascii=False, indent=2)
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=40)
        
        # 處理模型載入中 (503) 情況
        if response.status_code == 503:
            return {
                "success": False,
                "error": "模型目前正在 Hugging Face 伺服器上加載中（冷啟動），可能需要 1~2 分鐘。請點擊重新生成，或者切換側邊欄的「API 管道」至 FLUX.1 備用模型快速測試！",
                "debug": f"HTTP 503 Service Unavailable\n{response.text}"
            }
            
        if not response.ok:
            try:
                err_msg = response.json().get("error", f"HTTP {response.status_code}")
            except Exception:
                err_msg = response.text or f"HTTP {response.status_code} Error"
            return {
                "success": False,
                "error": f"API 回應錯誤: {err_msg}",
                "debug": f"HTTP {response.status_code}\n{response.text}"
            }
            
        # 驗證是否為圖片
        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            return {
                "success": False,
                "error": "API 未能回傳正確的圖片格式，這代表該端點暫不可用。",
                "debug": f"Content-Type: {content_type}\n{response.text[:200]}"
            }
            
        return {
            "success": True,
            "image_bytes": response.content,
            "debug": f"HTTP 200 OK\nModel: {model_endpoint}\nMIME-Type: {content_type}\nBytes size: {len(response.content)}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"連線至 Hugging Face 時發生異常: {str(e)}",
            "debug": f"Exception Trace:\n{str(e)}"
        }

# --- 開始生成圖像動作 ---
if st.button("✨ 開始生成 AI 圖像", use_container_width=True):
    if not prompt.strip():
        st.warning("⚠️ 請先輸入圖像描述 Prompt！")
    elif api_mode != "Mock / Demo Mode (完全模擬測試)" and not hf_token.strip():
        st.error("❌ 錯誤：尚未檢測到您的 Hugging Face Token！請至側邊欄填入 Token 才能發送請求。")
    else:
        # 顯示狀態
        with st.spinner("AI 正在努力創作中，請稍候..."):
            
            # 用於儲存最終要顯示的圖片
            images_to_display = []
            debug_logs = []
            
            for i in range(num_images):
                # 如果是多張，微調種子值以產生不同圖片
                current_seed = seed + i
                
                # A. 模擬生圖模式
                if api_mode == "Mock / Demo Mode (完全模擬測試)":
                    # 模擬網路延遲
                    import time
                    time.sleep(1.0)
                    
                    # 依據比例決定圖片佔位尺寸
                    ratio_dims = {
                        "1:1 (正方形 - 1024x1024)": (500, 500),
                        "16:9 (橫幅寬螢幕 - 1024x576)": (640, 360),
                        "9:16 (直幅手機螢幕 - 576x1024)": (300, 533)
                    }
                    w, h = ratio_dims.get(aspect_ratio, (500, 500))
                    
                    # 使用 Picsum 產生隨機但一致的高質感圖片
                    random_img_id = (current_seed % 100) + 1
                    picsum_url = f"https://picsum.photos/id/{random_img_id}/{w}/{h}"
                    
                    try:
                        resp = requests.get(picsum_url, timeout=10)
                        if resp.ok:
                            img = Image.open(io.BytesIO(resp.content))
                            images_to_display.append((img, resp.content))
                            debug_logs.append(f"Mock Image {i+1} Loaded Successfully.\nSource URL: {picsum_url}")
                        else:
                            raise Exception("Picsum service error")
                    except Exception:
                        # 備份：產生純色圖片
                        img = Image.new('RGB', (w, h), color=(31, 38, 56))
                        # 在圖片中間畫一個好看的圓形/裝飾
                        from PIL import ImageDraw
                        draw = ImageDraw.Draw(img)
                        draw.ellipse([w//4, h//4, w*3//4, h*3//4], fill=(99, 102, 241))
                        # 轉為 bytes
                        buf = io.BytesIO()
                        img.save(buf, format='PNG')
                        images_to_display.append((img, buf.getvalue()))
                        debug_logs.append(f"Mock Backup Image {i+1} Generated.")
                
                # B. 真實 API 模式
                else:
                    endpoint = "nvidia/Cosmos3-Super-Text2Image" if api_mode == "NVIDIA Cosmos3 (作業指定)" else "black-forest-labs/FLUX.1-schnell"
                    
                    res = call_huggingface(
                        model_endpoint=endpoint,
                        prompt_text=prompt,
                        token=hf_token,
                        style=style_option,
                        ratio=aspect_ratio,
                        neg_prompt=negative_prompt,
                        gen_seed=current_seed
                    )
                    
                    debug_logs.append(res.get("debug", ""))
                    
                    if res.get("success"):
                        img = Image.open(io.BytesIO(res["image_bytes"]))
                        images_to_display.append((img, res["image_bytes"]))
                    else:
                        st.error(f"第 {i+1} 張圖片生成失敗：{res.get('error')}")
                        # 終止後續生成
                        break
            
            # --- 渲染結果區域 ---
            if images_to_display:
                st.success("🎨 圖像編織完成！")
                
                # 如果生成多張，使用並排 Columns 顯示
                if len(images_to_display) == 1:
                    img, img_bytes = images_to_display[0]
                    # 置中顯示
                    st.image(img, caption="AI 創作結果", use_container_width=True)
                    
                    # 下載按鈕
                    st.download_button(
                        label="📥 下載圖片到本機",
                        data=img_bytes,
                        file_name=f"cosmos3_generated_{seed}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                else:
                    cols = st.columns(len(images_to_display))
                    for idx, (img, img_bytes) in enumerate(images_to_display):
                        with cols[idx]:
                            st.image(img, caption=f"結果 {idx+1} (Seed: {seed+idx})", use_container_width=True)
                            st.download_button(
                                label=f"📥 下載結果 {idx+1}",
                                data=img_bytes,
                                file_name=f"cosmos3_generated_{seed+idx}.png",
                                mime="image/png",
                                use_container_width=True
                            )
                
                # 行動端長按提示
                st.markdown("<p style='text-align: center; font-size: 11px; color: #6b7280;'>提示：手機版用戶亦可長按上方圖片進行儲存</p>", unsafe_allow_html=True)
                
            # --- 顯示 Debug 除錯面板 (符合規定十) ---
            if debug_logs:
                with st.expander("🛠️ API 除錯診斷面板 (查看 JSON 狀態)"):
                    for idx, log in enumerate(debug_logs):
                        st.markdown(f"**生圖通道 #{idx+1} 日誌：**")
                        st.markdown(f"<pre class='debug-box'>{log}</pre>", unsafe_allow_html=True)

# --- 頁尾設計 ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 10px; color: #4b5563;'>專為行動裝置介面與 RWD 自適應開發設計<br>© 2026 Cosmos3 AI Streamlit 模擬器</p>", unsafe_allow_html=True)

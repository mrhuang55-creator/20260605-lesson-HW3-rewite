# HW3 Cosmos3-Super-Text2Image App

## Project Goal

This project uses Streamlit and Hugging Face to build an interactive, responsive text-to-image generation web application featuring the **NVIDIA Cosmos3-Super-Text2Image** model. Designed with a mobile-first philosophy, this app optimizes interface space, touch targets, and inputs for seamless use on smartphones and desktop screens alike.

## Model

* **Primary Model:** `nvidia/Cosmos3-Super-Text2Image` (64B parameters text-to-image specialist)
* **Secondary Fallback Model:** `black-forest-labs/FLUX.1-schnell` (For fast, high-performance generation fallback)
* **Simulation Mode:** Interactive mock generation utilizing `Picsum` placeholders (Enables 100% stable runtime demo without requiring API keys).

## Features

1. **Flexible API Key Settings:** Secure handling via Streamlit Secrets (`HF_TOKEN`) or custom masked field inputs directly inside the sidebar.
2. **Detailed Aspect Ratio Options:** Seamlessly switch layouts between:
   - `1:1` (Square - 1024x1024)
   - `16:9` (Widescreen - 1024x576)
   - `9:16` (Vertical Mobile Screen - 576x1024)
3. **Advanced Parameter Panel:** Customize style presets (Cinematic, Cyberpunk, Anime, Photorealistic), seed values, image counts (1-3 slider), and negative prompts.
4. **Mock / Demo Mode:** Built-in simulation fallback that generates beautiful image results matching selected aspect ratios when models are loading or rate-limited.
5. **Interactive Quick Presets:** Single-click template prompts to test the generation workflow quickly.
6. **Mobile Touch Adjustments:** Buttons with large, accessible touch target heights (>48px) and direct image download controls.
7. **Debug Console:** Expanded accordion section outputs raw response payloads and headers from Hugging Face endpoints for diagnostics.

---

## How to Run Locally

### 1. Install Dependencies

Ensure Python is installed, then run:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional)

You can create a `.env` file in the root folder to supply your Hugging Face Token locally:

```text
HF_TOKEN=your_huggingface_token_here
```

### 3. Run the App

Launch the local web server:

```bash
streamlit run app.py
```

---

## API Key Configuration

Do not hardcode your API key. You can supply your Hugging Face token in two safe ways:

1. **Enter on the Web Page:** Type your Token into the password field inside the left sidebar.
2. **Streamlit Secrets (Recommended for deployment):** When deploying to Streamlit Community Cloud, set the value in the **Advanced Settings > Secrets** dialog:
   ```toml
   HF_TOKEN = "your_hugging_face_token_here"
   ```

---

## Deployment

This app is designed for easy deployment to **Streamlit Community Cloud** (https://share.streamlit.io). Connect your GitHub repository, configure your `HF_TOKEN` in the Cloud secrets, and launch.

---

## Links

* **GitHub Repo:** [https://github.com/mrhuang55-creator/20260605-lesson-HW3-rewite](https://github.com/mrhuang55-creator/20260605-lesson-HW3-rewite)
* **Streamlit Demo:** [https://20260605-leappn-hw3-rewitegit-gzko5beyuyvczgk6brwwuf.streamlit.app/](https://20260605-leappn-hw3-rewitegit-gzko5beyuyvczgk6brwwuf.streamlit.app/)

---

## Screenshots

*Place your application screenshots inside the `screenshots/` directory and reference them here.*

### Application Home Screen
![App Home](screenshots/app_home.png)

### Generated Image Output
![Generated Result](screenshots/generated_result.png)

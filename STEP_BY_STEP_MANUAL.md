# Multi-Agent Gateway – Complete Step-by-Step Manual
## AI Software Innovation Infotech And Hardware Enterprises

**Version:** 2.0 (with AI Chat + Voice + Multi-Language)  
**Copyright (c) 2026 – All Rights Reserved**

---

## 1. What is this project?

This is a **Multi-Agent AI Gateway** with:

- ChatGPT / Grok style **AI Chat**
- **Voice / Audio input** (browser microphone)
- **Text-to-Speech** (Speak Reply button)
- **15+ languages** support
- 6 specialized agents working together
- Admin Panel (company info, logo, team)
- About Us page

---

## 2. Files in this project

```
multi_agent_gateway/
├── app.py                  ← Main Streamlit app (run this)
├── gateway.py              ← API Gateway + orchestration
├── main.py                 ← CLI version
├── requirements.txt
├── README.md
├── LICENSE
├── STEP_BY_STEP_MANUAL.md  ← This file
├── agents/
│   ├── base.py
│   └── specialized.py
├── config/
│   └── settings.py
├── utils/
│   ├── cache.py
│   ├── logger.py
│   └── rate_limiter.py
├── data/
│   ├── company_info.json
│   └── users.json
└── assets/
    ├── logo.svg
    └── ceo_placeholder.svg
```

---

## 3. How to run LOCALLY

### Step 1 – Extract
```bash
unzip multi_agent_gateway_full.zip
cd multi_agent_gateway
```

### Step 2 – Install
```bash
pip install -r requirements.txt
```

### Step 3 – Run
```bash
streamlit run app.py
```

Browser will open at: http://localhost:8501

---

## 4. How to deploy on Streamlit Cloud (FREE)

1. Create a **public** GitHub repository
2. Upload **all files** from this folder (keep structure)
3. Go to https://share.streamlit.io
4. Click **Create app** → Deploy from GitHub
5. Fill:
   - Repository → your repo
   - Branch → main
   - Main file path → `app.py`
6. Click **Deploy**

App will be live at: `https://your-app-name.streamlit.app`

---

## 5. How to use the App

### AI Chat (💬)
- Type message and press Enter
- Or open **Voice / Audio Input** → record → type what you said → Send
- Click **🔊 Speak Reply** to hear the answer
- Change language from sidebar

### Multi-Agent System (🤖)
- Enter a complex task
- Click **Run Multi-Agent Pipeline**
- See all agents working + confidence score

### Admin
- Go to **Admin Login**
- Default passwords are in the app (change after first login)
- Admin Panel → edit company name, CEO, team, logo, contact

---

## 6. Default Admin Logins

| Username | Password |
|----------|----------|
| ceo | AI Software Innovation Infotech And Hardware Enterprises@CEO2026 |
| priya | AI Software Innovation Infotech And Hardware Enterprises@CTO2026 |
| jordan | AI Software Innovation Infotech And Hardware Enterprises@Research2026 |
| sam | AI Software Innovation Infotech And Hardware Enterprises@Product2026 |

**Important:** Change these passwords from Admin Panel after first login.

---

## 7. Languages Supported

English, Hindi, Spanish, French, German, Chinese, Japanese, Arabic, Portuguese, Russian, Bengali, Tamil, Telugu, Marathi, Gujarati

Language selector is in the **sidebar**.

---

## 8. Voice Notes

- **Microphone**: Browser will ask permission (Chrome/Edge recommended)
- **Text-to-Speech**: Works in most modern browsers (🔊 Speak Reply)
- **Full auto Speech-to-Text** (all languages without typing): needs paid STT API (OpenAI Whisper / Google Speech). Current version uses audio recording + manual text entry for maximum free compatibility on Streamlit Cloud.

---

## 9. Updating live app

1. Edit `app.py` (or any file) on GitHub
2. Commit
3. Streamlit Cloud automatically redeploys in 1–2 minutes

---

## 10. Support

Company: AI Software Innovation Infotech And Hardware Enterprises  
Focus: Artificial Intelligence | Software Innovation | Infotech & Hardware

---

**End of Manual**

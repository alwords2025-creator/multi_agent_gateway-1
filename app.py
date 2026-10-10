# Copyright (c) 2026 AI Software Innovation Infotech And Hardware Enterprises. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.

"""
AI Software Innovation Infotech And Hardware Enterprises Multi-Agent Gateway
Features: AI Chat + Voice Input + Multi-Language + Multi-Agent System + Admin Panel
"""

import streamlit as st
import json
import hashlib
from pathlib import Path
from datetime import datetime
import asyncio
from gateway import APIGateway

# ====================== CONFIG ======================
DATA_FILE = Path("data/company_info.json")
USERS_FILE = Path("data/users.json")
ASSETS_DIR = Path("assets")
ASSETS_DIR.mkdir(exist_ok=True)

DEFAULT_USERS = {
    "ceo": {
        "password_hash": hashlib.sha256("AI Software Innovation Infotech And Hardware Enterprises@CEO2026".encode()).hexdigest(),
        "role": "Founder & CEO",
        "name": "Alex Rivera",
        "full_access": True
    },
    "priya": {
        "password_hash": hashlib.sha256("AI Software Innovation Infotech And Hardware Enterprises@CTO2026".encode()).hexdigest(),
        "role": "CTO",
        "name": "Priya Sharma",
        "full_access": True
    },
    "jordan": {
        "password_hash": hashlib.sha256("AI Software Innovation Infotech And Hardware Enterprises@Research2026".encode()).hexdigest(),
        "role": "Head of AI Research",
        "name": "Jordan Lee",
        "full_access": True
    },
    "sam": {
        "password_hash": hashlib.sha256("AI Software Innovation Infotech And Hardware Enterprises@Product2026".encode()).hexdigest(),
        "role": "Product Lead",
        "name": "Sam Patel",
        "full_access": True
    }
}

LANGUAGES = {
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Spanish (Español)": "es",
    "French (Français)": "fr",
    "German (Deutsch)": "de",
    "Chinese (中文)": "zh",
    "Japanese (日本語)": "ja",
    "Arabic (العربية)": "ar",
    "Portuguese": "pt",
    "Russian (Русский)": "ru",
    "Bengali (বাংলা)": "bn",
    "Tamil (தமிழ்)": "ta",
    "Telugu (తెలుగు)": "te",
    "Marathi (मराठी)": "mr",
    "Gujarati (ગુજરાતી)": "gu",
}

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE) as f:
            return json.load(f)
    save_users(DEFAULT_USERS)
    return DEFAULT_USERS

def save_users(users):
    USERS_FILE.parent.mkdir(exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def load_company():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}

def save_company(data):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_login(username, password):
    users = load_users()
    if username in users:
        hash_pw = hashlib.sha256(password.encode()).hexdigest()
        if users[username]["password_hash"] == hash_pw:
            return users[username]
    return None

def run_gateway(task: str, language: str = "English"):
    if language != "English":
        task = f"[Please respond in {language}] {task}"
    gateway = APIGateway()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        response = loop.run_until_complete(gateway.process(task))
        if response.success:
            return response.final_output, response
        return "Sorry, the agents could not complete this request.", None
    finally:
        loop.close()

def tts_button(text: str, lang_code: str = "en"):
    safe_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$").replace("'", "\\'")[:800]
    st.components.v1.html(f"""
    <button onclick="speak()" style="
        background: linear-gradient(90deg, #7c3aed, #8b5cf6);
        color: white; border: none; border-radius: 8px;
        padding: 8px 16px; cursor: pointer; font-size: 14px;">
        🔊 Speak Reply
    </button>
    <script>
    function speak() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(`{safe_text}`);
            u.lang = '{lang_code}';
            u.rate = 1.0;
            window.speechSynthesis.speak(u);
        }} else {{
            alert('Text-to-Speech not supported in this browser');
        }}
    }}
    </script>
    """, height=50)

st.set_page_config(
    page_title="AISIH Multi-Agent Gateway | AI Chat + Voice",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {{
        background: linear-gradient(90deg, #0f172a, #1e1b4b);
        padding: 1.5rem; border-radius: 12px;
        margin-bottom: 1.5rem; border: 1px solid #8b5cf6;
    }}
    .stButton>button {{
        background: linear-gradient(90deg, #7c3aed, #8b5cf6);
        color: white; border: none; border-radius: 8px; padding: 0.5rem 1.5rem;
    }}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "smart"
if "language" not in st.session_state:
    st.session_state.language = "English"

with st.sidebar:
    try:
        st.image("assets/logo.svg", width=220)
    except Exception:
        st.markdown("### 🚀 AISIH")
    st.markdown("### AISIH Enterprises")
    st.caption("Multi-Agent AI Systems")
    st.divider()

    menu = st.radio(
        "Navigation",
        ["🏠 Home", "💬 AI Chat", "🤖 Multi-Agent System", "📄 About Us", "🔐 Admin Login", "⚙️ Admin Panel"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("**🌐 Language**")
    lang_name = st.selectbox(
        "Reply Language",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.language) if st.session_state.language in LANGUAGES else 0,
        label_visibility="collapsed"
    )
    st.session_state.language = lang_name
    lang_code = LANGUAGES.get(lang_name, "en")

    st.divider()
    if st.session_state.logged_in:
        st.success(f"Logged in as: **{st.session_state.user['name']}**")
        st.caption(st.session_state.user['role'])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    else:
        st.info("Login for full access")

if menu == "🏠 Home":
    company = load_company()
    st.markdown(f"""
    <div class="main-header">
        <h1 style="color:white;margin:0;">🚀 {company.get('company_name', 'AI Software Innovation Infotech And Hardware Enterprises')}</h1>
        <p style="color:#a78bfa;margin:0.3rem 0 0 0;">{company.get('tagline', '')}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Agents", "6 Specialized")
    c2.metric("Architecture", "API Gateway")
    c3.metric("Quality Gate", "Enabled")
    c4.metric("Languages", "15+")

    st.markdown("### Welcome")
    st.write(company.get("about", ""))
    st.info("Go to **💬 AI Chat** for ChatGPT-style chat with Voice support, or **Multi-Agent System** for structured tasks.")

elif menu == "💬 AI Chat":
    st.header("💬 AI Chat + Voice")
    st.caption(f"ChatGPT / Grok style • Language: **{st.session_state.language}** • Multi-Agent powered")

    col1, col2 = st.columns([3, 1])
    with col2:
        mode = st.selectbox("Mode", ["Smart (Multi-Agent)", "Fast Reply"])
        st.session_state.chat_mode = "smart" if "Smart" in mode else "fast"

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                tts_button(msg["content"], lang_code)

    with st.expander("🎤 Voice / Audio Input", expanded=False):
        st.write("Record your voice. (Browser will ask for microphone permission)")
        audio_data = st.audio_input("Speak your message")
        if audio_data is not None:
            st.audio(audio_data)
            st.info("Voice recorded. Full auto speech-to-text needs STT API (Whisper). Type or paste what you said below.")
            voice_text = st.text_input("Type / paste what you said")
            if voice_text and st.button("Send Voice Message"):
                st.session_state.messages.append({"role": "user", "content": voice_text})
                with st.chat_message("user"):
                    st.markdown(voice_text)
                with st.chat_message("assistant"):
                    with st.spinner("Agents working..."):
                        reply, response = run_gateway(voice_text, st.session_state.language)
                        st.markdown(reply)
                        tts_button(reply, lang_code)
                        if response:
                            with st.expander("🔍 Agent Details"):
                                st.write(f"Agents: {', '.join(response.agents_used)}")
                                st.write(f"Confidence: {response.confidence:.0%} | Time: {response.total_time_ms:.0f} ms")
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..." if st.session_state.chat_mode == "fast" else "Agents collaborating..."):
                reply, response = run_gateway(prompt, st.session_state.language)
                st.markdown(reply)
                tts_button(reply, lang_code)
                if response and st.session_state.chat_mode == "smart":
                    with st.expander("🔍 Agent Details"):
                        st.write(f"**Agents used:** {', '.join(response.agents_used)}")
                        st.write(f"**Confidence:** {response.confidence:.0%}")
                        st.write(f"**Time:** {response.total_time_ms:.0f} ms")

        st.session_state.messages.append({"role": "assistant", "content": reply})

    if st.session_state.messages:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

elif menu == "🤖 Multi-Agent System":
    st.header("🤖 Multi-Agent Gateway")
    st.caption("Parallel Collaboration • Quality Gate • Language: " + st.session_state.language)

    task = st.text_area("Enter your task", height=100,
                        placeholder="Example: Design a scalable recommendation system")

    if st.button("🚀 Run Multi-Agent Pipeline", type="primary"):
        if not task.strip():
            st.warning("Please enter a task")
        else:
            with st.spinner("Agents collaborating..."):
                reply, response = run_gateway(task, st.session_state.language)
            if response and response.success:
                st.success(f"✅ Completed in {response.total_time_ms:.0f} ms | Confidence: {response.confidence:.0%}")
                st.markdown("### Final Output")
                st.markdown(reply)
                tts_button(reply, lang_code)
                with st.expander("📊 Performance & Agent Breakdown"):
                    st.write(f"**Agents Used:** {', '.join(response.agents_used)}")
                    st.write(f"**Critic Approved:** {response.aggregation_details.get('critic_approved')}")
                    for r in response.individual_results:
                        st.write(f"- {r['agent']}: {r['confidence']:.0%} confidence, {r['execution_time_ms']:.0f}ms")
            else:
                st.error("Pipeline failed")
                st.write(reply)

elif menu == "📄 About Us":
    company = load_company()
    st.markdown(f"""
    <div class="main-header">
        <h1 style="color:white;margin:0;">About {company.get('company_name', 'AISIH Enterprises')}</h1>
        <p style="color:#a78bfa;">{company.get('tagline', '')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Our Story")
    st.write(company.get("about", ""))
    st.divider()

    st.subheader("👨‍💼 Founder & CEO")
    ceo = company.get("founder_ceo", {})
    col1, col2 = st.columns([1, 3])
    with col1:
        try:
            st.image(ceo.get("photo", "assets/ceo_placeholder.svg"), width=150)
        except Exception:
            pass
    with col2:
        st.markdown(f"### {ceo.get('name', 'N/A')}")
        st.caption(ceo.get("title", "Founder & CEO"))
        st.write(ceo.get("bio", ""))
        st.write(f"📧 {ceo.get('email', '')}")
        st.write(f"📱 {ceo.get('mobile', '')}")

    st.divider()
    st.subheader("👥 Our Team")
    team = company.get("team_members", [])
    cols = st.columns(3)
    for i, member in enumerate(team):
        with cols[i % 3]:
            try:
                st.image(member.get("photo", "assets/ceo_placeholder.svg"), width=120)
            except Exception:
                pass
            st.markdown(f"**{member.get('name', 'N/A')}**")
            st.caption(member.get("role", ""))
            bio = member.get("bio", "")
            st.write(bio[:120] + "..." if len(bio) > 120 else bio)

    st.divider()
    st.subheader("📍 Contact & Head Office")
    office = company.get("head_office", {})
    contact = company.get("contact", {})
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Head Office Address**")
        st.write(office.get("address", ""))
        st.write(f"{office.get('city', '')}, {office.get('country', '')}")
    with c2:
        st.markdown("**Helpline & Support**")
        st.write(f"📞 Helpline: **{contact.get('helpline', '')}**")
        st.write(f"📧 Support: {contact.get('support_email', '')}")
        st.write(f"🌐 Website: {contact.get('website', '')}")

elif menu == "🔐 Admin Login":
    st.header("🔐 Admin Login")
    st.caption("CEO and Team members only — Full Access")

    if st.session_state.logged_in:
        st.success(f"Already logged in as {st.session_state.user['name']}")
    else:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            if submit:
                user = check_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success(f"Welcome {user['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        st.info("""
        **Default Credentials (Change after first login):**
        - CEO: `ceo` / `AI Software Innovation Infotech And Hardware Enterprises@CEO2026`
        - CTO: `priya` / `AI Software Innovation Infotech And Hardware Enterprises@CTO2026`
        - Research: `jordan` / `AI Software Innovation Infotech And Hardware Enterprises@Research2026`
        - Product: `sam` / `AI Software Innovation Infotech And Hardware Enterprises@Product2026`
        """)

elif menu == "⚙️ Admin Panel":
    if not st.session_state.logged_in:
        st.warning("🔒 Please login first from **Admin Login** page")
        st.stop()

    st.header("⚙️ Admin Panel — Full Access")
    st.caption(f"Logged in as: {st.session_state.user['name']} ({st.session_state.user['role']})")

    company = load_company()
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Company Info", "CEO Profile", "Team Members", "Contact & Office", "Logo Upload"
    ])

    with tab1:
        st.subheader("Edit Company Information")
        new_name = st.text_input("Company Name", value=company.get("company_name", ""))
        new_tagline = st.text_input("Tagline", value=company.get("tagline", ""))
        new_about = st.text_area("About Description", value=company.get("about", ""), height=150)
        if st.button("💾 Save Company Info"):
            company["company_name"] = new_name
            company["tagline"] = new_tagline
            company["about"] = new_about
            save_company(company)
            st.success("Company information updated!")

    with tab2:
        st.subheader("Edit Founder & CEO")
        ceo = company.get("founder_ceo", {})
        ceo_name = st.text_input("CEO Full Name", value=ceo.get("name", ""))
        ceo_title = st.text_input("Title", value=ceo.get("title", "Founder & CEO"))
        ceo_bio = st.text_area("Bio", value=ceo.get("bio", ""), height=100)
        ceo_email = st.text_input("Email", value=ceo.get("email", ""))
        ceo_mobile = st.text_input("Mobile Number", value=ceo.get("mobile", ""))
        if st.button("💾 Save CEO Profile"):
            company["founder_ceo"] = {
                "name": ceo_name, "title": ceo_title, "bio": ceo_bio,
                "email": ceo_email, "mobile": ceo_mobile,
                "photo": ceo.get("photo", "assets/ceo_placeholder.svg")
            }
            save_company(company)
            st.success("CEO profile updated!")

    with tab3:
        st.subheader("Edit Team Members")
        team = company.get("team_members", [])
        for i, member in enumerate(team):
            with st.expander(f"Member {i+1}: {member.get('name', 'Unnamed')}"):
                name = st.text_input(f"Name {i}", value=member.get("name", ""), key=f"name_{i}")
                role = st.text_input(f"Role {i}", value=member.get("role", ""), key=f"role_{i}")
                bio = st.text_area(f"Bio {i}", value=member.get("bio", ""), key=f"bio_{i}")
                if st.button(f"Save Member {i+1}", key=f"save_m_{i}"):
                    company["team_members"][i] = {
                        "name": name, "role": role, "bio": bio,
                        "photo": member.get("photo", "assets/ceo_placeholder.svg")
                    }
                    save_company(company)
                    st.success(f"Member {i+1} updated!")

    with tab4:
        st.subheader("Edit Contact & Head Office")
        office = company.get("head_office", {})
        contact = company.get("contact", {})
        address = st.text_area("Head Office Address", value=office.get("address", ""))
        city = st.text_input("City", value=office.get("city", ""))
        country = st.text_input("Country", value=office.get("country", ""))
        helpline = st.text_input("Helpline Mobile Number", value=contact.get("helpline", ""))
        support_email = st.text_input("Support Email", value=contact.get("support_email", ""))
        website = st.text_input("Website", value=contact.get("website", ""))
        if st.button("💾 Save Contact & Office"):
            company["head_office"] = {"address": address, "city": city, "country": country}
            company["contact"] = {"helpline": helpline, "support_email": support_email, "website": website}
            save_company(company)
            st.success("Contact & Office details updated!")

    with tab5:
        st.subheader("Company Logo Upload")
        try:
            st.image(company.get("logo", "assets/logo.svg"), width=250)
        except Exception:
            st.write("No logo found")
        uploaded = st.file_uploader("Upload new logo (PNG, JPG, SVG)", type=["png", "jpg", "jpeg", "svg"])
        if uploaded:
            logo_path = ASSETS_DIR / f"logo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{uploaded.name.split('.')[-1]}"
            with open(logo_path, "wb") as f:
                f.write(uploaded.getbuffer())
            company["logo"] = str(logo_path)
            save_company(company)
            st.success(f"Logo uploaded: {logo_path}")
            st.image(str(logo_path), width=250)

st.markdown("---")
st.caption("© 2026 AI Software Innovation Infotech And Hardware Enterprises. All Rights Reserved. | Multi-Agent Gateway + Voice Chat")

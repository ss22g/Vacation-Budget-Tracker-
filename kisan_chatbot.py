import os
import re
import io
import wave
import array
import json
import hashlib
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types


# ==========================================
# 1. GEMINI CLIENT & RAG LOADER
# ==========================================
ENABLE_VOICE_INPUT = False  # Change to False to hide mic input

def get_gemini_client():
    api_key = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


@st.cache_data
def load_rag_knowledge(filepath="rag_manual.txt") -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Agri-Predictor Pro Knowledge Base (rag_manual.txt) not found."


# ==========================================
# 2. LIVE USER JOURNEY & STATE TRACKER
# ==========================================
def init_tracker():
    if "user_journey" not in st.session_state:
        st.session_state.user_journey = []
    if "_tracked_values" not in st.session_state:
        st.session_state._tracked_values = {}
    if "app_snapshot" not in st.session_state:
        st.session_state.app_snapshot = {
            "prediction_generated": False,
            "generated_strategies": {},
        }
    if "last_audio_hash" not in st.session_state:
        st.session_state.last_audio_hash = None
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "Namaste! Main **Kisan Sahayak AI** hoon. 🌱\n\n"
                    "Aap **English, Hindi, ya Hinglish** mein type ya bol kar kuch bhi pooch sakte hain—"
                    "soil report bharna ho, mandi bhav samajhna ho, ya aapke crop warnings ke baare mein!"
                ),
            }
        ]


def log_user_step(action: str, detail: str):
    """Logs explicit button clicks and key events chronologically."""
    init_tracker()
    tag = f"{action}: {detail}"
    entry = f"[{datetime.now().strftime('%H:%M:%S')}] {tag}"
    if not st.session_state.user_journey or st.session_state.user_journey[-1].split("] ", 1)[1] != tag:
        st.session_state.user_journey.append(entry)
        st.session_state.user_journey = st.session_state.user_journey[-30:]


def track_state_change(key: str, action: str, value):
    """Logs widget changes ONLY when the user actually changes a selection or value."""
    init_tracker()
    prev = st.session_state._tracked_values.get(key)
    if prev != value:
        st.session_state._tracked_values[key] = value
        if prev is None:
            log_user_step(f"Initial {action}", str(value))
        else:
            log_user_step(f"Changed {action}", f"{prev} -> {value}")


def update_app_snapshot(data: dict):
    """Updates live form values and configuration on screen."""
    init_tracker()
    st.session_state.app_snapshot.update(data)


def reset_generated_strategies():
    """Clears old strategy tabs right before a fresh prediction is generated."""
    init_tracker()
    st.session_state.app_snapshot["prediction_generated"] = True
    st.session_state.app_snapshot["generated_strategies"] = {}


def record_crop_strategy_tab(rank: int, tab_data: dict):
    """Stores full Mandi, Forecast, XAI, and Quality details for Rank 1, 2, and 3."""
    init_tracker()
    rank_labels = {1: "Primary Strategy", 2: "Alternative Option A", 3: "Alternative Option B"}
    label = rank_labels.get(rank, f"Option {rank}")
    st.session_state.app_snapshot.setdefault("generated_strategies", {})[label] = tab_data


# ==========================================
# 3. SYSTEM PROMPT BUILDER (RAG + LIVE STATE)
# ==========================================
def build_system_instruction() -> str:
    rag_text = load_rag_knowledge()
    journey_log = "\n".join(st.session_state.get("user_journey", [])) or "User just opened the app."
    live_snapshot = json.dumps(st.session_state.get("app_snapshot", {}), indent=2, ensure_ascii=False)

    return f"""
You are "Kisan Sahayak AI", the official intelligent assistant embedded inside Agri-Predictor Pro.

### STRICT LANGUAGE RULES:
1. Detect and match the exact language and script of the user's latest message:
   - **English** -> Reply in clear, crisp, structured English.
   - **Hindi (Devanagari, e.g., "मेरी फसल का भाव क्या है?")** -> Reply in simple, natural Devanagari Hindi.
   - **Hinglish (Hindi in Roman script, e.g., "bhai humidity kam kyun dikha raha hai?")** -> Reply in natural, conversational Hinglish (Roman script). Do NOT switch to pure Devanagari if the user wrote in Hinglish.
2. Keep answers concise, warm, and scannable (short paragraphs or bullet points) so they fit cleanly in a floating chat window and sound smooth when read aloud.
3. Address farmers respectfully (e.g., "Namaste Kisan Bhai").

### CONTEXT & DOMAIN RULES:
1. **Live Screen Awareness:** You have full visibility into the user's exact inputs, step-by-step history, and all 3 generated strategy tabs (Primary, Alternative A, Alternative B), including Mandi rates, 14-day sentiment, Explainable AI badges, and Crop Quality alerts. Quote their exact on-screen numbers naturally.
2. **Journey Guide:** If the user asks "what did I do?" / "maine kya kiya?" or seems confused, summarize their recent actions in simple words and tell them the exact next button to click.
3. **Zero ML Jargon:** Never say "Random Forest", "Softmax", "7D feature vector", or "Gini impurity" unless a judge/student explicitly asks for technical specs. Otherwise explain the AI as "250 virtual agricultural scientists voting together for your soil".
4. **Actionable Agronomic Help:** For `LOW (Action Needed)` factors, suggest practical field steps (e.g., irrigation/mulching for low humidity, Urea for low N, DAP for low P, MOP for low K). For `HIGH (Tolerable)` factors, remind them to save money by avoiding extra inputs.

### OFFICIAL KNOWLEDGE BASE (RAG):
{rag_text}

### USER'S STEP-BY-STEP JOURNEY ON THE WEBSITE:
{journey_log}

### LIVE DATA CURRENTLY ON USER'S SCREEN:
{live_snapshot}
"""


# ==========================================
# 4. GEMINI TEXT & VOICE HANDLERS
# ==========================================
def _build_history_contents():
    contents = []
    for msg in st.session_state.chat_messages[-10:]:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
    return contents


def ask_kisan_ai_text(user_query: str) -> str:
    client = get_gemini_client()
    contents = _build_history_contents()
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_query)]))

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=build_system_instruction(),
                temperature=0.4,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
        return response.text
    except Exception as e:
        return f"Maaf kijiye, abhi AI server se connect nahi ho paaya. Kripya apni GEMINI_API_KEY check karein. ({e})"


def _is_audio_silent(audio_bytes: bytes, threshold: int = 250) -> bool:
    """Detects muted or near-silent mic recordings (Python 3.14 safe)."""
    try:
        with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
            frames = wf.readframes(wf.getnframes())
            if wf.getsampwidth() == 2 and frames:
                samples = array.array("h")
                samples.frombytes(frames)
                peak = max(abs(s) for s in samples) if samples else 0
                return peak < threshold
    except Exception:
        pass
    return len(audio_bytes) < 2000


def ask_kisan_ai_voice(audio_bytes: bytes) -> tuple[str, str]:
    """Step 1: Pure verbatim transcription (zero RAG bias). Step 2: Answer via Kisan AI."""
    if _is_audio_silent(audio_bytes):
        return (
            "(No sound detected)",
            "Mic se koi aawaz record nahi hui. Kripya browser mic permission check karein ya type karke poochein.",
        )

    client = get_gemini_client()
    try:
        trans_res = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                types.Part.from_text(
                    text=(
                        "Transcribe the exact words spoken in this audio verbatim. "
                        "The speaker may use English, Hindi, or Hinglish. "
                        "Output ONLY the exact spoken words. Do not answer and do not guess. "
                        "If there is no clear speech, output exactly: UNCLEAR"
                    )
                ),
            ],
            config=types.GenerateContentConfig(
                temperature=0.0,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
        transcript = (trans_res.text or "").strip()
    except Exception as e:
        return "(Voice error)", f"Aawaz process karne mein dikkat aayi. Kripya type karke poochein. ({e})"

    if not transcript or transcript.upper() == "UNCLEAR":
        return (
            "(Unclear audio)",
            "Aawaz saaf sunai nahi di. Kripya thoda saaf bolein ya neeche type karke poochein.",
        )

    reply = ask_kisan_ai_text(transcript)
    return transcript, reply
# ==========================================
# 5. ZERO-RELOAD CLIENT-SIDE VOICE PLAYER
# ==========================================
def render_voice_player(text_to_speak: str):
    """Browser-native Web Speech API Play/Stop pill (zero Python reruns)."""
    clean_text = re.sub(r"[*_`#>-]", " ", text_to_speak)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    has_hindi = bool(re.search(r"[\u0900-\u097F]", clean_text))
    default_lang = "hi-IN" if has_hindi else "en-IN"
    safe_json_text = json.dumps(clean_text)

    components.html(
        f"""
        <div style="display:flex; align-items:center; gap:8px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin-top:2px;">
            <button onclick="speakText()" style="
                background:#1e8449; color:#ffffff; border:none; border-radius:20px;
                padding:5px 12px; font-size:12px; font-weight:600; cursor:pointer;">
                🔊 Suniye / Listen
            </button>
            <button onclick="stopText()" style="
                background:#f1f5f9; color:#334155; border:1px solid #cbd5e1; border-radius:20px;
                padding:5px 10px; font-size:12px; font-weight:600; cursor:pointer;">
                ⏹ Stop
            </button>
            <select id="langSelect" style="
                font-size:11px; padding:4px 6px; border-radius:12px;
                border:1px solid #cbd5e1; background:#ffffff; color:#334155;">
                <option value="hi-IN" {"selected" if default_lang == "hi-IN" else ""}>हिंदी (HI)</option>
                <option value="en-IN" {"selected" if default_lang == "en-IN" else ""}>English / Hinglish</option>
            </select>
        </div>
        <script>
            const msgText = {safe_json_text};
            function speakText() {{
                if (!('speechSynthesis' in window)) {{
                    alert('Browser does not support Voice Playback.');
                    return;
                }}
                window.speechSynthesis.cancel();
                const utter = new SpeechSynthesisUtterance(msgText);
                const selectedLang = document.getElementById('langSelect').value;
                utter.lang = selectedLang;
                utter.rate = 0.96;
                const voices = window.speechSynthesis.getVoices();
                const match = voices.find(v => v.lang.startsWith(selectedLang.split('-')[0]));
                if (match) utter.voice = match;
                window.speechSynthesis.speak(utter);
            }}
            function stopText() {{
                if ('speechSynthesis' in window) window.speechSynthesis.cancel();
            }}
        </script>
        """,
        height=38,
    )


# ==========================================
# 6. FLOATING CHAT BUBBLE CSS (THEME-SAFE)
# ==========================================
def inject_floating_bubble_css():
    st.markdown(
        """
        <style>
        .st-key-kisan_floating_chat {
            position: fixed !important;
            bottom: 24px !important;
            right: 24px !important;
            z-index: 99999 !important;
            width: auto !important;
        }

        .st-key-kisan_floating_chat button[data-testid="stPopoverButton"] {
            background: linear-gradient(135deg, #27ae60 0%, #1b5e20 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 9999px !important;
            padding: 12px 22px !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            box-shadow: 0 8px 24px rgba(27, 94, 32, 0.38) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }

        /* Override main2.py global p/span/div color inside the green launcher button */
        .st-key-kisan_floating_chat button[data-testid="stPopoverButton"] p,
        .st-key-kisan_floating_chat button[data-testid="stPopoverButton"] span,
        .st-key-kisan_floating_chat button[data-testid="stPopoverButton"] div,
        .st-key-kisan_floating_chat button[data-testid="stPopoverButton"] svg {
            color: #ffffff !important;
            fill: #ffffff !important;
        }

        .st-key-kisan_floating_chat button[data-testid="stPopoverButton"]:hover {
            transform: translateY(-2px) scale(1.03) !important;
            box-shadow: 0 12px 28px rgba(27, 94, 32, 0.48) !important;
        }

        div[data-testid="stPopoverBody"] {
            width: 400px !important;
            max-width: 92vw !important;
            border-radius: 18px !important;
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.20) !important;
            border: 1px solid rgba(39, 174, 96, 0.28) !important;
            padding: 14px !important;
        }

        @media (max-width: 600px) {
            .st-key-kisan_floating_chat {
                bottom: 16px !important;
                right: 16px !important;
            }
            .st-key-kisan_floating_chat button[data-testid="stPopoverButton"] {
                padding: 10px 16px !important;
                font-size: 14px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# 7. NON-RELOADING FLOATING CHATBOT UI
# ==========================================
@st.fragment
def render_kisan_chatbot():
    init_tracker()
    inject_floating_bubble_css()

    with st.container(key="kisan_floating_chat"):
        with st.popover("💬 Kisan Sahayak AI"):
            hdr_col1, hdr_col2 = st.columns([4, 1])
            hdr_col1.markdown("#### 🌱 Kisan Sahayak AI")
            if hdr_col2.button("🗑️", help="Clear chat", use_container_width=True):
                st.session_state.chat_messages = st.session_state.chat_messages[:1]
                st.session_state.last_audio_hash = None
                st.rerun(scope="fragment")

            st.caption("English • हिंदी • Hinglish | Live Screen & Voice Aware")

            q1, q2 = st.columns(2)
            quick_prompt = None
            if q1.button("📊 Result Samjhao", use_container_width=True):
                quick_prompt = "Mere screen par jo crop result, mandi bhav, aur warnings aaye hain unhe simple Hinglish mein samjhao."
            if q2.button("🧭 Next Step?", use_container_width=True):
                quick_prompt = "Maine abhi tak website par kya kiya hai aur mujhe aage kya karna chahiye?"

            chat_box = st.container(height=300, border=True)
            with chat_box:
                for msg in st.session_state.chat_messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            last_assistant_msg = next(
                (m["content"] for m in reversed(st.session_state.chat_messages) if m["role"] == "assistant"),
                None,
            )
            if last_assistant_msg:
                render_voice_player(last_assistant_msg)

            with st.form("kisan_chat_form", clear_on_submit=True, border=False):
                in_col, btn_col = st.columns([4.2, 1])
                typed_prompt = in_col.text_input(
                    "Message",
                    placeholder="Type in English, Hindi, or Hinglish...",
                    label_visibility="collapsed",
                )
                submitted = btn_col.form_submit_button("➤", use_container_width=True)

            audio_file = st.audio_input("🎙️ Bol kar poochein (Hindi / Hinglish / English)", sample_rate=16000, key=f"kisan_mic_{st.session_state.get('mic_counter', 0)}") if ENABLE_VOICE_INPUT else None

            active_text = quick_prompt or (typed_prompt.strip() if submitted and typed_prompt.strip() else None)
            if active_text:
                st.session_state.chat_messages.append({"role": "user", "content": active_text})
                with st.spinner("Soch raha hoon..."):
                    reply = ask_kisan_ai_text(active_text)
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun(scope="fragment")

            if audio_file is not None:
                audio_bytes = audio_file.getvalue()
                audio_hash = hashlib.md5(audio_bytes).hexdigest()
                if audio_hash != st.session_state.last_audio_hash:
                    st.session_state.last_audio_hash = audio_hash
                    with st.spinner("Aapki aawaz sun raha hoon..."):
                        transcript, reply = ask_kisan_ai_voice(audio_bytes)
                    st.session_state.chat_messages.append({"role": "user", "content": f"🎙️ {transcript}"})
                    st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                    st.rerun(scope="fragment")
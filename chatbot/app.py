import streamlit as st
import requests
import json
import uuid
import os

# Konfiguration der Seite

st.set_page_config(page_title="Ask Me Anything", page_icon="🗣", layout="centered")

# Get API base URL from environment variable or use default
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost")
API_PORT = os.environ.get("API_PORT", "8001")

# Determine the correct API URL
# If API_BASE_URL is localhost, use port 8000 (internal container communication)
# Otherwise use the external port (for browser access from outside)
if "localhost" in API_BASE_URL or "127.0.0.1" in API_BASE_URL:
    API_URL = f"{API_BASE_URL}:8000/chat"
else:
    API_URL = f"{API_BASE_URL}:{API_PORT}/chat"

print(f"API_URL: {API_URL}")


# CSS für besseres Styling
st.markdown(
    """
<style>
    /* Streamlit UI Elemente ausblenden */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: white;
    }
    .chat-message.bot {
        background-color: #f0f2f6;
    }
    .chat-message .avatar {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    .input-container {
        position: sticky;
        bottom: 0;
        background-color: white;
        padding: 1rem 0;
        z-index: 100;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialisierung des Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_state" not in st.session_state:
    st.session_state.current_state = "irina"
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Titel und Beschreibung

st.title("🗣 Ask Me Anything")
st.markdown("""
Chatte mit Youssef, Irina, Rami, oder Duygu! 
Wähle einfach mit wem du sprechen möchtest und stelle deine Fragen.  

**Hinweis:** Bitte beachte, dass dies eine Simulation ist und nicht als Ersatz für echte Gespräche oder Beratungen dienen soll. Es ist wichtig, sich an Fachleute zu wenden, wenn du persönliche oder sensible Themen besprechen möchtest.
""")


# Status-Anzeige

# print("state", st.session_state.current_state)


st.markdown("### Wähle einen Charakter:")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("👵🏻 Irina"):
        st.session_state.current_state = "irina"
        st.session_state.messages = []
        st.session_state.last_input = ""  # Reset last input!
        st.rerun()

with col2:
    if st.button("👨🏿‍💻 Youssef"):
        st.session_state.current_state = "youssef"
        st.session_state.messages = []
        st.session_state.last_input = ""
        st.rerun()

with col3:
    if st.button("🧑🏽 Rami"):
        st.session_state.current_state = "rami"
        st.session_state.messages = []
        st.session_state.last_input = ""
        st.rerun()

with col4:
    if st.button("🧕 Duygu"):
        st.session_state.current_state = "duygu"
        st.session_state.messages = []
        st.session_state.last_input = ""
        st.rerun()

if "youssef" in st.session_state.current_state :
    state_emoji = "👨🏿‍💻"
elif "irina" in st.session_state.current_state :
    state_emoji = "👵🏻"
elif "rami" in st.session_state.current_state :
    state_emoji = "🧑🏽"
elif "duygu" in st.session_state.current_state :
    state_emoji = "🧕"

st.markdown(f"**Aktueller Charakter:** {state_emoji}")

# Chat-Verlauf anzeigen
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(
                f"""
            <div class="chat-message user">
                <div>👤 <b>Du:</b></div>
                <div>{message["content"]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
            <div class="chat-message bot">
                <div>{state_emoji} <b>Bot:</b></div>
                <div>{message["content"]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

# --- Chatbot is typing indicator logic ---
if "is_replying" not in st.session_state:
    st.session_state.is_replying = False
if "pending_user_input" not in st.session_state:
    st.session_state.pending_user_input = None


# Zähle die Anzahl der User-Nachrichten (muss vor dem Input-Feld passieren)
user_message_count = sum(1 for msg in st.session_state.messages if msg["role"] == "user")

# Eingabefeld in einem Container
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    user_input = st.text_input(
        "Deine Nachricht:",
        key=f"user_input_{st.session_state.input_key}",
        disabled=st.session_state.is_replying or user_message_count >= 5
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Step 1: User submits a message
if user_input and user_input != st.session_state.last_input and not st.session_state.is_replying:
    st.session_state.pending_user_input = user_input
    st.session_state.is_replying = True
    st.rerun()

# Step 2: If there is a pending message, send it to the API
if st.session_state.is_replying and st.session_state.pending_user_input:
    st.info("🤖 Der Chatbot schreibt ...")
    # Nachricht zum Chat-Verlauf hinzufügen
    st.session_state.messages.append({"role": "user", "content": st.session_state.pending_user_input})
    st.session_state.last_input = st.session_state.pending_user_input

    # Zähle die Anzahl der User-Nachrichten
    user_message_count = sum(1 for msg in st.session_state.messages if msg["role"] == "user")

    # API-Anfrage senden
    try:
        response = requests.post(
            API_URL,
            json={
                "message": st.session_state.pending_user_input,
                "chat_history": [msg["content"] for msg in st.session_state.messages],
                "session_id": st.session_state.session_id,
                "state": st.session_state.current_state,
                "user_message_count": user_message_count
            },
        )
        response_data = response.json()

        # Bot-Antwort zum Chat-Verlauf hinzufügen
        st.session_state.messages.append(
            {"role": "bot", "content": response_data["response"]}
        )
        st.session_state.current_state = response_data["state"]

        # Sende eine benutzerdefinierte Nachricht nach 5 User-Nachrichten
        if user_message_count == 5:
            # Serialize chat history as readable string
            chat_history_str = "\n".join([
                f"{'Du' if m['role']=='user' else 'Bot'}: {m['content']}" for m in st.session_state.messages
            ])
            import urllib.parse
            chat_history_encoded = urllib.parse.quote(chat_history_str)
            google_form_url = (
                "https://docs.google.com/forms/d/e/1FAIpQLSeRHVcJZcJeFivyZ6PBgJMq9KZ4OxUySr3tpQHwyZfGz5QdeA/viewform"
                "?usp=pp_url"
                "&entry.677084014=" + chat_history_encoded
            )
            st.session_state.messages.append(
                {"role": "bot", "content": f"Danke für das Gespräch. Bitte fülle das Formular aus: <a href='{google_form_url}' target='_blank'>Formular öffnen</a>"}
            )

        # Eingabefeld leeren durch Erhöhung des Keys
        st.session_state.input_key += 1
        st.session_state.is_replying = False
        st.session_state.pending_user_input = None
        st.rerun()

    except Exception as e:
        st.session_state.is_replying = False
        st.session_state.pending_user_input = None
        st.error(f"Fehler bei der Kommunikation mit dem Server: {str(e)}")

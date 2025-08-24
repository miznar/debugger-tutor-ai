import streamlit as st
from core.parser import parse_code, SUPPORTED_LANGS
from core.debug_agent import debug_code, llm_status
from utils.detect_language import detect_language
from core.snippets import EXAMPLES

# Page Config
st.set_page_config(page_title="AI Code Debugging Tutor", page_icon="🧑‍🏫", layout="wide")

# Custom Header
st.markdown(
    """
    <h1 style="text-align:center;">🧑‍🏫 AI Code Debugging Tutor</h1>
    <p style="text-align:center; color:gray; font-size:16px;">
        Paste your buggy code, upload a file, or load an example.<br>
        The app will parse it (AST) and explain issues with fixes.
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/bug.png", use_container_width=True)
st.sidebar.title("⚙️ Settings")

lang_choice = st.sidebar.selectbox("Choose Language", SUPPORTED_LANGS, index=0)
st.sidebar.caption(f"LLM status: **{llm_status()}**")

st.sidebar.subheader("📂 Examples")
example_lang = st.sidebar.selectbox("Load Example Snippet", ["(none)"] + SUPPORTED_LANGS, index=0)

# Code Input
st.markdown("### ✍️ Input Code")
uploaded_file = st.file_uploader("Upload a code file", type=["py", "js", "cpp", "java"])

default_code = EXAMPLES.get(example_lang, "") if example_lang in EXAMPLES else ""
code_input = st.text_area("Or paste your code here:", value=default_code, height=260)

# Detect Language
lang = lang_choice
if uploaded_file:
    lang = detect_language(uploaded_file.name)
    code = uploaded_file.read().decode("utf-8", errors="replace")
else:
    code = code_input

# Layout
colA, colB = st.columns([1, 1])

with colA:
    if st.button("🔍 Analyze & Debug", use_container_width=True) and code.strip():
        with st.spinner("Analyzing your code and generating explanation..."):
            try:
                ast = parse_code(code, lang)
            except Exception as e:
                ast = f"(Failed to parse AST) {e}"

            explanation = debug_code(code, lang, ast)

        st.success("Debugging complete!")
        st.subheader("🛠️ Explanation & Fixes")
        st.write(explanation)

        # Downloadable Report
        report = (
            f"Language: {lang}\n\n"
            f"--- CODE ---\n{code}\n\n"
            f"--- AST ---\n{ast}\n\n"
            f"--- EXPLANATION ---\n{explanation}\n"
        )
        st.download_button("⬇️ Download Report (.txt)", report, file_name="debug_report.txt", use_container_width=True)

with colB:
    if code.strip():
        st.subheader("📊 Parsed AST Tree")
        st.code(parse_code(code, lang), language="text")
    else:
        st.info("ℹ️ Paste some code or load an example to see the AST here.")

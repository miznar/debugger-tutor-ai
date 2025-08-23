import streamlit as st
from core.parser import parse_code, SUPPORTED_LANGS
from core.debug_agent import debug_code, llm_status
from utils.detect_language import detect_language
from core.snippets import EXAMPLES

st.set_page_config(page_title="AI Code Debugging Tutor", page_icon="🧑‍🏫", layout="wide")
st.title("🧑‍🏫 AI Code Debugging Tutor")
st.write("Paste code or upload a file. I’ll parse it (AST) and explain bugs with suggested fixes.")

# Sidebar
st.sidebar.header("Settings")
lang_choice = st.sidebar.selectbox("Language", SUPPORTED_LANGS, index=0)
st.sidebar.caption(f"LLM status: **{llm_status()}**")

example_lang = st.sidebar.selectbox("Load example snippet", ["(none)"] + SUPPORTED_LANGS, index=0)

# Inputs
uploaded_file = st.file_uploader("Upload a code file", type=["py", "js", "cpp", "java"])
default_code = EXAMPLES.get(example_lang, "") if example_lang in EXAMPLES else ""
code_input = st.text_area("Or paste your code here:", value=default_code, height=260)

# Determine language
lang = lang_choice
if uploaded_file:
    lang = detect_language(uploaded_file.name)
    code = uploaded_file.read().decode("utf-8", errors="replace")
else:
    code = code_input

colA, colB = st.columns([1, 1])
with colA:
    if st.button("🔍 Analyze & Debug", use_container_width=True) and code.strip():
        with st.spinner("Parsing code and generating explanation..."):
            try:
                ast = parse_code(code, lang)
            except Exception as e:
                ast = f"(Failed to parse AST) {e}"

            explanation = debug_code(code, lang, ast)

        st.subheader("🛠️ Debugging Explanation & Fixes")
        st.write(explanation)

        # Downloadable report
        report = (
            f"Language: {lang}\n\n"
            f"--- CODE ---\n{code}\n\n"
            f"--- AST ---\n{ast}\n\n"
            f"--- EXPLANATION ---\n{explanation}\n"
        )
        st.download_button("⬇️ Download Report (.txt)", report, file_name="debug_report.txt", use_container_width=True)

with colB:
    if code.strip():
        st.subheader("📊 Code AST")
        st.code(parse_code(code, lang), language="text")
    else:
        st.info("Paste code or load an example to see the AST here.")

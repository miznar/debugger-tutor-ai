import os
from typing import Literal

# Prefer modern LangChain OpenAI client; graceful fallback if not installed or quota exceeded.
def llm_status() -> Literal["ready", "no_api_key", "quota_or_offline"]:
    if not os.getenv("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"):
        return "no_api_key"
    return "ready"

_SYSTEM = (
    "You are an expert AI coding tutor that helps debug code. "
    "Be concise, explain each error clearly, point to the exact line/construct, "
    "and propose a corrected version of the code."
)

_TEMPLATE = (
    "Language: {lang}\n\n"
    "Code:\n```{lang}\n{code}\n```\n\n"
    "AST:\n{ast}\n\n"
    "Please:\n"
    "1) List errors (syntax, name, type, logic) with short explanations.\n"
    "2) Provide a corrected code block.\n"
    "3) Add 2-3 quick tips to avoid such bugs."
)

def _llm_explain(code: str, lang: str, ast: str) -> str:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema.output_parser import StrOutputParser

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_messages(
        [("system", _SYSTEM), ("human", _TEMPLATE)]
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"code": code, "lang": lang, "ast": ast})

def _fallback_explain(code: str, lang: str, ast: str, err: Exception | None) -> str:
    msg = (
        "⚠️ LLM unavailable (no API key or quota exceeded). "
        "Here’s a quick rule-based review + your AST so you can keep working.\n\n"
    )
    hints = []
    if lang == "python":
        if "def " in code and ":" not in code.split("def ", 1)[1].split("\n", 1)[0]:
            hints.append("Missing `:` after function definition.")
        if "(" in code and ")" not in code:
            hints.append("Possibly missing closing `)` in a call.")
    if "return a + c" in code:
        hints.append("Using undefined variable `c`; did you mean `b`?")
    if not hints:
        hints = ["Check for unmatched brackets/quotes.", "Verify variable names.", "Run linter/formatter."]

    return msg + "• " + "\n• ".join(hints) + "\n\n" + "AST:\n" + ast

def debug_code(code: str, lang: str, ast: str) -> str:
    if llm_status() != "ready":
        return _fallback_explain(code, lang, ast, None)
    try:
        return _llm_explain(code, lang, ast)
    except Exception as e:
        return _fallback_explain(code, lang, ast, e)

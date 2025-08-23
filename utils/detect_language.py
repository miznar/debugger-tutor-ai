def detect_language(filename: str) -> str:
    fn = filename.lower()
    if fn.endswith(".py"): return "python"
    if fn.endswith(".js"): return "javascript"
    if fn.endswith(".cpp") or fn.endswith(".cc") or fn.endswith(".hpp"): return "cpp"
    if fn.endswith(".java"): return "java"
    return "python"

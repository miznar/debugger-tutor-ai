from functools import lru_cache
from tree_sitter import Parser

SUPPORTED_LANGS = ["python", "javascript", "cpp", "java"]

@lru_cache(maxsize=None)
def _load_language(lang: str):
    """
    Try both APIs:
    1) get_language("python")  (works with tree-sitter-languages 1.10.2)
    2) per-language callables: python(), javascript(), cpp(), java()
    """
    assert lang in SUPPORTED_LANGS, f"Unsupported language: {lang}"

    # Try get_language API
    try:
        from tree_sitter_languages import get_language
        return get_language(lang)
    except Exception:
        pass

    # Try per-language callables
    try:
        from tree_sitter_languages import python as py, javascript as js, cpp as cc, java as jv
        mapping = {
            "python": py(),
            "javascript": js(),
            "cpp": cc(),
            "java": jv(),
        }
        return mapping[lang]
    except Exception as e:
        raise RuntimeError(f"Could not load language '{lang}': {e}")

def parse_code(code: str, lang: str = "python") -> str:
    if lang not in SUPPORTED_LANGS:
        return f"Language '{lang}' not supported yet."
    parser = Parser()
    language = _load_language(lang)
    parser.set_language(language)
    tree = parser.parse(code.encode("utf-8"))
    return tree.root_node.sexp()

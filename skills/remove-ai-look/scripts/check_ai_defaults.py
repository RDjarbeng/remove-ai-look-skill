#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

ALLOWED_EXTENSIONS = {
    ".html", ".htm", ".css", ".scss",
    ".js", ".jsx", ".ts", ".tsx",
    ".vue", ".svelte", ".astro",
    ".md", ".mdx",
}

SKIPPED_DIRS = {
    "node_modules", ".git", "dist", "build",
    ".next", "coverage", "vendor",
}

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB

RE_STOCK_ACCENT = re.compile(
    r'(?<![\w-])(?:[a-zA-Z0-9_\-]+:)*(?:bg|text|border|ring|divide|outline|accent|shadow|fill|stroke|decoration|caret|placeholder)(?:-[a-z0-9]+)*-(?:indigo|violet|purple)-(?:50|100|200|300|400|500|600|700|800|900|950|\d+)(?:/[a-zA-Z0-9.]+)?(?![-\w])'
)

RE_FROM = re.compile(r'(?<![\w-])(?:[a-zA-Z0-9_\-]+:)*from-(?:purple|indigo|violet)-[a-zA-Z0-9]+(?![-\w])')
RE_TO = re.compile(r'(?<![\w-])(?:[a-zA-Z0-9_\-]+:)*to-(?:blue|pink|purple)-[a-zA-Z0-9]+(?![-\w])')
RE_GRADIENT_HEX = re.compile(r'#(?:6366f1|4f46e5|8b5cf6|7c3aed|a855f7)\b', re.I)

RE_ROUNDED_2XL_3XL = re.compile(r'(?<![\w-])(?:[a-zA-Z0-9_\-]+:)*rounded-(?:2xl|3xl)\b')
RE_ROUNDED_ANY = re.compile(r'(?<![\w-])(?:[a-zA-Z0-9_\-]+:)*rounded-[a-zA-Z0-9]+\b')
RE_SHADOW_LG_XL = re.compile(r'(?<![\w-])(?:[a-zA-Z0-9_\-]+:)*shadow-(?:lg|xl)\b')

RE_FONT_FAMILY_INTER = re.compile(
    r'''(?i)(?:font-family|fontFamily)\s*[:=]\s*(?:\[\s*)?['"]*(?:\\?['"])?Inter(?:\b|['",;\s])'''
)
RE_GOOGLE_FONTS_INTER = re.compile(
    r'''(?i)fonts\.googleapis\.com/css2?\?(?:(?!family=)[^"'\s>])*family=Inter(?::|&|\||\+|%20|['"\s>])'''
)

MULTI_WORD_COPY_PATTERNS = [
    re.compile(r'\b(?:empower|unlock|transform)\s+your(?:\s+[\w\'-]+){0,6}', re.I),
    re.compile(r'\bseamless\s+integration\b', re.I),
    re.compile(r'\bbuilt\s+for\s+modern\s+teams\b', re.I),
    re.compile(r'\btake\s+your\s+[\w\s\'-]{1,30}?\s+to\s+the\s+next\s+level\b', re.I),
]
RE_REVOLUTIONIZE = re.compile(r'\brevolutionize\w*\b', re.I)


def check_stock_accent(line: str):
    stripped = line.strip()
    if stripped.startswith(("//", "/*", "*", "<!--")):
        return []
    return [m.group(0) for m in RE_STOCK_ACCENT.finditer(line)]


def check_stock_gradient(line: str, in_gradient_block: bool):
    stripped = line.strip()
    if stripped.startswith(("//", "/*", "*", "<!--")):
        return [], in_gradient_block

    results = []
    m_from = RE_FROM.search(line)
    m_to = RE_TO.search(line)
    if m_from and m_to:
        results.append(f"{m_from.group(0)} {m_to.group(0)}")

    has_lg = bool(re.search(r'linear-gradient', line, re.I))
    if has_lg:
        # Track whether a multi-line gradient statement opened without closing
        open_count = line.count("(")
        close_count = line.count(")")
        in_gradient_block = open_count > close_count
    elif in_gradient_block and ")" in line:
        in_gradient_block = False

    if has_lg or in_gradient_block:
        m_hex = RE_GRADIENT_HEX.search(line)
        if m_hex:
            m_full = re.search(r'linear-gradient\([^)]*#(?:6366f1|4f46e5|8b5cf6|7c3aed|a855f7)[^)]*\)', line, re.I)
            if m_full:
                results.append(m_full.group(0))
            else:
                results.append(f"linear-gradient with {m_hex.group(0)}")

    return results, in_gradient_block


def check_reflex_card(line: str):
    stripped = line.strip()
    if stripped.startswith(("//", "/*", "*", "<!--")):
        return []

    m_2xl_3xl = RE_ROUNDED_2XL_3XL.search(line)
    m_rounded = RE_ROUNDED_ANY.search(line)
    m_shadow = RE_SHADOW_LG_XL.search(line)

    results = []
    if m_2xl_3xl and m_shadow:
        results.append(f"{m_2xl_3xl.group(0)} {m_shadow.group(0)}")
    elif m_2xl_3xl:
        results.append(m_2xl_3xl.group(0))
    elif m_rounded and m_shadow:
        results.append(f"{m_rounded.group(0)} {m_shadow.group(0)}")

    return results


def check_stock_font(line: str):
    stripped = line.strip()
    if stripped.startswith(("//", "/*", "*", "<!--")):
        return []

    results = []
    m_ff = RE_FONT_FAMILY_INTER.search(line)
    if m_ff:
        results.append(m_ff.group(0).strip())

    m_gf = RE_GOOGLE_FONTS_INTER.search(line)
    if m_gf:
        results.append(m_gf.group(0).strip())

    return results


def check_stock_copy(line: str, ext: str):
    stripped = line.strip()
    if not stripped:
        return []

    if stripped.startswith(("//", "/*", "*", "<!--", "-->", "*/")):
        return []

    # In CSS, user-facing text is only found inside content declarations
    if ext in (".css", ".scss"):
        content_matches = re.findall(r'content\s*:\s*(["\'])(.*?)\1', line, re.I)
        if not content_matches:
            return []
        scan_text = " ".join(m[1] for m in content_matches)
    else:
        # Strip comments
        scan_text = re.sub(r'<!--.*?-->', '', line)
        scan_text = re.sub(r'(?<!:)\/\/.*$', '', scan_text)
        scan_text = re.sub(r'/\*.*?\*/', '', scan_text)

    if not scan_text.strip():
        return []

    results = []
    for pat in MULTI_WORD_COPY_PATTERNS:
        for m in pat.finditer(scan_text):
            results.append(m.group(0).strip())

    # Distinguish user-facing prose from code identifiers for "revolutionize"
    for m in RE_REVOLUTIONIZE.finditer(scan_text):
        start, end = m.span()
        before = scan_text[:start]
        after = scan_text[end:]
        # Skip import / variable / function declaration statements
        if re.search(r'\b(?:function|const|let|var|class|interface|type)\s+$', before):
            continue
        if re.search(r'\bimport\b.*\bfrom\b', scan_text) or re.search(r'\bexport\b', before):
            continue
        if re.match(r'^\s*[:=(]', after):
            continue
        results.append(m.group(0).strip())

    return results


def should_skip_file(path: Path) -> bool:
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return True
    if ".min." in path.name:
        return True
    try:
        if path.stat().st_size > MAX_FILE_SIZE:
            return True
    except OSError:
        return True
    return False


def collect_files(paths):
    for raw_path in paths:
        p = Path(raw_path)
        if not p.exists():
            continue
        if p.is_file():
            if any(part in SKIPPED_DIRS for part in p.parts):
                continue
            if not should_skip_file(p):
                yield p
        elif p.is_dir():
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIPPED_DIRS]
                for f in files:
                    file_path = Path(root) / f
                    if not should_skip_file(file_path):
                        yield file_path


def scan_file(filepath: Path):
    findings = []
    ext = filepath.suffix.lower()
    in_gradient_block = False

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                for text in check_stock_accent(line):
                    findings.append((line_no, "stock-accent", text))

                grad_findings, in_gradient_block = check_stock_gradient(line, in_gradient_block)
                for text in grad_findings:
                    findings.append((line_no, "stock-gradient", text))

                for text in check_reflex_card(line):
                    findings.append((line_no, "reflex-card", text))

                for text in check_stock_font(line):
                    findings.append((line_no, "stock-font", text))

                for text in check_stock_copy(line, ext):
                    findings.append((line_no, "stock-copy", text))
    except Exception:
        pass

    return findings


def main():
    if len(sys.argv) < 2:
        print("Usage: check_ai_defaults.py PATH [PATH ...]")
        sys.exit(2)

    counts = {
        "stock-accent": 0,
        "stock-gradient": 0,
        "reflex-card": 0,
        "stock-font": 0,
        "stock-copy": 0,
    }

    total_findings = 0
    paths = sys.argv[1:]

    for filepath in collect_files(paths):
        display_path = str(filepath).replace("\\", "/")
        findings = scan_file(filepath)
        for line_no, rule, matched_text in findings:
            counts[rule] += 1
            total_findings += 1
            formatted = f"{display_path}:{line_no}: {rule}: {matched_text}"
            if len(formatted) > 160:
                formatted = formatted[:160]
            print(formatted)

    summary = (
        f"Summary: {total_findings} finding{'s' if total_findings != 1 else ''} "
        f"(stock-accent: {counts['stock-accent']}, "
        f"stock-gradient: {counts['stock-gradient']}, "
        f"reflex-card: {counts['reflex-card']}, "
        f"stock-font: {counts['stock-font']}, "
        f"stock-copy: {counts['stock-copy']})"
    )
    print(summary)

    sys.exit(1 if total_findings > 0 else 0)


if __name__ == "__main__":
    main()

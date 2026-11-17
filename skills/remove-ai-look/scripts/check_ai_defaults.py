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
    re.compile(r'\b(?:supercharge|elevate)\s+your(?:\s+[\w\'-]+){0,6}', re.I),
    re.compile(r'\bharness\s+the\s+power\s+of\b', re.I),
    re.compile(r'\b(?:cutting-edge|next-gen(?:eration)?|blazing(?:ly)?[- ]fast|lightning[- ]fast)\b', re.I),
    re.compile(r'\b(?:system|engine|core|neural\s+core)\s+(?:online|active|engaged|armed)\b', re.I),
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


# ---- Mission-control / glow / glass / emoji rules -------------------------

RE_HEX = re.compile(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
RE_RGB = re.compile(r'rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})')
RE_NEON_NAME = re.compile(r'(?i)(?:--|\$)[\w-]*(?:neon|phosphor|glow)[\w-]*(?=\s*:)')

RE_GLOW_SHADOW = re.compile(
    r'(?i)(?:box-shadow|text-shadow|boxShadow|textShadow)\s*[:=]\s*[\'"]?\s*(?:inset\s+)?0(?:px)?\s+0(?:px)?\s+(?!0(?:px)?\s)\d+(?:\.\d+)?px(?:\s+-?\d+px)?\s+(?!rgba?\(\s*0\s*,\s*0\s*,\s*0)(?:#|rgba?\(|hsla?\(|var\()'
)
RE_DROP_SHADOW_GLOW = re.compile(r'(?i)drop-shadow\(\s*0(?:px)?\s+0(?:px)?\s+\d+px\s+(?!rgba?\(\s*0\s*,\s*0\s*,\s*0)(?:#|rgba?\(|hsla?\(|var\()')
RE_CANVAS_GLOW = re.compile(r'\bshadowBlur\s*=\s*(?!0\b)\d+')
RE_TW_GLOW = re.compile(
    r'(?<![\w-])(?:[a-zA-Z0-9_\-]+:)*(?:shadow-(?:cyan|sky|teal|emerald|green|lime|fuchsia|pink|blue)-\d+(?:/\d+)?|drop-shadow-\[0_0_[^\]]+\]|shadow-\[0_0_[^\]]+\])'
)

RE_GLASS = re.compile(r'(?i)(?:backdrop-filter\s*:\s*[^;]*blur|backdropFilter\s*:\s*[\'"][^\'"]*blur|(?<![\w-])backdrop-blur(?:-[a-z0-9]+)?(?![\w-]))')
RE_GRADIENT_TEXT = re.compile(r'(?i)(?:(?:-webkit-)?background-clip\s*:\s*text|backgroundClip\s*:\s*[\'"]text|(?<![\w-])bg-clip-text(?![\w-]))')

RE_TW_DARK_NAVY = re.compile(r'(?<![\w-])(?:[a-zA-Z0-9_\-]+:)*bg-(?:slate|gray|zinc|neutral)-(?:900|950)(?![\w-])')
RE_BG_DECL = re.compile(r'(?i)(?:background(?:-color)?|--[\w-]*(?:bg|background|surface|panel|chassis|canvas)[\w-]*)\s*:')

RE_EMOJI = re.compile(
    '[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF\U0001F000-\U0001F2FF]'
)
RE_UI_TAG_TEXT = re.compile(r'(?i)<(?:button|a|h[1-6]|label|summary|th|option|span|div)\b[^>]*>([^<]*)')

RE_UPPERCASE = re.compile(r'(?i)(?:text-transform\s*:\s*uppercase|textTransform\s*:\s*[\'"]uppercase|(?<![\w-])uppercase(?![\w-]))')
RE_TRACKING = re.compile(r'(?i)(?:letter-spacing\s*:\s*0?\.\d+em|letterSpacing\s*:|(?<![\w-])tracking-(?:wide|wider|widest|\[[^\]]+\])(?![\w-]))')
RE_MONO_USE = re.compile(r'(?i)(?:font-family\s*:\s*var\(--[\w-]*mono[\w-]*\)|font-family\s*:\s*[^;]*monospace|(?<![\w-])font-mono(?![\w-]))')


def _hex_to_rgb(h):
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hsv(rgb):
    r, g, b = (c / 255 for c in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d == 0:
        hue = 0.0
    elif mx == r:
        hue = (60 * ((g - b) / d)) % 360
    elif mx == g:
        hue = 60 * ((b - r) / d) + 120
    else:
        hue = 60 * ((r - g) / d) + 240
    sat = 0 if mx == 0 else d / mx
    return hue, sat, mx


def _is_neon(rgb):
    hue, sat, val = _hsv(rgb)
    if sat < 0.85 or val < 0.9:
        return False
    # cyan/aqua, electric green/lime, hot magenta
    return 75 <= hue <= 200 or 285 <= hue <= 330


def _is_dark_navy(rgb):
    hue, sat, val = _hsv(rgb)
    return val <= 0.13 and sat >= 0.2 and 195 <= hue <= 250


def _colours(line):
    for m in RE_HEX.finditer(line):
        yield m.group(0), _hex_to_rgb(m.group(1))
    for m in RE_RGB.finditer(line):
        rgb = tuple(int(x) for x in m.groups())
        if all(c <= 255 for c in rgb):
            yield m.group(0), rgb


def _is_comment(line):
    return line.strip().startswith(("//", "/*", "*", "<!--"))


def check_neon(line: str):
    if _is_comment(line):
        return []
    results = [text for text, rgb in _colours(line) if _is_neon(rgb)]
    results += [m.group(0) for m in RE_NEON_NAME.finditer(line)]
    return results


def check_glow(line: str):
    if _is_comment(line):
        return []
    results = []
    for rx in (RE_GLOW_SHADOW, RE_DROP_SHADOW_GLOW, RE_CANVAS_GLOW, RE_TW_GLOW):
        results += [m.group(0) for m in rx.finditer(line)]
    return results


def check_dark_navy(line: str):
    if _is_comment(line):
        return []
    results = [m.group(0) for m in RE_TW_DARK_NAVY.finditer(line)]
    if RE_BG_DECL.search(line):
        results += [text for text, rgb in _colours(line) if _is_dark_navy(rgb)]
    return results


def check_glass(line: str):
    if _is_comment(line):
        return []
    return [m.group(0) for m in RE_GLASS.finditer(line)]


def check_gradient_text(line: str):
    if _is_comment(line):
        return []
    return [m.group(0) for m in RE_GRADIENT_TEXT.finditer(line)]


def check_emoji_ui(line: str, ext: str):
    if ext in (".md", ".mdx", ".css", ".scss") or _is_comment(line):
        return []
    results = []
    for m in RE_UI_TAG_TEXT.finditer(line):
        text = m.group(1)
        if RE_EMOJI.search(text):
            results.append(text.strip()[:60])
    return results


HUD_TYPE_THRESHOLD = 4
HUD_MONO_THRESHOLD = 8


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
    upper_lines, tracking_lines, mono_lines = [], [], []
    navy_findings = []

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

                for text in check_neon(line):
                    findings.append((line_no, "neon-color", text))

                for text in check_glow(line):
                    findings.append((line_no, "glow", text))

                for text in check_dark_navy(line):
                    navy_findings.append((line_no, "dark-navy", text))

                for text in check_glass(line):
                    findings.append((line_no, "glass", text))

                for text in check_gradient_text(line):
                    findings.append((line_no, "gradient-text", text))

                for text in check_emoji_ui(line, ext):
                    findings.append((line_no, "emoji-ui", text))

                if not _is_comment(line):
                    if RE_UPPERCASE.search(line):
                        upper_lines.append(line_no)
                    if RE_TRACKING.search(line):
                        tracking_lines.append(line_no)
                    if RE_MONO_USE.search(line):
                        mono_lines.append(line_no)
    except Exception:
        pass

    # Dark blue-black surfaces are fine alone (e.g. GitHub dark); they are the
    # mission-control fingerprint only when paired with neon accents.
    if any(rule == "neon-color" for _, rule, _ in findings):
        findings.extend(navy_findings)
    if len(upper_lines) >= HUD_TYPE_THRESHOLD and len(tracking_lines) >= HUD_TYPE_THRESHOLD:
        findings.append((upper_lines[0], "hud-type",
                         f"{len(upper_lines)} uppercase + {len(tracking_lines)} letter-spaced rules (caps labels everywhere)"))
    if len(mono_lines) >= HUD_MONO_THRESHOLD:
        findings.append((mono_lines[0], "hud-type",
                         f"monospace used in {len(mono_lines)} places (mono beyond code and numbers)"))
    findings.sort(key=lambda f: f[0])

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
        "neon-color": 0,
        "glow": 0,
        "dark-navy": 0,
        "glass": 0,
        "gradient-text": 0,
        "emoji-ui": 0,
        "hud-type": 0,
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

    breakdown = ", ".join(f"{rule}: {n}" for rule, n in counts.items())
    summary = (
        f"Summary: {total_findings} finding{'s' if total_findings != 1 else ''} "
        f"({breakdown})"
    )
    if total_findings == 0:
        summary += "\nNo known fingerprints found. This does not prove the page looks designed: check it by eye too."
    print(summary)

    sys.exit(1 if total_findings > 0 else 0)


if __name__ == "__main__":
    main()

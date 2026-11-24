"""
Unicode Tamil letter classification and syllable decomposition utilities.
Zero-dependency, pure Python.
"""

# Tamil Unicode code points
UYIR = {
    'அ': 'a', 'ஆ': 'aa', 'இ': 'i', 'ஈ': 'ee', 'உ': 'u', 'ஊ': 'oo',
    'எ': 'e', 'ஏ': 'e', 'ஐ': 'ai', 'ஒ': 'o', 'ஓ': 'o', 'ஔ': 'au'
}

AYTHAM = {'ஃ': 'h'}

PULLI = '\u0BCD'  # Virama (pulli)

MEI_BASES = {
    'க': 'k', 'ங': 'ng', 'ச': 's', 'ஞ': 'gn', 'ட': 't', 'ண': 'n',
    'த': 'th', 'ந': 'n', 'ப': 'p', 'ம': 'm', 'ய': 'y', 'ர': 'r',
    'ல': 'l', 'வ': 'v', 'ழ': 'zh', 'ள': 'l', 'ற': 'r', 'ன': 'n',
    'ஜ': 'j', 'ஷ': 'sh', 'ஸ': 's', 'ஹ': 'h', 'க்ஷ': 'ksh'
}

VOWEL_SIGNS = {
    '\u0BBE': 'aa',  # ா
    '\u0BBF': 'i',   # ி
    '\u0BC0': 'ee',  # ீ
    '\u0BC1': 'u',   # ு
    '\u0BC2': 'oo',  # ூ
    '\u0BC6': 'e',   # ெ
    '\u0BC7': 'e',   # ே
    '\u0BC8': 'ai',  # ை
    '\u0BCA': 'o',   # ொ
    '\u0BCB': 'o',   # ோ
    '\u0BCC': 'au',  # ௌ
}

def split_tamil_letters(text: str) -> list[str]:
    """
    Splits Tamil text into individual phonetic graphemes/syllables.
    Preserves non-Tamil characters as-is.
    """
    if not text:
        return []
        
    letters = []
    i = 0
    n = len(text)
    
    while i < n:
        char = text[i]
        
        # Check for Grantha Sri (ஸ + ் + ர + ீ)
        if text[i:i+4] == 'ஸ்ரீ':
            letters.append('ஸ்ரீ')
            i += 4
            continue
            
        # Check if Tamil Unicode block
        if '\u0B80' <= char <= '\u0BFF':
            if char in UYIR or char in AYTHAM:
                letters.append(char)
                i += 1
            elif char in MEI_BASES or char in ['ஜ', 'ஷ', 'ஸ', 'ஹ']:
                if i + 1 < n and text[i+1] == PULLI:
                    letters.append(text[i:i+2])
                    i += 2
                elif i + 1 < n and text[i+1] in VOWEL_SIGNS:
                    letters.append(text[i:i+2])
                    i += 2
                else:
                    letters.append(char)
                    i += 1
            else:
                letters.append(char)
                i += 1
        else:
            letters.append(char)
            i += 1
            
    return letters

def is_tamil(text: str) -> bool:
    """Checks if text contains any Tamil characters."""
    return any('\u0B80' <= c <= '\u0BFF' for c in text)

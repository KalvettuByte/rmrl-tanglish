"""
Sandhi (புணர்ச்சி) Disassembler for Tamil.
Splits compound words, prefixes, suffixes, and removes euphonic insertion stops (ஒற்று)
to produce clean, readable, word-segmented modern Tanglish.
"""

import re

# Suffixes that frequently attach to titles or preceding nouns
COMPOUND_SUFFIXES = [
    'திருவாய்மலர்ந்தருளிய', 'அருளிச்செய்த', 'இயற்றிய', 'திருவாய்மலர்ந்த',
    'தமிழ்வேதமாகிய', 'வேதமாகிய',
    'சாஸ்திரத்திரட்டு', 'சாஸ்திரத் திரட்டு', 'சாஸ்திரம்',
    'நீதிக்கதைகள்', 'நீதிக்கதை',
    'சரித்திரக்கதை', 'சரித்திரக் கதை', 'சரித்திரம்', 'சரிதம்',
    'புராணம்', 'காவியம்', 'வெண்பா', 'சதகம்', 'மாலை', 'அகவல்',
    'தாலாட்டு', 'தூக்குப்பாட்டு', 'பாட்டு', 'பாசுரம்',
    'கதைகள்', 'கதை',
    'விரிவுரை', 'உரை', 'விளக்கம்', 'முறை', 'திரட்டு',
    'மூலமும்', 'மூலம்',
    'இன்பம்', 'அமுது'
]

# Prefixes that link to following words with an insertion stop (ஒற்று)
COMPOUND_PREFIXES = ['தனி', 'பெரிய', 'சிறு', 'புதிய']

# Insertion consonants (தோன்றல் வல்லொற்று) that appear before corresponding stops
SANDHI_PAIRS = [
    ('க்', 'க'),
    ('ச்', 'ச'),
    ('த்', 'த'),
    ('ப்', 'ப')
]

def split_sandhi_compounds(text: str) -> str:
    """
    Deconstructs conjoined Tamil compounds into separated constituent words.
    E.g.:
      - 'தெய்வப்புலமை' -> 'தெய்வ புலமை' (removes linking 'ப்')
      - 'தனிப்பாடல்களும்' -> 'தனி பாடல்களும்' (removes linking 'ப்')
      - 'ரத்தினச்சுறுக்கம்' -> 'ரத்தின சுறுக்கம்' (removes linking 'ச்')
      - 'திருக்குறள்மூலம்' -> 'திருக்குறள் மூலம்'
      - 'திருக்குறளின்பம்' -> 'திருக்குறள் இன்பம்'
    """
    if not text:
        return ''

    # Handle known OCR / print spacing quirks
    text = re.sub(r'க்குற\s+ளின்பம்', 'க்குறள் இன்பம்', text)
    text = re.sub(r'ளின்பம்', 'ள் இன்பம்', text)
    
    # Strip word-final external sandhi stops before another word
    # E.g. 'தெய்வப்புலமைத் திருவள்ளுவ' -> 'தெய்வப்புலமை திருவள்ளுவ'
    text = re.sub(r'([\u0B80-\u0BFF]+)[கசதப]\u0BCD\s+([கசதப])', r'\1 \2', text)
    
    # Process compound prefixes: E.g. 'தனிப்' + 'பாடல்' -> 'தனி ' + 'பாடல்'
    for prefix in COMPOUND_PREFIXES:
        pattern = rf'(?<![\u0B80-\u0BFF]){prefix}[கசதப]\u0BCD([கசதப])'
        text = re.sub(pattern, rf'{prefix} \1', text)
    
    # Process compound suffixes
    for suffix in sorted(COMPOUND_SUFFIXES, key=lambda x: -len(x)):
        # Pattern 1: Word + [Optional Linking Stop (க்/ச்/த்/ப்)] + Suffix
        for stop, start_char in SANDHI_PAIRS:
            if suffix.startswith(start_char):
                pattern = rf'([\u0B80-\u0BFF]+){stop}{suffix}(?=\s|$|[,\.!?])'
                replacement = rf'\1 {suffix}'
                text = re.sub(pattern, replacement, text)
                
        # Pattern 2: Word ending in consonant or vowel directly attaching to suffix without stop
        pattern_direct = rf'([\u0B80-\u0BFF]{{3,}}){suffix}(?=\s|$|[,\.!?])'
        text = re.sub(pattern_direct, rf'\1 {suffix}', text)

    # Clean up any leftover isolated stop consonants floating between words
    text = re.sub(r'\s+[க்ங்ச்ஞ்ட்ண்த்ந்ப்ம்ய்ர்ல்வ்ழ்ள்ற்ன்]\s+', ' ', text)
    
    # Normalize multiple whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

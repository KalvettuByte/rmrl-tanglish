"""
Tamil Allophonic Voicing & Phonotactics Engine.
Applies authentic, spoken Tamil rules (Intervocalic voicing, Homorganic nasal clusters,
Gemination preservation, and Grantha phonology).
"""

import re
from .utils import split_tamil_letters, UYIR, VOWEL_SIGNS, MEI_BASES

STOPS = {'க', 'ச', 'ட', 'த', 'ப', 'ற'}
NASALS = {'ங', 'ஞ', 'ண', 'ந', 'ம', 'ன'}

def transliterate_token(token: str) -> str:
    """
    Transliterates a single Tamil token/word applying allophonic voicing.
    """
    if not token:
        return ''
        
    if token.isascii():
        return token
        
    letters = split_tamil_letters(token)
    n = len(letters)
    out = []
    
    for i, char in enumerate(letters):
        # 0. Non-Tamil characters (spaces, punctuation, digits, ASCII)
        if char == 'ஸ்ரீ':
            out.append('Sri ')
            continue
            
        if not ('\u0B80' <= char[0] <= '\u0BFF'):
            out.append(char)
            continue
            
        # 1. Pure Independent Vowels (அ, ஆ, etc.)
        if char in UYIR:
            out.append(UYIR[char])
            continue
            
        # 2. Aytham (ஃ)
        if char == 'ஃ':
            out.append('h')
            continue
            
        # 3. Pure Consonants with Pulli (க், ச், த், etc.)
        if len(char) == 2 and char[1] == '\u0BCD':
            base = char[0]
            next_char = letters[i+1] if i + 1 < n else ''
            
            # Nasals before corresponding stops:
            if base in NASALS:
                if base == 'ங':
                    out.append('ng')
                elif base == 'ம':
                    out.append('m')
                else:
                    out.append('n')
                continue
                
            # Geminate stops: க்+க -> k, ச்+ச -> ch, ட்+ட -> t, த்+த -> t, ப்+ப -> p
            if base == 'க' and next_char.startswith('க'):
                out.append('k')
            elif base == 'ச' and next_char.startswith('ச'):
                out.append('ch')
            elif base == 'ட' and next_char.startswith('ட'):
                out.append('t')
            elif base == 'த' and next_char.startswith('த'):
                out.append('t')
            elif base == 'ப' and next_char.startswith('ப'):
                out.append('p')
            elif base == 'ற' and next_char.startswith('ற'):
                out.append('tt')
            else:
                mei_map = {
                    'க': 'k', 'ங': 'ng', 'ச': 's', 'ஞ': 'gn', 'ட': 't', 'ண': 'n',
                    'த': 'th', 'ந': 'n', 'ப': 'p', 'ம': 'm', 'ய': 'y', 'ர': 'r',
                    'ல': 'l', 'வ': 'v', 'ழ': 'zh', 'ள': 'l', 'ற': 'r', 'ன': 'n',
                    'ஜ': 'j', 'ஷ': 'sh', 'ஸ': 's', 'ஹ': 'h', 'க்ஷ': 'ksh'
                }
                out.append(mei_map.get(base, base))
            continue
            
        # 4. Syllabic Consonants (உயிர்மெய் - க, கா, கி, or inherent 'a')
        base_cons = char[0]
        vowel_part = char[1:] if len(char) > 1 else ''
        vowel_latin = VOWEL_SIGNS.get(vowel_part, 'a')
        
        prev_is_vowel = (i > 0 and (letters[i-1] in UYIR or (len(letters[i-1]) == 1 and letters[i-1] in MEI_BASES) or (len(letters[i-1]) == 2 and letters[i-1][1] in VOWEL_SIGNS)))
        prev_is_nasal_pulli = (i > 0 and len(letters[i-1]) == 2 and letters[i-1][1] == '\u0BCD' and letters[i-1][0] in NASALS)
        prev_is_stop_pulli = (i > 0 and len(letters[i-1]) == 2 and letters[i-1][1] == '\u0BCD' and letters[i-1][0] in STOPS)
        
        cons_latin = MEI_BASES.get(base_cons, base_cons)
        
        # Rule A: Velar /k/ (க)
        if base_cons == 'க':
            if prev_is_nasal_pulli:
                cons_latin = 'g'  # ங் + க -> ngg / ng + ga -> nga
            elif prev_is_stop_pulli:
                cons_latin = 'k'  # க் + க -> kk
            elif prev_is_vowel:
                cons_latin = 'g'  # Intervocalic: Agathiyar, Murugan
            else:
                cons_latin = 'k'  # Word-initial: Kural, Kambar
                
        # Rule B: Palatal /c/ (ச)
        elif base_cons == 'ச':
            if prev_is_nasal_pulli:
                cons_latin = 'j'  # ஞ் + ச -> nja / nja
            elif prev_is_stop_pulli:
                cons_latin = 'ch' # ச் + ச -> cch / ch
            elif prev_is_vowel:
                cons_latin = 's'  # Intervocalic: Kasu, Vasagam
            else:
                cons_latin = 's'  # Word-initial: Siddhar, Sol
                
        # Rule C: Retroflex /ṭ/ (ட)
        elif base_cons == 'ட':
            if prev_is_nasal_pulli:
                cons_latin = 'd'  # ண் + ட -> nd
            elif prev_is_stop_pulli:
                cons_latin = 't'  # ட் + ட -> tt
            elif prev_is_vowel:
                cons_latin = 'd'  # Intervocalic: Nadu, Padam
            else:
                cons_latin = 'd'
                
        # Rule D: Dental /t/ (த)
        elif base_cons == 'த':
            if prev_is_nasal_pulli:
                cons_latin = 'dh' # ந் + த -> ndha
            elif prev_is_stop_pulli:
                cons_latin = 'th' # த் + த -> tth
            elif i == 0 and vowel_latin in ['e', 'ai']:
                cons_latin = 'd'  # Word-initial Deivam, Desam
            elif prev_is_vowel:
                cons_latin = 'dh' # Intervocalic: Madham, Vidhai
            else:
                cons_latin = 'th' # Word-initial: Thiruvalluvar, Thamizh
                
        # Rule E: Bilabial /p/ (ப)
        elif base_cons == 'ப':
            if prev_is_nasal_pulli:
                cons_latin = 'b'  # ம் + ப -> mb
            elif prev_is_stop_pulli:
                cons_latin = 'p'  # ப் + ப -> pp
            elif prev_is_vowel:
                cons_latin = 'b'  # Intervocalic: Abayam, Subam
            else:
                cons_latin = 'p'  # Word-initial: Paattu, Pudhu
                
        # Rule F: Alveolar /ṟ/ (ற)
        elif base_cons == 'ற':
            if prev_is_stop_pulli and letters[i-1][0] == 'ற':
                cons_latin = 'r'  # ற் + ற -> ttr
            else:
                cons_latin = 'r'
                
        out.append(cons_latin + vowel_latin)
        
    result = ''.join(out)
    
    # Post-processing smoothing for natural English aesthetics
    result = re.sub(r'thth', 'th', result)
    result = re.sub(r'tth', 'th', result)
    result = re.sub(r'chch', 'ch', result)
    result = re.sub(r'cch', 'ch', result)
    result = re.sub(r'kg', 'kk', result)
    result = re.sub(r'ttr', 'tt', result)
    result = re.sub(r'zhzh', 'zh', result)
    
    return result

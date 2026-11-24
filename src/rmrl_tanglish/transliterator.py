"""
Main Modern Tanglish Transliterator Interface.
"""

import re
from .lexicon import COMMON_LEXICON
from .sandhi import split_sandhi_compounds
from .phonology import transliterate_token
from .utils import is_tamil

class ModernTanglish:
    def __init__(self, custom_lexicon: dict[str, str] | None = None):
        """
        Initializes the Modern Tanglish transliterator with default
        classical/modern lexicon, plus any optional custom dictionary overrides.
        """
        self.lexicon = dict(COMMON_LEXICON)
        if custom_lexicon:
            self.lexicon.update(custom_lexicon)
            
        # Pre-sort lexicon keys by descending length for greedy matching
        self._sorted_lex_keys = sorted(self.lexicon.keys(), key=lambda x: -len(x))

    def transliterate(self, text: str, capitalize_words: bool = True) -> str:
        """
        Converts Tamil text to clean, natural, search-optimized Modern Tanglish.
        
        Args:
            text: Input string in Tamil script (can include English, numbers, punctuation).
            capitalize_words: If True, capitalizes words into Title Case.
            
        Returns:
            Natural Tanglish string.
        """
        if not text:
            return ''
            
        if not is_tamil(text):
            return text
            
        # Step 1: Pre-process Sandhi compounds (unlinking conjoined words)
        text = split_sandhi_compounds(text)
        
        # Step 2: Apply high-frequency Lexicon replacements with boundary awareness
        for key in self._sorted_lex_keys:
            val = self.lexicon[key]
            # Match whole-token boundary (not embedded inside longer Tamil words)
            pattern = rf'(?<![\u0B80-\u0BFF]){re.escape(key)}(?![\u0B80-\u0BFF])'
            text = re.sub(pattern, f' {val} ', text)
                
        # Step 3: Split into tokens (whitespace delimited)
        tokens = [t for t in text.split() if t]
        
        # Step 4: Transliterate remaining Tamil tokens via allophonic phonology
        output_tokens = []
        for tok in tokens:
            # If the token was already matched by the lexicon or is ASCII, preserve it
            if tok.isascii():
                output_tokens.append(tok)
            else:
                out = transliterate_token(tok)
                output_tokens.append(out)
                
        # Step 5: Capitalization & Formatting
        if capitalize_words:
            formatted_tokens = []
            for tok in output_tokens:
                if tok.isascii() and tok.isalpha():
                    formatted_tokens.append(tok.capitalize())
                elif tok.isupper():
                    formatted_tokens.append(tok)
                else:
                    formatted_tokens.append(tok)
            res = ' '.join(formatted_tokens)
        else:
            res = ' '.join(output_tokens)
            
        # Clean up punctuation spacing
        res = re.sub(r'\s+([,.:;?!])', r'\1', res)
        res = re.sub(r'\s+', ' ', res).strip()
        return res

# Default singleton instance
_default_instance = ModernTanglish()

def to_tanglish(text: str, capitalize_words: bool = True) -> str:
    """
    Convenience function: Converts Tamil text to natural Modern Tanglish.
    """
    return _default_instance.transliterate(text, capitalize_words=capitalize_words)

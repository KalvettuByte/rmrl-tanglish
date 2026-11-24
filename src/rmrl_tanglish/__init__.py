"""
rmrl-tanglish: High-fidelity, Sandhi-aware phonetic Tanglish transliterator
specialized for the Roja Muthiah Research Library (RMRL) digital collection.
"""

from .transliterator import ModernTanglish as RMRLTanglish, to_tanglish

__version__ = "0.1.0"
__all__ = ["RMRLTanglish", "to_tanglish"]

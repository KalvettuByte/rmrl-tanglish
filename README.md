# rmrl-tanglish

**Sandhi-aware, phonetic Tanglish transliterator built specifically for the Roja Muthiah Research Library (RMRL) digital preservation collection.**

---

The Problem with Standard Tamil Transliteration:

Standard Python transliterators (`open-tamil`, `aksharamukha`, `tamil-toolkit`, `indic-transliteration`) follow strict orthographic or academic rules (like ISO-15919 or keyboard mappings). 

When applied to 18th–20th century classical Tamil literature and Siddha medical treatises, they produce robotic, unreadable output:

| Tamil Original | Academic / Generic Tool Output ❌ | `rmrl-tanglish` Output ✅ |
| :--- | :--- | :--- |
| **தெய்வப்புலமைத் திருவள்ளுவநாயனார்... தமிழ்வேதமாகிய திருக்குறள்மூலம்** | `Theyvappulamaith Thiruvalluvanaayanaar... Thamizhvethamaagiya Thirukkuralmoolam` | **`Deiva Pulamai Thiruvalluva Nayanar Thiruvaaimalarndhu Aruliya Thamizh Vedhamaagiya Thirukkural Moolam`** |
| **மகாபாரதம்** | `Makaapaaratham` / `makāpāratam` | **`Mahabharatham`** |
| **அகஸ்தியமுனிவர்... வயித்தியரத்தினச்சுறுக்கம் 360** | `...Vayithiyarathinachsurukkam 360` | **`Agasthiya Munivar... Vaithiya Rathina Churukkam 360`** |
| **மதிறாஸ் தூக்குப்பாட்டு** | `Mathiraas Thookkuppaattu` | **`Madras Thookku Paattu`** |
| **சுவாமி சுத்தானந்த பாரதியார்** | `Suvaami Suthtaanantha Paarathiyaar` | **`Swamy Suthanandha Bharathiyar`** |

### Why?
1. **Sandhi (புணர்ச்சி) Blindness:** Classical printers conjoined words with stop consonants (`தெய்வப் + புலமை` = `தெய்வப்புலமை`). Generic libraries fail to segment compounds.
2. **Positional Allophony:** Tamil uses `க` for both *k* and *g*, and `த` for *th* and *d*. Generic tools lack phonetic context, generating unnatural forms like *Makaapaaratham* instead of *Mahabharatham*.
3. **No Cultural / Archival Lexicon:** Medical terms (*Vaithiya*, *Navaneetham*, *Siddha*) and historical places (*Madras*, *Kandanur*) get mangled.

---

## Features

- **Sandhi Disassembler (புணர்ச்சி பிரிப்பான்):** Automatically unlinks compound titles and removes joining stops (`க், ச், த், ப்`).
- **Allophonic Voicing Engine:** Accurately voices intervocalic stops and homorganic nasal clusters (`ங்க` $\rightarrow$ `ng`, `ஞ்ச` $\rightarrow$ `nj`, `ண்ட` $\rightarrow$ `nd`, `ந்த` $\rightarrow$ `ndh`, `ம்ப` $\rightarrow$ `mb`).
- **RMRL Archival Lexicon:** Built-in recognition for classical literature, Sangam commentary, Shaiva/Vaishnava texts, and 19th-century palm-leaf prints.
- **Zero External Dependencies:** Pure Python 3, fast and self-contained (processes 14,000+ book titles in under 4 seconds).

---

## Quickstart

```python
from rmrl_tanglish import to_tanglish

title = "அகஸ்தியமுனிவர் திருவாய்மலர்ந்தருளிய வயித்தியரத்தினச்சுறுக்கம் 360"
print(to_tanglish(title))
# Output: Agasthiya Munivar Thiruvaaimalarndhu Aruliya Vaithiya Rathina Churukkam 360

epic = "மகாபாரதம்"
print(to_tanglish(epic))
# Output: Mahabharatham
```

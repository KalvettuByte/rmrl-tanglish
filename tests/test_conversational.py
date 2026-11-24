import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from modern_tanglish import to_tanglish

def test_conversational():
    cases = [
        ("வணக்கம்", "Vanakkam"),
        ("ரொம்ப நன்றி", "Romba Nandri"),
        ("தம்பி", "Thambi"),
        ("எப்படி இருக்கிறீர்கள்?", "Eppadi Irukkireergal?"),
        ("சென்னை", "Chennai"),
        ("மழை பெய்கிறது", "Mazhai Peygiradhu"),
        ("அன்பு", "Anbu"),
        ("காதல்", "Kaadhal"),
        ("வெற்றி", "Vetri")
    ]
    
    passed = 0
    for tamil_in, expected in cases:
        out = to_tanglish(tamil_in)
        print(f"In : {tamil_in} -> Out: {out}")
        assert out == expected, f"\nFAILED:\nExpected: '{expected}'\nGot     : '{out}'"
        passed += 1
        
    print(f"\nAll {passed}/{len(cases)} conversational tests PASSED!")

if __name__ == '__main__':
    test_conversational()

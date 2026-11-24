import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from modern_tanglish import to_tanglish

def test_classical_titles():
    cases = [
        (
            "தெய்வப்புலமைத் திருவள்ளுவநாயனார் திருவாய்மலர்ந்தருளிய தமிழ்வேதமாகிய திருக்குறள்மூலம்",
            "Deiva Pulamai Thiruvalluva Nayanar Thiruvaaimalarndhu Aruliya Thamizh Vedhamaagiya Thirukkural Moolam"
        ),
        (
            "அகஸ்தியமுனிவர் திருவாய்மலர்ந்தருளிய வயித்தியரத்தினச்சுறுக்கம் 360",
            "Agasthiya Munivar Thiruvaaimalarndhu Aruliya Vaithiya Rathina Churukkam 360"
        ),
        (
            "மகாபாரதம்",
            "Mahabharatham"
        ),
        (
            "மதிறாஸ் தூக்குப்பாட்டு",
            "Madras Thookku Paattu"
        ),
        (
            "வள்ளுவர் வகுத்த வழி",
            "Valluvar Vagutha Vazhi"
        ),
        (
            "சுவாமி சுத்தானந்த பாரதியார் இயற்றிய திருக்குறளின்பம்",
            "Swamy Suthanandha Bharathiyar Iyatriya Thirukkural Inbam"
        ),
        (
            "திருக்குறள் உரை வேற்றுமை",
            "Thirukkural Urai Vetrumai"
        ),
        (
            "வைத்தியத் திருப்புகழும் வைத்தியத் தனிப்பாடல்களும்",
            "Vaithiya Thiruppugazhum Vaithiya Thani Paadalkalum"
        ),
        (
            "அநுபோக வைத்திய நவநீதம்",
            "Anuboga Vaithiya Navaneetham"
        ),
        (
            "குறள் அமுது",
            "Kural Amudhu"
        )
    ]
    
    passed = 0
    for tamil_in, expected in cases:
        out = to_tanglish(tamil_in)
        print(f"In : {tamil_in}")
        print(f"Out: {out}")
        assert out == expected, f"\nFAILED:\nExpected: '{expected}'\nGot     : '{out}'"
        passed += 1
        print("  -> PASSED [OK]\n")
        
    print(f"All {passed}/{len(cases)} classical title tests PASSED 100%!")

if __name__ == '__main__':
    test_classical_titles()

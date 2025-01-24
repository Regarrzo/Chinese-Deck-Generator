def convert_to_unicode_tone_marks(string):
    tone_marks = {
        'a': ['ā', 'á', 'ǎ', 'à', 'a'],
        'e': ['ē', 'é', 'ě', 'è', 'e'],
        'i': ['ī', 'í', 'ǐ', 'ì', 'i'],
        'o': ['ō', 'ó', 'ǒ', 'ò', 'o'],
        'u': ['ū', 'ú', 'ǔ', 'ù', 'u'],
        'ü': ['ǖ', 'ǘ', 'ǚ', 'ǜ', 'ü'],
        'v': ['ǖ', 'ǘ', 'ǚ', 'ǜ', 'ü']
    }

    def find_vowel_to_change(syllable):
        vowels = 'aeiouüv'
        if 'a' in syllable:
            return 'a'
        elif 'e' in syllable:
            return 'e'
        elif 'ou' in syllable:
            return 'o'
        for v in vowels:
            if v in syllable:
                return v
        return None

    result = []
    tokens = string.split()
    for token in tokens:
        tone = 4
        new_token = token
        for char in token:
            if char.isdigit():
                tone = int(char) - 1
                new_token = new_token.replace(char, '')
                break
        
        vowel = find_vowel_to_change(new_token)
        if vowel:
            new_token = new_token.replace(vowel, tone_marks[vowel][tone])
        result.append(new_token)
    
    return ' '.join(result)


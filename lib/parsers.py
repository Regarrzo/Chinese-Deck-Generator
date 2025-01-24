def parse_dict(path):
    #A parser for the CC-Cedict. Convert the Chinese-English dictionary into a list of python dictionaries with "traditional","simplified", "pinyin", and "english" keys.
    #Make sure that the cedict_ts.u8 file is in the same folder as this file, and that the name matches the file name on line 13.
    #Before starting, open the CEDICT text file and delete the copyright information at the top. Otherwise the program will try to parse it and you will get an error message.
    #Characters that are commonly used as surnames have two entries in CC-CEDICT. This program will remove the surname entry if there is another entry for the character. If you want to include the surnames, simply delete lines 59 and 60.
    #This code was written by Franki Allegra in February 2020.

    #open CEDICT file

    # Modified by Regarrzo
    list_of_dicts = []

    with open(path, encoding="utf8") as file:
        text = file.read()
        lines = text.split('\n')
        dict_lines = list(lines)

        def parse_line(line):
            parsed = {}
            if line == '':
                dict_lines.remove(line)
                return 0
            line = line.rstrip('/')
            line = line.split('/')
            if len(line) <= 1:
                return 0
            english = " / ".join(line[1:]) # Regarrzo: I fixed an error here that would only take the first definition of a word
            char_and_pinyin = line[0].split('[')
            characters = char_and_pinyin[0]
            characters = characters.split()
            traditional = characters[0]
            simplified = characters[1]
            pinyin = char_and_pinyin[1]
            pinyin = pinyin.rstrip()
            pinyin = pinyin.rstrip("]")
            parsed['traditional'] = traditional
            parsed['simplified'] = simplified
            parsed['pinyin'] = pinyin
            parsed['english'] = english

            list_of_dicts.append(parsed)

        #make each line into a dictionary
        for line in dict_lines:
            if not line.startswith('#'):
                parse_line(line)
        
        return list_of_dicts

def to_hanzi_to_info(dictionary):
    hanzi_to_info = {}
    for entry in dictionary:
        if entry['simplified'] not in hanzi_to_info:
            hanzi_to_info[entry['simplified']] = [entry]
        else:
            hanzi_to_info[entry['simplified']].append(entry)

    return hanzi_to_info

def parse_wordlist(path="words.txt"):
    with open(path, "r", encoding="utf8") as file:
        words = file.read().split("\n")
        words = [word.split("（")[0] for word in words]
        words = [word.split("｜")[0] for word in words]
        words = [word.strip() for word in words if word]
    return words

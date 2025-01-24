import csv
import lib.parsers as parsers
import lib.pinyin as pinyin

# I made this file to edit the after creation after discovering a bug in the dictparser provided by MDBG. 
# Export the deck to CSV, then you can use this script to perform various edits. Right now it just overwrites the pinyin and definition fields
# with the correct values from the dictionary.

dictionary = parsers.parse_dict()
hanzi_to_info = parsers.to_hanzi_to_info(dictionary)

def process_csv(filename):
    modified_rows = []
    
    with open(filename, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter='\t')

        for row in reader:
            # if row is comment, skip
            if row[0].startswith("#"):
                modified_rows.append(row)
                continue

            word = row[0].split("(")[0].strip()
            
            if word not in hanzi_to_info:
                modified_rows.append(row)
                continue

            infos = hanzi_to_info[word]

            pinyins = [pinyin.convert_to_unicode_tone_marks(info['pinyin']) for info in infos]
            pinyin_field = '<br>'.join(pinyins)

            definitions = [info['english'] for info in infos]
            definition_field = '<br>'.join(definitions)

            pinyin_and_definition_field = '<br>'.join([f"{pinyin}: {definition}" for pinyin, definition in zip(pinyins, definitions)])
            modified_rows.append([row[0], pinyin_field, definition_field, pinyin_and_definition_field] + [row[4]])

    
    # Optional: Write modified data to new file
    with open('modified.csv', 'w', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in modified_rows:
            writer.writerow(row)

process_csv('FrequencyChinese.txt')


import genanki
import lib.parsers as parsers
import lib.llm_generation as llm_generation
import lib.pinyin as pinyin

def make_card(word):
    try:
        infos = hanzi_to_info[word]
        if infos[0]['simplified'] != infos[0]['traditional']:
            word_field = f"{infos[0]['simplified']} ({infos[0]['traditional']})"
        else:
            word_field = infos[0]['simplified']

        pinyins = [pinyin.convert_to_unicode_tone_marks(info['pinyin']) for info in infos]
        pinyin_field = '<br>'.join(pinyins)

        definitions = [info['english'] for info in infos]
        definition_field = '<br>'.join(definitions)
        

        pinyin_and_definition_field = '<br>'.join([f"{pinyin}: {definition}" for pinyin, definition in zip(pinyins, definitions)])
    except KeyError:
        # use llm to get the pinyin and definition
        definition_and_pinyin, definitions, pinyin_ = llm_generation.llm_definition_and_pinyin(word)
        traditional = llm_generation.llm_get_traditional_version(word)
        word_field = f"{word} ({traditional})"
        pinyin_field = pinyin_
        definition_field = definitions
        pinyin_and_definition_field = definition_and_pinyin

    example_sentences = llm_generation.llm_make_example_sentences(word, n=3)
    sentences_field = str(example_sentences)

    return genanki.Note(model=my_model, fields=[word_field, pinyin_field, definition_field, pinyin_and_definition_field, sentences_field])

def init_model_and_deck():
    my_model = genanki.Model(
    1822956412,
    'Chinese Card',
    fields=[
        {'name': 'Hanzi'},
        {'name': 'Pinyin'},
        {'name': 'Definition'},
        {'name': 'Pinyin and Definition'},
        {'name': 'Example Sentences'},
    ],
    templates=[
        {
        'name': 'Hanzi to Definition card',
        'qfmt': '{{Hanzi}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Pinyin and Definition}}<br><br>{{Example Sentences}}',
        },
    ])

    my_deck = genanki.Deck(1261185309, "Chinese")
    return my_model, my_deck

if __name__ == "__main__":
    dictionary = parsers.parse_dict("cedict_ts.u8")
    hanzi_to_info = parsers.to_hanzi_to_info(dictionary)
    words = parsers.parse_wordlist("twfrequency.txt")

    my_model, my_deck = init_model_and_deck()
    
    for idx, word in enumerate(words):
        print(f"Processing word {word} ({idx + 1}/{len(words)})")
        my_deck.add_note(make_card(word))

        if idx % 100 == 0:
            genanki.Package(my_deck).write_to_file(f'output{idx}.apkg')
                                                
    genanki.Package(my_deck).write_to_file(f'FINAL_output{idx}.apkg')
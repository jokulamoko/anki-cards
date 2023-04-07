from anki import Deck

kanji_deck_name = 'Kanji (Heisig)'

deck = Deck(deck_name=kanji_deck_name)
deck.n_notes

# test that adding notes is fine
# note = deck.notes[0]
# note.duplicate_note(kanji_deck_name, additional_params={'allowDuplicate':True})

# make changes to the cards
from tqdm import tqdm

def emphasise_keyword(note):
    before = note.fields['English']['value']
    words = before.split(', ')
    if len(words) > 1 and '<br>' not in before:
        keyword = "<b>"+ words[0] + "</b><br><br>"
        updated = keyword + ', '.join(words[1:])
        note.fields['English']['value'] = updated

for note in tqdm(deck.notes):
    emphasise_keyword(note)
    note.update_note()


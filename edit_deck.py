import pandas as pd
import os
from pathlib import Path

from anki.deck import Deck

DECK_NAME = 'Japanese Vocab'
MODEL_NAME = 'Vocabulary'
KEY_NAME = 'translation'
NOTE_FIELDS = ['translation', 'english notes', '日本語', 'hirigana', 'japanese notes', 'sentence']

# load excel file and deck
data_dir = Path(os.getcwd()) / 'data'
df_notes = pd.read_excel(data_dir / 'Japanese Vocab.xlsx')
deck = Deck(DECK_NAME, MODEL_NAME)

# first compare the cards by the key 'translation'
# deck_unmatched_cards, excel_unmatched_cards = deck.compare_to_df(df_notes, KEY_NAME)

# then edit notes
updated_notes, missing_notes = deck.update_notes_with_df(df_notes, KEY_NAME, NOTE_FIELDS)



25 - 1 - 0.3 - 0.8 - 1

5.4 - 0.8

6.1 + 5.4 - 8.2 + 0.7 * 52/12

5.9 - (0.4 + 0.5 + 0.3/4) * 4.33

(0.4 + 0.5 + 0.3/4) * 4.33

1.7 * 20
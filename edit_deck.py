import pandas as pd
import os
from pathlib import Path

from anki.deck import Deck
from anki.styling import AddLineBreaks
from settings import DECK_NAME, MODEL_NAME, KEY_NAME, NOTE_FIELDS

# load excel file and deck
data_dir = Path(os.getcwd()) / 'data'
df_notes = pd.read_excel(data_dir / 'Japanese Vocab.xlsx')
deck = Deck(DECK_NAME, MODEL_NAME)

# first compare the cards by the key 'translation'
deck_unmatched_cards, excel_unmatched_cards = deck.compare_to_df(df_notes, KEY_NAME)

# then edit notes
styling = [AddLineBreaks]
updated_notes, missing_notes = deck.update_notes_with_df(df_notes, KEY_NAME, NOTE_FIELDS, styles=styling)




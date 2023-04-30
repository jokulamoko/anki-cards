from anki import Deck, Note
import pandas as pd
import os
from pathlib import Path


DECK_NAME = 'Japanese Vocab'
MODEL_NAME = 'Vocabulary'
KEY_NAME = 'translation'
NOTE_FIELDS = ['translation', 'english notes', '日本語', 'hirigana', 'japanese notes', 'sentence']

deck = Deck(deck_name=DECK_NAME, model_name='Vocabulary')
print(f'Notes in {DECK_NAME}: {deck.n_notes}')

# load excel file of data
data_dir = Path(os.getcwd()) / 'data'
df_notes = pd.read_excel(data_dir / 'Japanese Vocab.xlsx')
df_new = df_notes[df_notes.uploaded!=1].reset_index(drop=True).fillna('')
print(f'{len(df_new)} new cards!')



###################

# add to deck
result, errors = deck.add_notes_to_deck_from_df(df_new, NOTE_FIELDS)

# for the successful cards, mark 'uploaded' and save result
df_new['uploaded'] = [int(x is not None) for x in result]
notes_cols = list(df_notes.columns)
notes_cols.remove('uploaded')
df_result = df_notes.drop(columns=['uploaded']).fillna('').merge(df_new, on=notes_cols, how='outer')
df_result['uploaded'].fillna(1, inplace=True)
df_result.to_excel(data_dir / 'Japanese Vocab.xlsx', index=False)


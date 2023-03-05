from anki import Deck, Note, invoke
import pandas as pd
import os
from pathlib import Path

deck_name = 'Japanese Vocab'

deck = Deck(deck_name=deck_name, model_name='Vocabulary')
print(f'Notes in {deck_name}: {deck.n_notes}')

# load excel file of data
data_dir = Path(os.getcwd()) / 'data'
df_notes = pd.read_excel(data_dir / 'Japanese Vocab.xlsx')
note_fields = list(df_notes.columns)
note_fields.remove('uploaded')
df_new = df_notes[df_notes.uploaded!=1].reset_index(drop=True).fillna('')
print(f'{len(df_new)} new cards!')

# define notes
new_notes = []
for i in range(len(df_new)):
    note_serial = df_new[note_fields].loc[i, :].to_dict()
    new_note = Note(note_serial)
    new_notes.append(new_note)

result, errors = deck.add_to_anki(new_notes)

errors

# for the successful cards, mark 'uploaded'
error_notes = [Note(error) for error in errors]
succes_notes = set(new_notes) - set(error_notes)
len(succes_notes)
len(new_notes)

# UPDATE speak on telephone
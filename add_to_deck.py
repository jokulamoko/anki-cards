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

# add to deck
result, errors = deck.add_to_anki(new_notes)


# for the successful cards, mark 'uploaded' and save result
df_new['uploaded'] = [int(x is not None) for x in result]
notes_cols = list(df_notes.columns)
notes_cols.remove('uploaded')
df_result = df_notes.drop(columns=['uploaded']).fillna('').merge(df_new, on=notes_cols, how='outer')
df_result['uploaded'].fillna(1, inplace=True)
df_result.to_excel(data_dir / 'Japanese Vocab.xlsx', index=False)

from .requests import invoke
from .note import Note
from .styling import Style

from typing import List, Optional
import pandas as pd
from tqdm import tqdm

class Deck:
    def __init__(self, deck_name, model_name, notes=None):
        self.deck_name = deck_name
        self.model_name = model_name
        self.new_deck = True
 
        if notes:
            self.n_notes = len(notes)
            self.notes = notes
        else:
            self.note_ids = invoke('findNotes', **{'query':f'deck:"{self.deck_name}"'})
            self.n_notes = len(self.note_ids)
            note_infos = invoke('notesInfo', **{'notes':self.note_ids})
            self.notes = [Note(note_info, new=False) for note_info in note_infos]
            self.new_deck = False

            # get model
            if len(self.notes) > 0:
                self.model_name = self.notes[0].dict['modelName']
            model_fields = invoke(action='modelFieldNames', modelName=self.model_name)
            model_fields.sort()
            self.model_fields = model_fields

    def __str__(self):
        return f"{self.deck_name}, {self.n_notes} notes"

    def add_notes_to_deck(self, note_list:List[Note], styles:Optional[List[Style]] = None):
        if self.new_deck:
            raise Exception('This is not an existing deck.\nCreating a new deck is not implemented')
        else:
            # # verifying model adherence
            # print('Verifying model adherence...')
            # for note in tqdm(note_list):
            #     note._verify_model_adherence(self.model_fields)
            # print('Done!\n')
            
            # then addNotes
            print('Adding notes...')
            # TODO add styles
            notes = [note._export_format(add_values={'modelName':self.model_name, 'deckName':self.deck_name}) for note in note_list]            
            result = invoke('addNotes', notes=notes)
            print('Done!')

            # verify result
            successful_uploads = [True if note_result else False for note_result in result]
            errors = [note for i, note in enumerate(note_list) if not successful_uploads[i]]
            print(f'{sum([int(x) for x in successful_uploads])} from {len(notes)} notes successfully uploaded!') 

            return result, errors

    def add_notes_to_deck_from_df(self, df_notes: pd.DataFrame, note_fields):
        new_notes = []
        for i in range(len(df_notes)):
            note_serial = df_notes[note_fields].loc[i, :].to_dict()
            new_note = Note(note_serial)
            new_notes.append(new_note)

        # add to deck
        result, errors = self.add_notes_to_deck(new_notes)
        return result, errors

    def compare_to_df(self, df_notes:pd.DataFrame, key_name:str, verbose=True):
        """
        Compares the notes in an excel file to those in the deck by a particular key.
        Useful check before editing notes using an excel file.
        """
        excel_note_keys = set(df_notes[key_name])
        deck_unmatched_cards = []
        excel_unmatched_cards = []

        # compare the deck against excel notes
        for note in self.notes:
            note_key = note.dict['fields'][key_name]['value']
            if note_key not in excel_note_keys:
                deck_unmatched_cards.append(note_key)

        # compare excel notes against the deck
        deck_note_keys = set([note.dict['fields'][key_name]['value'] for note in self.notes])
        for note_key in df_notes[key_name]:
            if note_key not in deck_note_keys:
                excel_unmatched_cards.append(note_key)

        if verbose:
            print(deck_unmatched_cards)
            print(excel_unmatched_cards)

        return deck_unmatched_cards, excel_unmatched_cards
    
    def update_notes_with_df(
            self, 
            df_notes:pd.DataFrame, 
            key_name:str, 
            note_fields:List[str], 
            styles:Optional[List[Style]] = None
            ):
        print(f'First building index of note by key {key_name}')
        note_keys = [note.dict['fields'][key_name]['value'] for note in self.notes]

        print('Updating notes...')
        missing_notes = []
        updated_notes = []
        for i in tqdm(range(len(df_notes))):
            try:
                note_idx = note_keys.index(df_notes.loc[i, key_name])
            except ValueError:
                missing_notes.append(note_idx)
                continue

            note = self.notes[note_idx]
            for field in note_fields:
                field_value = df_notes.loc[i, field]
                if type(field_value) is str:
                    note.dict['fields'][field]['value'] = field_value
            if styles:
                for style in styles:
                    style.apply_styling(note)
            note_update_result = note.update_note()
            updated_notes.append(note_update_result)

        print(f'{len(updated_notes)} notes updated!')
        print(f'Missing {len(missing_notes)} that are in df_notes, but not in the deck.')
        return updated_notes, missing_notes
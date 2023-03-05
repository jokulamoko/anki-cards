from .requests import invoke
from .note import Note
from tqdm import tqdm
from typing import List

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

    def add_to_anki(self, note_list:List[Note]):
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
            notes = [note._export_format(add_values={'modelName':self.model_name, 'deckName':self.deck_name}) for note in note_list]
            result = invoke('addNotes', notes=notes)
            print('Done!')

            # verify result
            successful_uploads = [True if note_result else False for note_result in result]
            errors = [note for note in note_list if not successful_uploads[i]]
            print(f'{sum([int(x) for x in successful_uploads])} from {len(notes)} notes successfully uploaded!') 

            return result, errors

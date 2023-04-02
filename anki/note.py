from .requests import invoke
from math import isnan

class Note:
    def __init__(self, note_info, new=True, **kwargs):
        if new:
            note_fields = list(note_info.keys())
            for key in note_fields:
                note_info[key] = note_info[key].replace('\n', '<br>')

            # transform into standard API response format for anki
            note_info = {'fields':{field:{'value':note_info[field]} for field in note_fields if note_info[field]}}

        self.dict = note_info
    
    def __repr__(self):
        note_id = self.dict['noteId'] if 'noteId' in self.dict.keys() else 'NEW CARD'
        return f"{note_id}, {self.dict['fields']}"

    def __str__(self):
        note_id = self.dict['noteId'] if 'noteId' in self.dict.keys() else 'NEW CARD'
        return f"{note_id}, {self.dict['fields']}"

    def _verify_model_adherence(self, model_fields):
        note_fields = list(self.dict['fields'])
        note_fields.sort()
        assert note_fields == model_fields, f"Expected {model_fields}, got {note_fields} for {self}"

    def _loop_over_dict(self, current_field):
        if type(current_field) is dict:
            keys = current_field.keys()
            if 'value' in keys:
                return current_field['value']
            else:
                return {k:self._loop_over_dict(current_field[k]) for k in keys}
        else:
            return current_field

    def _export_format(self, skip_keys:set={'noteId', 'cards'}, add_values={}):
        result = {core_attr:self._loop_over_dict(self.dict[core_attr]) 
                for core_attr in self.dict.keys() 
                if core_attr not in skip_keys
            }
        result.update(add_values)
        return result

    def duplicate_note(self, deck_name, skip_keys={'noteId', 'cards'}, additional_params={}):
        params = {
            'note': self._export_format(skip_keys)
        }
        params['note']['deckName'] = deck_name
        if additional_params:        
            params['note']['options'] = additional_params
        result = invoke('addNote', **params)
        return result

    def update_note(self):
        params =  {'note' : self._export_format()}
        params['note']['id'] = self.noteId
        result = invoke('updateNoteFields', **params)
        return result
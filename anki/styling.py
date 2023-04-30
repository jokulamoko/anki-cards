from abc import ABC, abstractclassmethod

class Style(ABC):        

    @abstractclassmethod
    def apply_styling(note):
        pass


class AddLineBreaks(Style):

    @abstractclassmethod
    def apply_styling(self, note):
        fields_applied = ['japanese notes', 'sentence']
        for field in fields_applied:
            note.dict['fields'][field]['value'] = note.dict['fields'][field]['value'].replace('|', '<br>')



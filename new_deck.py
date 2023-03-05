from anki import *

# first check models
query = {
    'action' : 'modelNamesAndIds'
}
models = invoke(**query)

# details of most appropriate model
model_name = 'Vocabulary'
query = {
    'action' : 'modelFieldNames',
    'modelName' : model_name
}
fields = invoke(**query)
# probably best off creating models in Anki, then accessing them via this app


# add a create note function
    # handles some annoying structure processing
    # asserts the note model conforms

# add to deck add-note functionality

# load from excel lines into note objects

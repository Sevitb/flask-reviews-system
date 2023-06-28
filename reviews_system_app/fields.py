from wtforms import Field, RadioField, StringField
from wtforms.widgets import ListWidget, RadioInput, TextInput 

class RadioPlusField(RadioField):
    widget = ListWidget(prefix_label=False)
    option_widget = RadioInput()

    def __init__(self, label='', validators=None, remove_duplicates=True, **kwargs):
        super(RadioPlusField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []
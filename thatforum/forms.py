from django import forms


class ThatForumBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ThatForumBaseForm, self).__init__(*args, **kwargs)
        for fn, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

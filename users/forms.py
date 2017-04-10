from django import forms

from users.models import Task


class ContactForm(forms.ModelForm):
    id = forms.IntegerField(required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['description'].widget.attrs = {
            'class': 'form-control'
        }

        self.fields['id'].widget = forms.HiddenInput()

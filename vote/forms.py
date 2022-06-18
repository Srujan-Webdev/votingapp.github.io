from django import forms
from .models import Polls_Create


class Polls_CreateForm(forms.ModelForm):

    poll_name = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add Poll here....!','rows':3}), label='Poll Question')
    option_one = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Option 1'}), label='Option 1')
    option_two = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Option 2'}), label='Option 2')
    option_three = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Option 3'}), label='Option 3')

    class Meta:						
        model = Polls_Create
        fields = ['poll_name','option_one','option_two','option_three']		


class Polls_UpdateForm(forms.ModelForm):

    poll_name = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add Poll here....!','rows':3}), label='Poll Question')
    option_one = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Option 1'}), label='Option 1')
    option_two = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Option 2'}), label='Option 2')
    option_three = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Option 3'}), label='Option 3')

    class Meta:						
        model = Polls_Create
        fields = ['poll_name','option_one','option_two','option_three']	
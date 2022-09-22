from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}), max_length=24)
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}), max_length=24)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your Email'}), max_length=56)
    comment = forms.CharField(label="Comment:", widget=forms.Textarea())

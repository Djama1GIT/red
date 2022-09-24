from django import forms


class AddToCartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'] = forms.ChoiceField(widget=forms.RadioSelect(), choices=args[1])


class EmailPostForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}), max_length=48)
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}), max_length=48)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your Email'}), max_length=56)
    comment = forms.CharField(widget=forms.Textarea())


class SignUpForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Login'}), max_length=48)
    mail = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}), max_length=56)
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Phone number'}),
                               min_value=1000000000, max_value=9999999999)
    passwd = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
                             min_length=8, max_length=48)
    repeat_passwd = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
                                    min_length=8, max_length=48)

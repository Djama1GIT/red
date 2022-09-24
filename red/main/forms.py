from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}), max_length=48)
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}), max_length=48)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your Email'}), max_length=56)
    comment = forms.CharField(widget=forms.Textarea())


class LogInForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Login'}), max_length=48)
    passwd = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Password'}), max_length=48)


class SignUpForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Login'}), max_length=48)
    mail = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}), max_length=56)
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Phone number'}))
    passwd = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}), max_length=48)
    repeat_passwd = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
                                    max_length=48)

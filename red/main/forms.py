from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as user
from django.urls import reverse_lazy

from .models import User
from .utils import ValidateMixin


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


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(), max_length=48)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=48)
    country = forms.CharField(widget=forms.TextInput(), max_length=48)
    address = forms.CharField(widget=forms.TextInput(), max_length=48)
    postcode = forms.CharField(widget=forms.TextInput(), max_length=48)
    city = forms.CharField(widget=forms.TextInput(), max_length=48)
    province = forms.CharField(widget=forms.TextInput(), max_length=48)


class SettingsForm(ValidateMixin, forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    mail = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}), max_length=56,
                            required=False)
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Phone number'}),
                               min_value=1000000000, max_value=9999999999, required=False)
    old = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter old password'}),
                          min_length=8, max_length=48, required=False)
    passwd = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
                             min_length=8, max_length=48, required=False)
    repeat_passwd = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
                                    min_length=8, max_length=48, required=False)

    def is_valid(self):
        if self.data.get('mail') and \
                self.data.get('mail') != user.objects.filter(username=self.request.user.username)[0].email:
            user.objects.filter(username=self.request.user.username).update(email=self.data.get('mail'))

        if self.data.get('phone') and \
                self.data.get('phone') != int(User.objects.filter(user=self.request.user.id)[0].phone):
            User.objects.filter(user=self.request.user.id).update(phone=self.data.get('phone'))

        if self.data.get('old'):
            if authenticate(self.request, username=self.request.user.username, password=self.data.get('old')):
                if self.check_password(self.data.get('passwd'), self.data.get('repeat_passwd'),
                                       self.request.user.username):
                    _user = user.objects.get(username=self.request.user.username)
                    _user.set_password(str(self.data.get('passwd')).strip())
                    _user.save()
                else:
                    self.add_error('passwd', 'Invalid new password')
            else:
                self.add_error('old', 'Incorrect password')
        return super().is_valid()


class UploadImageForm(forms.Form):
    image = forms.ImageField()

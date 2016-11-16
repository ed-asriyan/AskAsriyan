from django import forms


class BootstrapTextInput(forms.TextInput):
    def __init__(self, attrs={}, *args, **kwargs):
        attrs = {**attrs,
                 'class': 'form-control'}
        forms.TextInput.__init__(self, attrs=attrs)


class BootstrapPasswordInput(BootstrapTextInput):
    def __init__(self, attrs={}, *args, **kwargs):
        attrs = {**attrs,
                 'type': 'password'}
        BootstrapTextInput.__init__(self, attrs=attrs)


class SignInForm(forms.Form):
    user_name = forms.CharField(max_length=20, label='Login', widget=BootstrapTextInput)
    password = forms.CharField(label='Password', widget=BootstrapPasswordInput)

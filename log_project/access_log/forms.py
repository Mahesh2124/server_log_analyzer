from django import forms

class ServerLoginForm(forms.Form):
    ip_address = forms.GenericIPAddressField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    port = forms.IntegerField()

class Server(forms.Form):
    my_checkbox = forms.BooleanField(label='Archived files',required=False)
    server_name=forms.CharField(max_length=25)

class DateForm(forms.Form):
    from_date = forms.DateField(label='FROM DATE(please enter YYYY-MM-DD in this format)')
    to_date = forms.DateField(label='TO DATE')
    
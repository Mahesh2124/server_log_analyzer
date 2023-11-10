from django import forms

class ServerLoginForm(forms.Form):
    server_choices = [('apache', 'Apache'), ('nginx', 'Nginx'),('httpd','Httpd')]
    ip_address = forms.GenericIPAddressField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    port = forms.IntegerField()
    server = forms.ChoiceField(
        choices=server_choices,
        widget=forms.RadioSelect,
    )

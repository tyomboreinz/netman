from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from ipam.models import *

class FormIpAddress(ModelForm):
    class Meta:
        model = Ip_address
        fields = '__all__'
        list_choices = (
            ('Mikrotik', 'Mikrotik'),
            ('Ubuntu Server 20.04', 'Ubuntu Server 20.04'),
            ('Ubuntu Desktop', 'Ubuntu Desktop'),
            ('Windows 8', 'Windows 8'),
            ('Windows 10', 'Windows 10'), )

        widgets = {
            'ip_address': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'hostname': forms.TextInput({'class':'form-control ps-0 form-control-line'}),
            'description': forms.TextInput({'class':'form-control ps-0 form-control-line'}),
            'subnet': forms.Select({'class':'form-control'}),
            'os': forms.Select(choices=list_choices,attrs={'class':'form-control'}),
            'username': forms.TextInput({'class':'form-control'}),
            'password': forms.PasswordInput({'class':'form-control','data-toggle':'password'}),
        }

class FormSubnet(ModelForm):
    class Meta:
        model = Subnet
        fields = '__all__'

        widgets = {
            'netmask': forms.NumberInput({'class':'form-control ps-0 form-control-line'}),
            'ip_network': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'ip_broadcast': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'description': forms.TextInput({'class':'form-control ps-0 form-control-line'}),
        }

class FormDHCP(ModelForm):
    class Meta:
        model = Dhcp_Config
        fields = ['value']

        widgets = {
            'config': forms.TextInput({'class':'form-control'}),
            'value': forms.TextInput({'class':'form-control'}),
        }

class FormDHCP_Static(ModelForm):
    class Meta:
        model = Dhcp_static
        fields = '__all__'

        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
            'mac': forms.TextInput({'class':'form-control'}),
            'ip': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'description': forms.TextInput({'class':'form-control ps-0 form-control-line'}),
        }

class FormApplication(ModelForm):
    class Meta:
        model = Application
        fields = '__all__'

        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
            'port': forms.TextInput({'class':'form-control'}),
            'ip': forms.Select({'class':'form-control'}),
            'description': forms.TextInput({'class':'form-control'}),
        }

class FormConfigs(ModelForm):
    class Meta:
        model = ConfigPortal
        fields = ['value']
        widgets = {
            'value' : forms.TextInput({'class':'form-control'})
        }

class FormOS(ModelForm):
    class Meta:
        model = OS
        fields = '__all__'

        widgets = {
            'name': forms.TextInput({'class':'form-control', 'placeholder':'Press Enter to add OS'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username Here ...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password Here ...'}))
from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from ipam.models import *
from ipam.network import Network

class FormIpAddress(ModelForm):
    class Meta:
        model = Ip_address
        fields = '__all__'

        widgets = {
            'ip_address': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'hostname': forms.TextInput({'class':'form-control'}),
            'description': forms.TextInput({'class':'form-control'}),
            'subnet': forms.Select({'class':'form-control'}),
            'os': forms.Select({'class':'form-control'}),
            'username': forms.TextInput({'class':'form-control'}),
            'password': forms.TextInput({'class':'form-control','data-toggle':'password'}),
        }

class FormSubnet(ModelForm):
    class Meta:
        model = Subnet
        fields = '__all__'

        netmask = ()
        for i in range(16, 31):
            net = (str(i), str(i))
            netmask += (net,)

        labels = {
            'ip_network' : "IP "
        }

        widgets = {
            'netmask': forms.Select(choices=netmask,attrs={'class':'form-control'}),
            'ip_network': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'ip_broadcast': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'description': forms.TextInput({'class':'form-control'}),
        }

class FormDHCP(ModelForm):
    class Meta:
        model = Dhcp_Config
        fields = '__all__'

        netmask = ()
        for i in range(16, 31):
            net = (str(i), str(i))
            netmask += (net,)

        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
            'network': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'netmask': forms.Select(choices=netmask,attrs={'class':'form-control'}),
            'broadcast': forms.HiddenInput(),
            'ip_start': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'ip_end': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'gateway': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'dns1': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'dns2': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'interface': forms.Select({'class':'form-control'})
        }

class FormDHCP_Static(ModelForm):
    class Meta:
        model = Dhcp_static
        fields = '__all__'

        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
            'mac': forms.TextInput({'class':'form-control'}),
            'ip': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'description': forms.TextInput({'class':'form-control'}),
        }

class FormApplication(ModelForm):
    class Meta:
        model = Application
        fields = '__all__'
        list_choices = (
            ('http', 'http'),
            ('https', 'https'), )

        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
            'protocol': forms.Select(choices=list_choices,attrs={'class':'form-control'}),
            'port': forms.TextInput({'class':'form-control'}),
            'ip': forms.Select({'class':'form-control'}),
            'domain': forms.Select({'class':'form-control'}),
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

class FormDomain(ModelForm):
    class Meta:
        model = Domain
        fields = '__all__'

        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
            'ip': forms.Select({'class':'form-control'}),
            'description': forms.TextInput({'class':'form-control'}),
        }

class FormSubDomain(ModelForm):
    class Meta:
        model = SubDomain
        fields = '__all__'
        # list_choices = (
        #     ('A', 'A'),)

        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
            # 'type': forms.Select(choices=list_choices,attrs={'class':'form-control'}),
            'type' : forms.HiddenInput(),
            'root_domain': forms.Select({'class':'form-control'}),
            'ip': forms.Select({'class':'form-control'}),
            'description': forms.TextInput({'class':'form-control'}),
        }
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username Here ...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password Here ...'}))
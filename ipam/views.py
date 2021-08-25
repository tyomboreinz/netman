from ipam.network import Network
from django.shortcuts import render, redirect
from django.db.models.functions import Length
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ipam.models import *
from ipam.forms import *
import datetime, random

@login_required(login_url=settings.LOGIN_URL)
def os_delete(request, id_os):
    os = OS.objects.get(id=id_os)
    os.delete()
    return redirect('/setting')

@login_required(login_url=settings.LOGIN_URL)
def setting_os(request):
    if request.POST:
        form = FormOS(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/setting')
    else:
        form = FormOS()
        data = {
            'menu_config' : 'class=mm-active',
            'form' : form,
            'os_data' : OS.objects.all().order_by('name'),
            'configs' : ConfigPortal.objects.all().order_by('config'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            }
    return render(request, 'setting.html', data)

@login_required(login_url=settings.LOGIN_URL)
def config_edit(request, id_config):
    set = ConfigPortal.objects.get(id=id_config)
    if request.POST:
        form = FormConfigs(request.POST, instance=set)
        if form.is_valid():
            form.save()
            return redirect('/config/portal')
    else:
        form = FormConfigs(instance=set)
        data = {
            'form' : form,
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def application_delete(request, id_app):
    app = Application.objects.get(id=id_app)
    if app.image:
        app.image.delete()
    app.delete()
    return redirect('applications')

@login_required(login_url=settings.LOGIN_URL)
def application_edit(request, id_app):
    app = Application.objects.get(id=id_app)
    if request.POST:
        post_value = request.FILES.copy()
        if post_value:
            app.image.delete()
        form = FormApplication(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            return redirect('applications')
    else:
        form = FormApplication(instance=app)
        data = {
            'form' : form,
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def application_add(request):
    if request.POST:
        form = FormApplication(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('applications')
    else:
        form = FormApplication()
        data = {
            'form' : form,
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def applications(request):
    data = {
        'app_list' : Application.objects.all(),
        'menu_app' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'applications.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_lease(request):
    data = {
        'dhcp_lease': Network.get_dhcp_lease(),
        'menu_dhcp_lease' : 'class=mm-active',
        'menu_dhcp_client' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'dhcp-lease.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_static_edit(request,id_static):
    dhcp = Dhcp_static.objects.get(id=id_static)
    if request.POST:
        form = FormDHCP_Static(request.POST, instance=dhcp)
        if form.is_valid():
            form.save()
            return redirect('/dhcp/static')
    else:
        form = FormDHCP_Static(instance=dhcp)
        data = {
            'form' : form,
            'dhcp' : dhcp,
            'title' : 'Edit Static DHCP',
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_static_delete(request, id_static):
    dhcp = Dhcp_static.objects.get(id=id_static)
    dhcp.delete()
    return redirect('/dhcp/static')

@login_required(login_url=settings.LOGIN_URL)
def dhcp_static_add(request):
    if request.POST:
        form = FormDHCP_Static(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dhcp/static')
    else:
        form = FormDHCP_Static()
        data = {
            'form' : form,
            'title' : 'Add DHCP',
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_static_lease(request):

    dhcp_static = Dhcp_static.objects.all().order_by(Length('ip').asc(), 'ip')
    data = {
        'dhcp_static': dhcp_static,
        'menu_dhcp_lease' : 'class=mm-active',
        'menu_dhcp_static' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'dhcp-static-lease.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_config_apply(request):
    default_lease_time = Dhcp_Config.objects.get(config="default_lease_time")
    max_lease_time = Dhcp_Config.objects.get(config="max_lease_time")
    subnet = Dhcp_Config.objects.get(config="subnet")
    netmask = Dhcp_Config.objects.get(config="netmask")
    dhcp_start = Dhcp_Config.objects.get(config="dhcp_start")
    dhcp_end = Dhcp_Config.objects.get(config="dhcp_end")
    gateway = Dhcp_Config.objects.get(config="gateway")
    dns1 = Dhcp_Config.objects.get(config="dns1")
    dns2 = Dhcp_Config.objects.get(config="dns2")
    domain = Dhcp_Config.objects.get(config="domain")
    interface = Dhcp_Config.objects.get(config="interface")
    static_leases = Dhcp_static.objects.all().order_by(Length('ip').asc(), 'ip')

    Network.dhcp_config(default_lease_time.value, max_lease_time.value, subnet.value, netmask.value, dhcp_start.value, dhcp_end.value, gateway.value, dns1.value, dns2.value, domain.value, interface.value, static_leases)

    return redirect('/')

@login_required(login_url=settings.LOGIN_URL)
def dhcp_config_edit(request,id_setting):
    dhcp = Dhcp_Config.objects.get(id=id_setting)
    if request.POST:
        form = FormDHCP(request.POST, instance=dhcp)
        if form.is_valid():
            form.save()
            return redirect('/dhcp/config')
    else:
        form = FormDHCP(instance=dhcp)
        data = {
            'form' : form,
            'dhcp' : dhcp,
            'title' : 'Edit Config DHCP - '+ dhcp.config,
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_config_list(request):
    dhcp_config = Dhcp_Config.objects.all()
    data = {
        'dhcp_config' : dhcp_config,
        'menu_dhcp' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'dhcp-config.html', data)

@login_required(login_url=settings.LOGIN_URL)
def ip_delete(request, id_ip):
    ip = Ip_address.objects.get(id=id_ip)
    ip.delete()
    return redirect('/network/' + str(ip.subnet_id))

@login_required(login_url=settings.LOGIN_URL)
def ip_edit(request, id_ip):
    ip = Ip_address.objects.get(id=id_ip)
    if request.POST:
        form = FormIpAddress(request.POST, instance=ip)
        if form.is_valid():
            subnet = Subnet.objects.get(ip_network=form.cleaned_data['subnet'])
            form.save()
            return redirect('/network/' + str(subnet.id))
    else:
        form = FormIpAddress(instance=ip)
        #form.fields['subnet'].widget = forms.HiddenInput()
        #form.fields['subnet'].widget.attrs['disabled'] = True
        form.fields['subnet'].widget.attrs['readonly'] = True
        #form.fields['subnet'].disabled = True
        data = {
            'form' : form,
            'ip' : ip,
            'title' : 'Edit IP Address',
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def ip_add(request):
    if request.POST:
        form = FormIpAddress(request.POST)
        if form.is_valid():
            subnet = Subnet.objects.get(ip_network=form.cleaned_data['subnet'])
            form.save()
            return redirect('/network/' + str(subnet.id))
    else:
        form = FormIpAddress()
        data = {
            'form' : form,
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'title' : 'Add IP',
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_delete(request, id_subnet):
    subnet = Subnet.objects.get(id=id_subnet)
    subnet.delete()
    return redirect('/network/')

@login_required(login_url=settings.LOGIN_URL)
def network_edit(request, id_subnet):
    subnet = Subnet.objects.get(id=id_subnet)
    if request.POST:
        form = FormSubnet(request.POST, instance=subnet)
        if form.is_valid():
            form.save()
            return redirect('/network')
    else:
        form = FormSubnet(instance=subnet)
        data = {
            'form' : form,
            'subnet' : subnet,
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'title' : 'Edit Network',
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_detail(request, id_subnet):
    ips = Ip_address.objects.filter(subnet=id_subnet).order_by(Length('ip_address').asc(), 'ip_address')
    data = {
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        'id_subnet' : id_subnet,
        'ips' : ips,
        'menu_network_detail' : 'class=mm-active',
        'menu_network_' : 'class=mm-active',
    }
    return render(request, 'network-detail.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_add(request):
    if request.POST:
        form = FormSubnet(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/network/')
    else:
        form = FormSubnet()
        data = {
            'form' : form,
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'title' : 'Add Network',
            'menu_network_aria' : 'mm-collapse mm-show',
            'menu_network_add' : 'class=mm-active',
            'menu_network' : 'class=mm-active',
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_list(request):
    subnets = Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network')
    data = {
        'subnets' : subnets,
        'sidebar_subnets' : subnets,
        'menu_network_aria' : 'mm-collapse mm-show',
        'menu_network_list' : 'class=mm-active',
        'menu_network' : 'class=mm-active',
    }
    return render(request, 'network-list.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_scan(request, id_subnet):
    subnet = Subnet.objects.get(id=id_subnet)
    existing_ip = Ip_address.objects.filter(subnet=id_subnet)
    lists_ip = Network.network_scan(subnet.ip_network +"/"+ subnet.netmask)

    for ip in lists_ip:
        token = 0
        for address in existing_ip:
            if ip == address.ip_address:
                token += 1

        if token == 0:    
            Ip_address.objects.create(ip_address=str(ip),subnet_id=id_subnet)
            print("IP : "+ ip +" Addedd Successfully")
        else:
            print("IP : "+ ip +" Already Available")
        
    return redirect('/network/'+ str(id_subnet))

@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    os = OS.objects.all().order_by('name')
    total_ip = Ip_address.objects.all().count()
    total_subnet = Subnet.objects.all().count()
    color = ['primary', 'success', 'warning', 'danger']
    data_os = []
    for data in os:
        count_data = Ip_address.objects.filter(os_id=data.id).count()
        if count_data != 0:
            data_os.append({'name' : data.name, 'count' : count_data, 'percentage' : format(count_data / total_ip * 100, ".0f"), 'color' : random.choice(color)})

    data = {
        'total_subnet' : total_subnet,
        'total_ip' : total_ip,
        'data_os' : data_os,
        'menu_dashboard' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'dashboard.html', data)

def home(request):
    now = datetime.datetime.now()
    data = {
        'company_name' : ConfigPortal.objects.get(config='company_name'),
        'company_short_name' : ConfigPortal.objects.get(config='company_short_name'),
        'company_address' : ConfigPortal.objects.get(config='company_address'),
        'company_telp' : ConfigPortal.objects.get(config='company_telp'),
        'company_email' : ConfigPortal.objects.get(config='company_email'),
        'company_website' : ConfigPortal.objects.get(config='company_website'),
        'app_name' : ConfigPortal.objects.get(config='app_name'),
        'app_list' : Application.objects.all(),
        'year' : now.year
    }
    return render(request, 'portal.html', data)
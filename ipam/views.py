from django.db.models.aggregates import Count
from django.db.models.functions.text import Upper
from ipam.network import Network
from django.shortcuts import render, redirect
from django.db.models.functions import Length
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ipam.models import *
from ipam.forms import *
import datetime, random, ipcalc

@login_required(login_url=settings.LOGIN_URL)
def subdomain_apply(request, id_domain):
    domain = Domain.objects.get(id=id_domain)
    subdomain = SubDomain.objects.filter(root_domain=id_domain)
    Network.dns_file_config(domain.id, domain.name, domain.ip, subdomain)
    return redirect('/domain/'+ str(id_domain))

@login_required(login_url=settings.LOGIN_URL)
def subdomain_delete(request, id_subdomain):
    subdomain = SubDomain.objects.get(id=id_subdomain)
    subdomain.delete()
    return redirect('/domain/'+ str(subdomain.root_domain_id))

@login_required(login_url=settings.LOGIN_URL)
def subdomain_edit(request, id_subdomain):
    subdomain = SubDomain.objects.get(id=id_subdomain)
    if request.POST:
        form = FormSubDomain(request.POST, instance=subdomain)
        if form.is_valid():
            domain = Domain.objects.get(name=form.cleaned_data['root_domain'])
            form.save()
            return redirect('/domain/'+str(domain.id))
    else:
        form = FormSubDomain(instance=subdomain)
        data = {
            'form' : form,
            'title' : 'Edit Subdomain',
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def subdomain_add(request):
    if request.POST:
        form = FormSubDomain(request.POST)
        if form.is_valid():
            domain = Domain.objects.get(name=form.cleaned_data['root_domain'])
            form.save()
            return redirect('/domain/'+str(domain.id))
    else:
        form = FormSubDomain()
        data = {
            'form' : form,
            'title' : 'Add SubDomain',
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def subdomain(request, id_subdomain):
    data = {
        'menu_subdomain' : 'class=mm-active',
        'menu_domain_' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        'sidebar_domains' : Domain.objects.all().order_by('name'),
        'subdomain_list' : SubDomain.objects.filter(root_domain=id_subdomain),
        'domain' : Domain.objects.get(id=id_subdomain),
        'id_subdomain' : id_subdomain,
    }
    return render(request, 'subdomain.html', data)

@login_required(login_url=settings.LOGIN_URL)
def domain_delete(request, id_domain):
    domain = Domain.objects.get(id=id_domain)
    Network.dns_delete(domain.name)
    domain.delete()
    return redirect('/domain')

@login_required(login_url=settings.LOGIN_URL)
def domain_edit(request, id_domain):
    domain = Domain.objects.get(id=id_domain)
    if request.POST:
        form = FormDomain(request.POST, instance=domain)
        if form.is_valid():
            form.save()
            return redirect('/domain')
    else:
        form = FormDomain(instance=domain)
        data = {
            'form' : form,
            'title' : 'Edit Domain',
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def domain_add(request):
    domain = Domain.objects.all().order_by('name')
    if request.POST:
        form = FormDomain(request.POST)
        if form.is_valid():
            form.save()
            Network.dns_config(domain)
            return redirect('/domain')
        else:
            return redirect('/domain')
    else:
        form = FormDomain()
        data = {
            'form' : form,
            'title' : 'Add Domain',
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : domain,
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def domain_list(request):
    domain = Domain.objects.all().order_by('name')
    data = {
        'menu_domain' : 'class=mm-active',
        'domain_list' : domain,
        'sidebar_domains' : domain,
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'domain.html', data)

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
            'sidebar_domains' : Domain.objects.all().order_by('name'),
            }
    return render(request, 'setting.html', data)

@login_required(login_url=settings.LOGIN_URL)
def config_edit(request, id_config):
    set = ConfigPortal.objects.get(id=id_config)
    if request.POST:
        form = FormConfigs(request.POST, instance=set)
        if form.is_valid():
            form.save()
            return redirect('/setting')
    else:
        form = FormConfigs(instance=set)
        data = {
            'form' : form,
            'title' : 'Edit Config Portal - ' + str(set.config).upper(),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
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
            'title' : 'Edit App',
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
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
            'title' : 'Add App',
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def applications(request):
    data = {
        'app_list' : Application.objects.all(),
        'menu_app' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        'sidebar_domains' : Domain.objects.all().order_by('name'),
    }
    return render(request, 'applications.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_lease(request):
    data = {
        'dhcp_lease': Network.get_dhcp_lease(),
        'menu_dhcp_lease' : 'class=mm-active',
        'menu_dhcp_client' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        'sidebar_domains' : Domain.objects.all().order_by('name'),
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
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
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
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
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
        'sidebar_domains' : Domain.objects.all().order_by('name'),
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
        if dhcp.config == "interface":
            form.fields['value'].widget = forms.Select(choices=Network.get_interface_list(),attrs={'class':'form-control'})
            
        data = {
            'form' : form,
            'dhcp' : dhcp,
            'title' : 'Edit Config DHCP - '+ dhcp.config,
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_config_list(request):
    dhcp_config = Dhcp_Config.objects.all()
    data = {
        'dhcp_config' : dhcp_config,
        'menu_dhcp' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        'sidebar_domains' : Domain.objects.all().order_by('name'),
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
        # form.fields['subnet'].widget = forms.TextInput({'class':'form-control'})
        # form.fields['subnet'].widget = forms.HiddenInput()
        # form.fields['subnet'].disabled = True
        data = {
            'form' : form,
            'ip' : ip,
            'title' : 'Edit IP Address',
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
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
            'sidebar_domains' : Domain.objects.all().order_by('name'),
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
        post_value = request.POST.copy()
        subnet_calc = ipcalc.Network(str(post_value['ip_network']+'/'+str(post_value['netmask'])))
        post_value['ip_network'] = str(subnet_calc.network())
        post_value['ip_broadcast'] = str(subnet_calc.broadcast())
        form = FormSubnet(post_value, instance=subnet)
        if form.is_valid():
            form.save()
            return redirect('/network')
    else:
        form = FormSubnet(instance=subnet)
        data = {
            'form' : form,
            'subnet' : subnet,
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
            'title' : 'Edit Network',
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_detail(request, id_subnet):
    ips = Ip_address.objects.filter(subnet=id_subnet).order_by(Length('ip_address').asc(), 'ip_address')
    data = {
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        'sidebar_domains' : Domain.objects.all().order_by('name'),
        'id_subnet' : id_subnet,
        'ips' : ips,
        'menu_network_detail' : 'class=mm-active',
        'menu_network_' : 'class=mm-active',
    }
    return render(request, 'network-detail.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_add(request):
    if request.POST:
        post_value = request.POST.copy()
        subnet = ipcalc.Network(str(post_value['ip_network']+'/'+str(post_value['netmask'])))
        post_value['ip_network'] = str(subnet.network())
        post_value['ip_broadcast'] = str(subnet.broadcast())
        form = FormSubnet(post_value)
        if form.is_valid():
            form.save()
            return redirect('/network/')
    else:
        form = FormSubnet()
        form.fields['ip_broadcast'].widget = forms.HiddenInput()
        data = {
            'form' : form,
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'sidebar_domains' : Domain.objects.all().order_by('name'),
            'title' : 'Add Network',
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_list(request):
    subnets = Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network')
    data = {
        'subnets' : subnets,
        'sidebar_subnets' : subnets,
        'sidebar_domains' : Domain.objects.all().order_by('name'),
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
    os = OS.objects.all().annotate(count_os=Count('ip_address')).order_by('-count_os')
    total_ip = Ip_address.objects.all().count()
    color_list = ['#007bff', '#6610f2', '#6f42c1', '#e83e8c', '#dc3545', '#fd7e14', '#ffc107', '#28a745', '#20c997', '#17a2b8', '#6c757d', '#3f6ad8', '#6c757d', '#3ac47d', '#16aaff', '#f7b924', '#d92550', '#eee', '#343a40', '#444054', '#794c8a']
    data_os = []
    for data in os:
        count_data = Ip_address.objects.filter(os_id=data.id).count()
        if count_data != 0:
            # data_os.append({'name' : data.name, 'count' : count_data, 'percentage' : format(count_data / total_ip * 100, ".0f"), 'color' : random.choice(color)})
            data_os.append({'name' : data.name, 'count' : count_data})
    
    color = random.sample(color_list, len(data_os))
    for i in range(len(data_os)):
        data_os[i]['color'] = color[i]

    data = {
        'total_subnet' : Subnet.objects.all().count(),
        'total_ip' : total_ip,
        'total_domain' : Domain.objects.all().count(),
        'total_subdomain' : SubDomain.objects.all().count(),
        'total_app' : Application.objects.all().count(),
        'total_dhcp_lease' : len(Network.get_dhcp_lease()),
        'data_os' : data_os,
        'menu_dashboard' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        'sidebar_domains' : Domain.objects.all().order_by('name'),
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
        'app_name' : ConfigPortal.objects.get(config='portal_name'),
        'app_list' : Application.objects.all(),
        'year' : now.year
    }
    return render(request, 'portal.html', data)
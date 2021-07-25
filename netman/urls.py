"""netman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from django.contrib.auth import views
from django.contrib.auth.views import LoginView, LogoutView
from ipam.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', home, name='home'),
    
    path('dhcp/config', dhcp_config_list, name='dhcp_config_list'),
    path('dhcp/config/<int:id_setting>', dhcp_config_edit, name='dhcp_config_edit'),
    path('dhcp/config/apply', dhcp_config_apply, name='dhcp_config_apply'),
    path('dhcp/lease/', dhcp_lease, name='dhcp_lease'),
    path('dhcp/static/', dhcp_static_lease, name='dhcp_static_lease'),
    path('dhcp/static/add', dhcp_static_add, name='dhcp_static_add'),
    path('dhcp/static/edit/<int:id_static>', dhcp_static_edit, name='dhcp_static_edit'),
    path('dhcp/static/delete/<int:id_static>', dhcp_static_delete, name='dhcp_static_delete'),

    path('network/', network_list, name='network_list'),
    path('network/add', network_add, name='network_add'),
    path('network/edit/<int:id_subnet>', network_edit, name='network_edit'),
    path('network/scan/<int:id_subnet>', network_scan , name='network_scan'),
    path('network/<int:id_subnet>', network_detail, name='detail_network'),
    path('network/delete/<int:id_subnet>', network_delete , name='network_delete'),

    path('ipaddress/add/', ip_add, name='ip_add'),
    path('ipaddress/delete/<int:id_ip>', ip_delete, name='ip_delete'),
    path('ipaddress/edit/<int:id_ip>', ip_edit, name='ip_edit'),
]
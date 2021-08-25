from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from ipam.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard', dashboard, name='dashboard'),
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

    path('applications', applications, name='applications'),
    path('application/add', application_add, name='app_add'),
    path('application/edit/<int:id_app>', application_edit, name='app_edit'),
    path('application/delete/<int:id_app>', application_delete, name='app_delete'),

    path('config/portal/edit/<int:id_config>', config_edit, name='config_edit'),

    path('setting/', setting_os, name='setting'),
    path('os/delete/<int:id_os>', os_delete, name='os_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
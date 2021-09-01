import subprocess, os

class Network():

    def get_interface_dhcp(interface_db):
        x = subprocess.check_output("ifconfig | grep UP | grep -v br | grep -v docker | grep -v lo | awk '{print $1}' | tr -d ':'", shell=True)
        x_decode = x.decode("utf-8")
        interface_list = list(filter(None,(x_decode.split("\n"))))
        interface = ()
        for iface in interface_list:
            token = 0

            for ifacedb in interface_db:
                if iface == ifacedb['interface']:
                    token += 1
            
            if token == 0:
                ether = (iface, iface)
                interface += (ether,)
        return interface

    def get_dhcp_lease():
        x = subprocess.check_output("dhcp-lease-list | sed -n '/=======/,$p' | grep -v '=========' | awk '{print $0}'", shell=True)
        x_decode = x.decode("utf-8")
        lists_dhcp = list(filter(None,(x_decode.split("\n"))))
        dhcp_lease = []
        for line in lists_dhcp:
            value = []
            for word in line.split():
                value.append(word)

            dhcp_lease.append({'mac':value[0], 'ip':value[1], 'hostname':value[2], 'avaiable':value[4]+" "+value[3], 'manufacturer':value[5]})

        return dhcp_lease

    def network_scan(subnet):
        x = subprocess.check_output("nmap -sn "+ subnet +""" | grep report | awk '{print $NF}' | sed 's/(//g' | sed 's/)//g' """, shell=True, text=False)
        x_decode = x.decode("utf-8")
        lists_ip = list(filter(None,(x_decode.split("\n"))))
        return lists_ip

    # def dhcp_config(default_lease_time, max_lease_time, subnet, netmask, dhcp_start, dhcp_end, gateway, dns1, dns2, domain, interface, static_leases):
    def dhcp_config(dhcp_config, static_leases):
        config = ''
        interface = ''
        config_interface = ''

        if dhcp_config.count() != 0:
            config += "default-lease-time 600;\nmax-lease-time 7200;\nauthoritative;\n\n"

            for dhcp in dhcp_config:
                interface += dhcp.interface+" "

                config += "subnet "+ dhcp.network +" netmask "+ dhcp.netmask +"  {\n"
                config += "\trange "+ dhcp.ip_start +" "+ dhcp.ip_end +";\n"
                config += "\toption routers "+ dhcp.gateway +";\n"
                config += "\toption broadcast-address "+ dhcp.broadcast +";\n"
                config += "\toption domain-name-servers "+ dhcp.dns1 +", "+ dhcp.dns2 +";\n"
                config += "\toption domain-name \"coba.com\";\n\n"
            
            config += "}\n\n#static_lease\n\n"

            for static in static_leases:
                config += "host "+ str(static.name) +"{\n"
                config += "\thardware ethernet "+ str(static.mac) +";\n"
                config +=  "\tfixed-address "+ str(static.ip) +";\n}\n"

            config_interface = "INTERFACESv4=\""+ interface +"\""

        print(config)
        print(config_interface)
        # file_config = open(r"/etc/dhcp/dhcpd.conf","w+")
        # file_config.truncate(0)
        # file_config.writelines(config)
        # file_config.close()

        # file_config = open(r"/etc/default/isc-dhcp-server.conf","w+")
        # file_config.truncate(0)
        # file_config.writelines(config_interface)
        # file_config.close()

        # x = subprocess.check_output("/etc/init.d/isc-dhcp-server restart", shell=True, text=False)
        # sed -e '/host/,/^/d' | sed -e '/hardware/,/^/d' | sed -e '/fixed/,/^/d' #delete line contain word

        return ''

    def dns_default_config(id, domain, ip):
        config = [
                "; BIND data file "+domain+"\n\n",
                "$TTL\t604800\n",
                "@\tIN\tSOA\t"+domain+". root."+domain+". (\n",
                "\t\t\t"+str(id)+"\t; Serial\n",
                "\t\t\t604800\t; Refresh\n",
                "\t\t\t86400\t; Retry\n",
                "\t\t\t2419200\t; Expire\n",
                "\t\t\t604800 )\t; Negative Chace TTL\n",
                ";\n",
                "@\tIN\tNS\t"+domain+".\n",
                "@\tIN\tA\t"+str(ip)+"\n\n",
            ]
        return config

    def dns_file_config(id, domain, ip, subdomain):
        config = Network.dns_default_config(id, domain, ip)

        for sub in subdomain:
            config += sub.name+"\t\tIN\t"+sub.type+"\t"+str(sub.ip)+"\n"
            print(config)

        file_config = open(r"/etc/bind/zones/"+domain+".db","r+")
        file_config.writelines(config)
        file_config.close()

        x = subprocess.check_output("service bind9 restart", shell=True, text=False)

        return ''

    def dns_config(domains):
        config = '# Config File for bind9\n\n'
        for domain in domains:
            config += "zone \""+domain.name+"\" {\n"
            config += "\ttype master;\n"
            config += "\tfile \"/etc/bind/zones/"+domain.name+".db\";\n};\n\n"

            file_dns = Network.dns_default_config(domain.id, domain.name, domain.ip)

            if os.path.isfile("/etc/bind/zones/"+domain.name+".db") is False:   
                file_config = open(r"/etc/bind/zones/"+domain.name+".db","w+")
                file_config.writelines(file_dns)
                file_config.close()

        file_config = open(r"/etc/bind/named.conf.local","w+")
        file_config.truncate(0)
        file_config.writelines(config)
        file_config.close()

        x = subprocess.check_output("service bind9 restart", shell=True, text=False)

        return ''

    def dns_delete(domain):
        if os.path.isfile("/etc/bind/zones/"+domain+".db") is True: 
            os.remove("/etc/bind/zones/"+domain+".db")

        x = subprocess.check_output("service bind9 restart", shell=True, text=False)
        return ''
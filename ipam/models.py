from django.db import models

class OS(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Subnet(models.Model):
    netmask = models.CharField(max_length=15)
    ip_network = models.CharField(max_length=15)
    ip_broadcast = models.CharField(max_length=15)
    description = models.TextField()

    def __str__(self):
        return self.ip_network

class Ip_address(models.Model):
    ip_address = models.CharField(max_length=15)
    hostname = models.CharField(max_length=25)
    description = models.TextField()
    subnet = models.ForeignKey(Subnet, on_delete=models.CASCADE)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    os = models.ForeignKey(OS,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.ip_address

class Dhcp_Config(models.Model):
    config = models.CharField(max_length=20)
    value = models.CharField(max_length=20)

    def __str__(self):
        return self.config

class Dhcp_static(models.Model):
    name = models.CharField(max_length=20)
    mac = models.CharField(max_length=30)
    ip = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

class Application(models.Model):
    name = models.CharField(max_length=20)
    protocol = models.CharField(max_length=5)
    ip = models.ForeignKey(Ip_address, on_delete=models.CASCADE)
    port = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='app/', null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ConfigPortal(models.Model):
    config = models.CharField(max_length=25)
    value = models.CharField(max_length=70)

    def __str__(self):
        return self.value
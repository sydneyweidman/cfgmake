from django.db import models

# Create your models here.


def ip_validator(ip):
    """Check for valid IP"""
    return True

class Server(models.Model):

    ipaddr = models.IPAddressField(max_length=20, validators=[ip_validator])
    domain = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    hostname = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=255)

    def fqdn(self):
        """Compose the fully qualified domain name from the hostname and domain
        >>> from cfgmake.models import Server
        >>> svr = Server(hostname="foo")
        >>> svr.domain = "uwinnipeg.ca"
        >>> svr.fqdn()
        'foo.uwinnipeg.ca'
        """
        return '.'.join([self.hostname, self.domain])
    
class UnixUser(models.Model):

    iscrypted = models.BooleanField()
    login = models.CharField(max_length=50, blank=False, null=False)
    passwd = models.CharField(verbose_name="Password", max_length=255)
    uid = models.IntegerField(verbose_name="User ID", blank=False, null=False)
    gid = models.IntegerField(verbose_name="Group ID", blank=False, null=False)
    fullname = models.CharField(max_length=255)
    home = models.CharField(verbose_name="Home Directory", max_length=255)

class ConfigFile(models.Model):

    path = models.CharField(max_length=255)
    template = models.FileField(upload_to="config/")

class Application(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    executable = models.CharField(max_length=255)
    configfiles = models.ForeignKey(ConfigFile)

